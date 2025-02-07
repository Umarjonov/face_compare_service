from deepface import DeepFace

# Yuzlarni taqqoslash funksiyasi
def compare_faces(image_path1: str, image_path2: str):
    result = DeepFace.verify(img1_path=image_path1, img2_path=image_path2)
    return {"verified": result["verified"], "distance": result["distance"]}