from django.shortcuts import render
import torch
from diffusers import DiffusionPipeline
from safetensors.torch import load_file
import os
from datetime import datetime

# Configuración del modelo
MODEL_DIR = "./output_model_lora"
BASE_MODEL = "stabilityai/stable-diffusion-2-1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Carga del pipeline
pipe = DiffusionPipeline.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    safety_checker=None,
    requires_safety_checker=False
).to(DEVICE)
pipe.enable_attention_slicing()

# Aplicar LoRA
lora_path = os.path.join(MODEL_DIR, "diffusion_pytorch_model.safetensors")
lora_weights = load_file(lora_path, device=DEVICE)
pipe.unet.load_state_dict(lora_weights, strict=False)

def index(request):
    image_url = None
    if request.method == "POST":
        atributos = request.POST.getlist("atributos")
        prompt = ", ".join(atributos)

        generator = torch.manual_seed(42)
        image = pipe(prompt=prompt, num_inference_steps=40, guidance_scale=7.5, generator=generator).images[0]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"gen_{timestamp}.png"
        path = os.path.join("media/generated", filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image.save(path)

        image_url = "/" + path

    return render(request, "index.html", {"image_url": image_url})

