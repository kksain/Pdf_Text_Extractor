from django.urls import path
from . import views


urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('extract/<int:pk>/', views.extract_text, name='extract_text'),
    path('extract/<int:pk>/download-images/',
         views.download_images_as_zip, name='download_images_as_zip'),
]
