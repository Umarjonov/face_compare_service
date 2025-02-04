import cv2
import numpy as np

def read_image(file_path: str):
    """Suratni o‘qish va numpy massivga aylantirish"""
    img = cv2.imread(file_path)
    return img

def save_image(file, save_path: str):
    """Suratni serverga saqlash"""
    with open(save_path, "wb") as buffer:
        buffer.write(file.file.read())
    return save_path
