from deepface import DeepFace

def compare_faces(img1_path: str, img2_path: str):
    """Ikki suratni taqqoslaydi va o‘xshashlikni aniqlaydi"""
    try:
        result = DeepFace.verify(img1_path, img2_path)
        return {
            "verified": result["verified"],
            "distance": result["distance"],
            "threshold": result["threshold"],
            "similarity_score": 1 - result["distance"]
        }
    except Exception as e:
        return {"error": str(e)}

