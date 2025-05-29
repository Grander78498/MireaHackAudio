import torch

from project_settings import ML_Models


device = "cuda" if torch.cuda.is_available() else "cpu"
model_whisper_name = "dvislobokov/whisper-large-v3-turbo-russian"
model_bert_name = "DeepPavlov/rubert-base-cased"
ML_Models(device="cpu",
          model_whisper_name=model_whisper_name,
          model_bert_name=model_bert_name)