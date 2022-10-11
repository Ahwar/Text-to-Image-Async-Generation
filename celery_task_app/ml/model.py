import os

from torch import autocast
from diffusers import StableDiffusionPipeline
import torch

import json
import numpy as np

torch.cuda.empty_cache()

MODEL_PATH = os.environ['MODEL_PATH']

# class and functions on how to load and run inferences on model
# rename ChurnModel text_to_image_model
class ChurnModel:

    """ Wrapper for loading and serving pre-trained model"""

    def __init__(self):
        self.model_id = MODEL_PATH
        self.device = "cuda"
        self.model = self._load_model_from_path(self)

    @staticmethod
    def _load_model_from_path(self):
        # load the model using Stable Diffusion Pipeline  
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            revision="fp16",
            torch_dtype=torch.float16,
            use_auth_token=True,
            allow_nsfw=True,
        )
        pipe.enable_attention_slicing()
        pipe = pipe.to(self.device)
        return pipe

    def predict(self, data, return_option='Prob'):
        # take user input from streamlit
        # generate 2 imagesk, duplicate text
        user_input = data[0]["user_input"]
        no_of_images = data[0]["no_of_images"]
        prompt = [str(user_input)] * no_of_images
        with autocast("cuda"):
            # guidance_scale parameter part of model
            images = self.model(
                prompt,
                height=512,
                width=512,
                guidance_scale=7.5,
                revision="fp16",
                torch_dtype=torch.float16,
                allow_nsfw=True,
            ).images

        predictions = { idx: np.array(img).tolist() for idx, img in enumerate(images)}
        predictions = json.dumps(predictions)
        return predictions

