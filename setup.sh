#!/bin/bash

echo "🔧 Muhit sozlanmoqda..."

# Python virtual muhitni yaratish
python3 -m venv venv
source venv/bin/activate

# Pip va kutubxonalarni yangilash
pip install --upgrade pip setuptools wheel

# Kutubxonalarni o‘rnatish
pip install fastapi uvicorn deepface opencv-python numpy pillow python-multipart

# TensorFlow MacOS uchun optimallashtirish
if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "🖥 MacOS aniqlangan. TensorFlow optimallashtirilmoqda..."
    pip install tensorflow-macos tensorflow-metal
else
    echo "🐧 Linux aniqlangan. Oddiy TensorFlow o‘rnatilmoqda..."
    pip install tensorflow
fi

echo "✅ Muhit tayyor!"
