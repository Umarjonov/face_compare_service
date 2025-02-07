from fastapi import FastAPI, File, UploadFile, Depends, Query, HTTPException
from fastapi.responses import FileResponse
import os
from auth import verify_token, router as auth_router
from utils.image_utils import save_image
from models.face_model import compare_faces

# FastAPI ilovasini yaratish
app = FastAPI()

# Suratlarni saqlash uchun kataloglarni yaratish
UPLOAD_FOLDER = "images"
AVATAR_FOLDER = "avatar"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AVATAR_FOLDER, exist_ok=True)

# Faylni saqlash va tekshirish uchun umumiy funksiya
def save_and_validate_image(file: UploadFile, folder: str) -> str:
    file_path = os.path.join(folder, file.filename)
    try:
        save_image(file, file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rasmni saqlashda xatolik: {str(e)}")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=500, detail="Fayl saqlanmadi.")
    return file_path

# Routerlarni qo'shish
app.include_router(auth_router)

# Asosiy API endpointlari
@app.get("/")
async def root():
    return FileResponse("index.html")

@app.post("/upload/avatar/")
async def upload_avatar(file: UploadFile = File(...), user_id: str = Depends(verify_token)):
    return {"filename": file.filename, "file_path": save_and_validate_image(file, AVATAR_FOLDER)}

@app.post("/compare/")
async def compare_faces_api(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    file1_path = save_and_validate_image(file1, UPLOAD_FOLDER)
    file2_path = save_and_validate_image(file2, UPLOAD_FOLDER)
    try:
        return compare_faces(file1_path, file2_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yuzlarni taqqoslashda xatolik: {str(e)}")

@app.post("/user_verify/")
async def user_verify(
    file: UploadFile = File(...),
    user_id: int = Query(..., title="User ID", description="Foydalanuvchi ID si")
):
    avatar_path = os.path.join(AVATAR_FOLDER, f"{user_id}.jpg")
    if not os.path.exists(avatar_path):
        raise HTTPException(status_code=404, detail=f"Avatar rasm topilmadi: {avatar_path}")
    uploaded_file_path = save_and_validate_image(file, UPLOAD_FOLDER)
    try:
        return compare_faces(uploaded_file_path, avatar_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yuzlarni taqqoslashda xatolik: {str(e)}")