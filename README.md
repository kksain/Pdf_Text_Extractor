## PDF Extractor and Image Compression
This Django project allows users to upload PDF files, extract text and images from them, compress images, and download the images as a ZIP file. It uses fitz (PyMuPDF) for PDF processing, Pillow for image compression, and Django for web functionality.

## Features
# Upload PDF Files:
Users can upload PDF files through the web interface.
# Extract Text and Images:
Extracts text and images from the uploaded PDFs.
# Image Compression:
Extracted images are compressed to reduce file size without significant loss in quality.
# Download as ZIP:
Allows users to download all extracted images as a single ZIP file.

## Installation
Clone this repository:
git clone https://github.com/kksain/Pdf_Text_Extractor.git
cd pdf_text_extractor
# Install the required packages:
pip install -r requirements.txt
# Set up the Django project:
python manage.py migrate
python manage.py runserver
Open your browser and go to http://127.0.0.1:8000/ to access the upload page.

## Usage
# Upload a PDF: Users can upload a PDF file on the main page.
# Extract Text and Images: Upon successful upload, the application extracts text and images from the PDF.
# Compressed Images: Extracted images are compressed to a size less than 200KB while maintaining quality.
# Download Images as ZIP: Users can download all extracted and compressed images in a single ZIP file.
