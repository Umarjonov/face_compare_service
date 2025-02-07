import os
from fastapi import UploadFile

# Rasmni saqlash funksiyasi
def save_image(file: UploadFile, file_path: str):
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())