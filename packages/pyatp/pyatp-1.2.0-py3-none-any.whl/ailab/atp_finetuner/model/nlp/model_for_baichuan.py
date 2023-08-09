from typing import List
import torch
from transformers import AutoModelForCausalLM,AutoConfig
from peft import TaskType,LoraConfig,get_peft_model
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.question_answering, Model.baichuan_7b))
@ModelRg.register((Task.question_answering, Model.baichuan_13b))
@ModelRg.register((Task.question_answering, Model.bloomz_7b1_mt))
@ModelRg.register((Task.question_answering, Model.falcon_7b))
@ModelRg.register((Task.question_answering, Model.moss_moon_003_base))
@ModelRg.register((Task.question_answering, Model.llama2_7b))
class BaichuanModel(AILabModel):
    def __init__(self, model: any) -> None:
        self.model_name = None
        super().__init__(model)

    def forward(self):
        model = self.model_ins
        output_embedding_layer_name = "lm_head"
        layer_norm_names = ["norm", "ln_f", "ln_attn", "ln_mlp"]
        for name, param in model.named_parameters():
            if param.ndim == 1 and any(layer_norm_name in name for layer_norm_name in layer_norm_names):
                param.data = param.data.to(torch.float32)

        if hasattr(model, "enable_input_require_grads"):
            model.enable_input_require_grads()
        else:
            def make_inputs_require_grad(module, input, output):
                output.requires_grad_(True)
            model.get_input_embeddings().register_forward_hook(make_inputs_require_grad)

        model.gradient_checkpointing_enable()
        model.config.use_cache = False # turn off when gradient checkpointing is enabled

        if hasattr(model, output_embedding_layer_name):
            output_embedding_layer: torch.nn.Linear = getattr(model, output_embedding_layer_name)
            input_dtype = output_embedding_layer.weight.dtype

            class CastOutputToFloat(torch.nn.Sequential):
                def forward(self, x: torch.Tensor) -> torch.Tensor:
                    return super().forward(x.to(input_dtype)).to(torch.float32)

            setattr(model, output_embedding_layer_name, CastOutputToFloat(output_embedding_layer))


        target_modules_dict = {
            Model.baichuan_7b : ['W_pack'],
            Model.baichuan_13b : ['W_pack'],
            Model.bloomz_7b1_mt : ['query_key_value'],
            Model.falcon_7b : ['query_key_value'],
            Model.moss_moon_003_base : ['q_proj','v_proj'],
            Model.llama2_7b : ['q_proj','v_proj']
        }
        
        lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                inference_mode=False,
                r=8,
                lora_alpha=32.0,
                lora_dropout=0.1,
                target_modules=target_modules_dict.get(self.model_name),
            )
        model = get_peft_model(model, lora_config)

        def print_trainable_params(model: torch.nn.Module) -> None:
            trainable_params, all_param = 0, 0
            for param in model.parameters():
                num_params = param.numel()
                # if using DS Zero 3 and the weights are initialized empty
                if num_params == 0 and hasattr(param, "ds_numel"):
                    num_params = param.ds_numel
                all_param += num_params
                if param.requires_grad:
                    trainable_params += num_params
            print("trainable params: {:d} || all params: {:d} || trainable%: {:.4f}".format(
                        trainable_params, all_param, 100 * trainable_params / all_param))
        print_trainable_params(model)
        self._model = model
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        config = AutoConfig.from_pretrained(model_name_or_dir, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_dir,
            config=config,
            torch_dtype= torch.float16,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        if hasattr(config, "auto_map") and "AutoConfig" in config.auto_map:
            config.__class__.register_for_auto_class()
        if hasattr(config, "auto_map") and "AutoModelForCausalLM" in config.auto_map:
            model.__class__.register_for_auto_class()
        cls_model =  cls(model)
        cls_model.model_name = model_name
        return cls_model
    
    def get_inside_models(self, model_type:str):
        pass
