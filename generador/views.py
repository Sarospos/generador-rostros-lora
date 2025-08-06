from django.shortcuts import render
import requests
import base64
import os
from datetime import datetime
from django.conf import settings

ATRIBUTOS = sorted([
    "5_o_Clock_Shadow", "Arched_Eyebrows", "Attractive", "Bags_Under_Eyes", "Bald", "Bangs",
    "Big_Lips", "Big_Nose", "Black_Hair", "Blond_Hair", "Blurry", "Brown_Hair", "Bushy_Eyebrows",
    "Chubby", "Double_Chin", "Eyeglasses", "Goatee", "Gray_Hair", "Heavy_Makeup", "High_Cheekbones",
    "Male", "Mouth_Slightly_Open", "Mustache", "Narrow_Eyes", "No_Beard", "Oval_Face", "Pale_Skin",
    "Pointy_Nose", "Receding_Hairline", "Rosy_Cheeks", "Sideburns", "Smiling", "Straight_Hair",
    "Wavy_Hair", "Wearing_Earrings", "Wearing_Hat", "Wearing_Lipstick", "Wearing_Necklace",
    "Wearing_Necktie", "Young"
])

def index(request):
    imagenes_generadas = []

    if request.method == "POST":
        seleccionados = request.POST.getlist("atributos")
        prompt = ", ".join(seleccionados)

        rostros_dir = os.path.join(settings.MEDIA_ROOT, "rostros")
        os.makedirs(rostros_dir, exist_ok=True)

        for i in range(9):  # Generar 9 imágenes
            try:
                response = requests.post(
                    "https://b3d5fe3f6690.ngrok-free.app/generar/",
                    json={"prompt": prompt}
                )
                if response.status_code == 200:
                    img_base64 = response.json()["imagen"]
                    filename = f"imagen_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{i}.png"
                    filepath = os.path.join(rostros_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(base64.b64decode(img_base64))
                    imagenes_generadas.append(f"rostros/{filename}")
                else:
                    print("Error en la respuesta del servidor:", response.text)
            except Exception as e:
                print("Error de conexión con el servidor:", str(e))

    atributos_legibles = [(a, a.replace("_", " ")) for a in ATRIBUTOS]
    return render(request, "index.html", {"atributos": atributos_legibles, "imagenes_generadas": imagenes_generadas})

def galeria(request):
    rostros_dir = os.path.join(settings.MEDIA_ROOT, "rostros")
    if not os.path.exists(rostros_dir):
        images = []
    else:
        images = [f"rostros/{img}" for img in os.listdir(rostros_dir) if img.endswith('.png') or img.endswith('.jpg')]
    return render(request, "galeria.html", {"images": images})

def landing(request):
    return render(request, "landing.html")