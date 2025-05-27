import torch

from project_settings import ML_Models


device = "cuda" if torch.cuda.is_available() else "cpu"
ML_Models(device="cpu",
          transcription_model_name="dvislobokov/whisper-large-v3-turbo-russian",
          tagging_model_name="DeepPavlov/rubert-base-cased")