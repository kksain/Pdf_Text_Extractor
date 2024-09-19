from django.shortcuts import render, redirect
from django.http import HttpResponse
import zipfile
from io import BytesIO
from extractor.models import PDFFile
from extractor.forms import PDFFileForm
import fitz
import os
from PIL import Image
from django.conf import settings

MAX_IMAGES = 50


def compress_image(image_path, max_size_kb=200):
    """Compress the image to be under max_size_kb while maintaining quality."""
    try:
        img = Image.open(image_path)
        if img.format.lower() not in ['jpeg', 'png']:
            return
        quality = 85
        while os.path.getsize(image_path) > (max_size_kb * 1024) and quality > 10:
            img.save(image_path, optimize=True, quality=quality)
            quality -= 5
    except Exception as e:
        print(f"Error compressing image: {e}")


def upload_pdf(request):
    if request.method == 'POST':
        form = PDFFileForm(request.POST, request.FILES)
        if form.is_valid:
            pdf_file = form.save()
            return redirect('extract_text', pk=pdf_file.pk)

    else:
        form = PDFFileForm()
        return render(request, 'extractor/upload.html', {'form': form})


def extract_text(request, pk):
    pdf_file = PDFFile.objects.get(pk=pk)
    doc = fitz.open(pdf_file.file.path)
    text = ""
    image_paths = []
    image_count = 0

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        text += page.get_text()

        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            if image_count >= MAX_IMAGES:
                break
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            img_filename = f'pdf_image_{pk}_{page_num}_{img_index}.png'
            img_filepath = os.path.join(settings.MEDIA_ROOT, img_filename)

            try:
                with open(img_filepath, "wb") as img_file:
                    img_file.write(image_bytes)
                compress_image(img_filepath)

                image_url = f'{settings.MEDIA_URL}{img_filename}'
                image_paths.append(image_url)
                image_count += 1
            except IOError:
                print(f"Error: Could not save or access {img_filename}")

    context = {
        'text': text,
        'pdf_file': pdf_file,
        'images': image_paths,
        'image_count': image_count,
        'max_images': MAX_IMAGES,
    }
    return render(request, 'extractor/result.html', context)


def download_images_as_zip(request, pk):
    pdf_file = PDFFile.objects.get(pk=pk)
    doc = fitz.open(pdf_file.file.path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            if len(image_paths) >= MAX_IMAGES:
                break
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_filename = f'pdf_image_{pk}_{page_num}_{img_index}.png'
            img_filepath = os.path.join(settings.MEDIA_ROOT, img_filename)
            image_paths.append(img_filepath)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for image_path in image_paths:
            zip_file.write(image_path, os.path.basename(image_path))

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{
        pdf_file.file.name}_images.zip"'
    return response
