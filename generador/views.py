from django.shortcuts import render
import torch
from diffusers import DiffusionPipeline
from safetensors.torch import load_file
import os
from datetime import datetime

# === Lista completa de atributos ===
ATRIBUTOS = sorted([
    "5_o_Clock_Shadow", "Arched_Eyebrows", "Attractive", "Bags_Under_Eyes", "Bald", "Bangs",
    "Big_Lips", "Big_Nose", "Black_Hair", "Blond_Hair", "Blurry", "Brown_Hair", "Bushy_Eyebrows",
    "Chubby", "Double_Chin", "Eyeglasses", "Goatee", "Gray_Hair", "Heavy_Makeup", "High_Cheekbones",
    "Male", "Mouth_Slightly_Open", "Mustache", "Narrow_Eyes", "No_Beard", "Oval_Face", "Pale_Skin",
    "Pointy_Nose", "Receding_Hairline", "Rosy_Cheeks", "Sideburns", "Smiling", "Straight_Hair",
    "Wavy_Hair", "Wearing_Earrings", "Wearing_Hat", "Wearing_Lipstick", "Wearing_Necklace",
    "Wearing_Necktie", "Young"
])

# === Configuración del modelo ===
MODEL_DIR = "./output_model_lora"
BASE_MODEL = "stabilityai/stable-diffusion-2-1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# === Cargar modelo solo una vez ===
print("🔁 Cargando modelo...")
pipe = DiffusionPipeline.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    safety_checker=None,
    requires_safety_checker=False,
).to(DEVICE)
pipe.enable_attention_slicing()

# === Aplicar pesos LoRA ===
lora_path = os.path.join(MODEL_DIR, "diffusion_pytorch_model.safetensors")
if os.path.exists(lora_path):
    lora_weights = load_file(lora_path, device=DEVICE)
    pipe.unet.load_state_dict(lora_weights, strict=False)
    print("✅ LoRA aplicado correctamente.")
else:
    print("⚠️ No se encontró el archivo de pesos LoRA.")

# === Vista principal ===
def index(request):
    imagen_generada = None

    if request.method == "POST":
        seleccionados = request.POST.getlist("atributos")
        prompt = ", ".join(seleccionados)
        generator = torch.manual_seed(42)

        # Generar imagen
        image = pipe(prompt=prompt, num_inference_steps=40, guidance_scale=7.5, generator=generator).images[0]

        # Guardar imagen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"imagen_{timestamp}.png"
        ruta_completa = os.path.join("media", nombre_archivo)
        image.save(ruta_completa)

        imagen_generada = nombre_archivo

    return render(request, "index.html", {
        "atributos": [(a, a.replace("_", " ")) for a in ATRIBUTOS],
        "imagen_generada": imagen_generada
    })
