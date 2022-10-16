import os

from torch import autocast
from diffusers import StableDiffusionInpaintPipeline
import torch
import json
import numpy as np
from PIL import Image

torch.cuda.empty_cache()

MODEL_PATH = os.environ["MODEL_PATH"]

# class and functions on how to load and run inferences on model
# rename GenerationModel text_to_image_model
class GenerationModel:

    """Wrapper for loading and serving pre-trained model"""

    def __init__(self):
        self.model_id = MODEL_PATH
        self.device = "cuda"
        self.model = self._load_model_from_path(self)

    @staticmethod
    def _load_model_from_path(self):
        # load the model using Stable Diffusion Pipeline
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            self.model_id,
            revision="fp16",
            torch_dtype=torch.float16,
            use_auth_token=True,
            allow_nsfw=True,
        )
        pipe.enable_attention_slicing()
        pipe = pipe.to(self.device)
        return pipe

    def predict(self, data):
        # take user input from streamlit
        # generate 2 imagesk, duplicate text
        prompt = data[0]["prompt"]
        print(prompt)
        # init_image = Image.fromarray(np.array(data[0]["image"], dtype="uint8"))
        # mask_image = Image.fromarray(np.array(data[0]["mask_image"], dtype="uint8"))

        # init_image = Image.fromarray(np.array(json.loads(data[0]["image"]), dtype="uint8"))
        # mask_image = Image.fromarray(np.array(json.loads(data[0]["mask_image"]), dtype="uint8"))

        init_image = Image.fromarray(np.array(json.loads(data[0]["image"]), dtype='uint8'))
        mask_image = Image.fromarray(np.array(json.loads(data[0]["mask_image"]), dtype='uint8'))
        with autocast("cuda"):
            # guidance_scale parameter part of model
            images = self.model(
                prompt=prompt,
                init_image=init_image,
                mask_image=mask_image,
                strength=0.75,
                guidance_scale=7.5,
                
            ).images

        results = json.dumps(np.array(images[0]).tolist())
        return results
