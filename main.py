from fastapi import FastAPI, File, UploadFile
import os
import shutil
from deepface import DeepFace
from models.face_model import compare_faces
from utils.image_utils import save_image

app = FastAPI()

UPLOAD_FOLDER = "images/"
LOCAL_IMAGE_PATH = "local_image/img_1.png"  # Lokal rasm yo'li
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Face Recognition API ishlamoqda"}

# Suratni yuklash
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    save_image(file, file_path)
    return {"filename": file.filename, "file_path": file_path}

# Yuzni taqqoslash
@app.post("/compare/")
async def compare_faces_api(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    file1_path = os.path.join(UPLOAD_FOLDER, file1.filename)
    file2_path = os.path.join(UPLOAD_FOLDER, file2.filename)

    save_image(file1, file1_path)
    save_image(file2, file2_path)

    result = compare_faces(file1_path, file2_path)
    return result


@app.post("/compare_with_local/")
async def compare_with_local(file: UploadFile = File(...)):
    """ Yuklangan rasmni lokal rasm bilan taqqoslaydi """

    # Rasmni vaqtinchalik saqlash
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    save_image(file, uploaded_file_path)

    # Lokal rasmni yuklangan rasm bilan taqqoslash
    try:
        result = DeepFace.verify(uploaded_file_path, LOCAL_IMAGE_PATH, detector_backend='opencv')
        return {
            "verified": result["verified"],
            "distance": result["distance"],
            "threshold": result["threshold"],
            "similarity_score": 1 - result["distance"]
        }
    except Exception as e:
        return {"error": str(e)}