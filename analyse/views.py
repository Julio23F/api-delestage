# import pytesseract
# import re
# import json
# from django.shortcuts import render
# from .forms import ImageUploadForm
# from PIL import Image

# def extract_data(image_path):
#     texte = pytesseract.image_to_string(Image.open(image_path), lang='fra')
#     match = re.search(r'\b\d{2}H00\s*-\s*\d{2}H00\b', texte)
#     horaire = match.group(0) if match else "Inconnu"
#     start = texte.find(horaire) + len(horaire)
#     quartiers_bruts = texte[start:]
#     quartiers = re.split(r'\s*[-,]\s*', quartiers_bruts)
#     quartiers = [q.strip() for q in quartiers if len(q.strip()) > 2]
#     return {horaire: quartiers}

# def analyse_image(request):
#     data = None
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save()
#             path = instance.image.path
#             data = extract_data(path)

#             # Enregistrer en JSON
#             with open('media/resultat.json', 'w', encoding='utf-8') as f:
#                 json.dump(data, f, ensure_ascii=False, indent=4)

#     else:
#         form = ImageUploadForm()
#     return render(request, 'analyse/index.html', {'form': form, 'data': data})

# ZONE_DE_RECADRAGE = (100, 300, 1200, 900)  # (left, top, right, bottom)

# def extraire_texte_zone(image_path, zone=None):
#     image = Image.open(image_path)
#     if zone:
#         image = image.crop(zone)
#     texte = pytesseract.image_to_string(image, lang='fra')
#     return texte


# import pytesseract
# import re
# import json
# from django.shortcuts import render
# from .forms import ImageUploadForm
# from PIL import Image

# LEFT = 10
# RIGHT = 1000
# TOP = 0
# BOTTOM = 110

# def extraire_texte_zone(image_path):
#     image = Image.open(image_path)
#     width = image.width 
#     # cropped_image = image.crop((LEFT, TOP, width, BOTTOM))
#     cropped_image = image.crop((LEFT, TOP, RIGHT, BOTTOM))
#     texte = pytesseract.image_to_string(cropped_image, lang='fra')
#     return texte

# def extract_data(image_path):
#     texte = extraire_texte_zone(image_path)
#     match = re.search(r'\b\d{2}H00\s*-\s*\d{2}H00\b', texte)
#     horaire = match.group(0) if match else "Inconnu"
#     start = texte.find(horaire) + len(horaire)
#     quartiers_bruts = texte[start:]
#     quartiers = re.split(r'\s*[-,]\s*', quartiers_bruts)
#     quartiers = [q.strip() for q in quartiers if len(q.strip()) > 2]
#     return {horaire: quartiers}

# def analyse_image(request):
#     data = None
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save()
#             path = instance.image.path
#             data = extract_data(path)

#             # Enregistrer en JSON
#             with open('media/resultat.json', 'w', encoding='utf-8') as f:
#                 json.dump(data, f, ensure_ascii=False, indent=4)

#     else:
#         form = ImageUploadForm()
#     return render(request, 'analyse/index.html', {'form': form, 'data': data})


import pytesseract
import re
import json
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import os


# #Pour les quartier
# LEFT = 235
LEFT = 166
TOP = 205
BOTTOM = 1000


# Pour l'heure
# LEFT = 0
# RIGHT = 300
# TOP = 350
# BOTTOM = 750

def extraire_texte_zone(image_path, cropped_output_path):
    image = Image.open(image_path)
    width = image.width 
    
    cropped_image = image.crop((LEFT, TOP, width, BOTTOM))
    image = Image.open(image_path)
    # cropped_image = image.crop((LEFT, TOP, RIGHT, BOTTOM))

    # Sauvegarder l'image rognée pour affichage
    cropped_image.save(cropped_output_path)

    texte = pytesseract.image_to_string(cropped_image, lang='fra')
    return texte

def extract_data(image_path, cropped_output_path):
    texte = extraire_texte_zone(image_path, cropped_output_path)
    match = re.search(r'\b\d{2}H00\s*-\s*\d{2}H00\b', texte)
    horaire = match.group(0) if match else "Inconnu"
    start = texte.find(horaire) + len(horaire)
    quartiers_bruts = texte[start:]
    quartiers = re.split(r'\s*[-,]\s*', quartiers_bruts)
    quartiers = [q.strip() for q in quartiers if len(q.strip()) > 2]
    return {horaire: quartiers}

def analyse_image(request):
    data = None
    cropped_image_url = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            path = instance.image.path

            # Chemin de l'image rognée
            cropped_path = os.path.join("media", "cropped.jpg")

            # Extraction + sauvegarde de l'image rognée
            data = extract_data(path, cropped_path)

            # Stocker URL relative pour affichage
            cropped_image_url = "/" + cropped_path.replace("\\", "/")

            # Enregistrer en JSON
            with open('media/resultat.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        form = ImageUploadForm()
    return render(request, 'analyse/index.html', {
        'form': form,
        'data': data,
        'cropped_image_url': cropped_image_url
    })
