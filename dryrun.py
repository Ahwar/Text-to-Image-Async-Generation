import json
from typing import List

import torch
from torch import autocast


from io import BytesIO
import numpy as np
from PIL import Image

import requests
import PIL

from diffusers import StableDiffusionInpaintPipeline

def download_as_json(url):
    response = requests.get(url)
    img = PIL.Image.open(BytesIO(response.content)).convert("RGB").resize((512, 512))
    return json.dumps(np.array(img).tolist())

img_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
mask_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo_mask.png"

init_image = download_as_json(img_url)
mask_image = download_as_json(mask_url)

init_image = Image.fromarray(np.array(json.loads(init_image), dtype='uint8'))
mask_image = Image.fromarray(np.array(json.loads(mask_image), dtype='uint8'))

post_data = {
        "prompt": str(prompt),
        "image": init_image,
        "mask_image": mask_image
    }

device = "cuda"
model_id_or_path = "/dev/stable-diffusion-v1-4/"
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    model_id_or_path,
    revision="fp16", 
    torch_dtype=torch.float16,
)
# or download via git clone https://huggingface.co/CompVis/stable-diffusion-v1-4
# and pass `model_id_or_path="./stable-diffusion-v1-4"`.
pipe = pipe.to(device)

prompt = "a cat sitting on a bench"
with autocast("cuda"):
    image = pipe(prompt=prompt, init_image=init_image, mask_image=mask_image, strength=0.75, guidance_scale=7.5).images[0]

image.save("cat_on_bench.png")