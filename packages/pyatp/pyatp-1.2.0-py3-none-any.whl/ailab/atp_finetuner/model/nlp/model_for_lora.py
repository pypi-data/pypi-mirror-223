from typing import List
import torch
from peft import LoraConfig,get_peft_model,prepare_model_for_int8_training
from transformers import LlamaForCausalLM,AutoConfig
from ailab.atp_finetuner.model.model import AILabModel
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.question_answering, Model.alpaca))
@ModelRg.register((Task.question_answering_cn, Model.vicuna))
@ModelRg.register((Task.question_answering_cn, Model.open_llama))
class LoraModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self):
        model = self._model
        model = prepare_model_for_int8_training(model)
        lora_r: int = 8
        lora_alpha: int = 16
        lora_dropout: float = 0.05
        lora_target_modules: List[str] = [
            "q_proj",
            "v_proj",
        ] 

        config = LoraConfig(
            r=lora_r,
            lora_alpha=lora_alpha,
            target_modules=lora_target_modules,
            lora_dropout=lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, config)
        model.print_trainable_parameters()
        model.is_parallelizable = True
        model.model_parallel = True
        self._model = model
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        device_map = "auto"
        model_name_or_dir = model_name if model_dir is None else model_dir

        config = AutoConfig.from_pretrained(model_name_or_dir)
        model = LlamaForCausalLM.from_pretrained(model_name_or_dir,
            from_tf=bool(".ckpt" in model_name_or_dir),
            config=config,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True)
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
