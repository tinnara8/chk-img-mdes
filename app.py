import cv2
import imagehash
from PIL import Image

from flask_ngrok import run_with_ngrok
from flask import Flask, request, jsonify
from pyngrok import ngrok



def compare_images(image1_path, image2_path, threshold=80):
    """
    เปรียบเทียบสองรูปภาพและส่งคืนค่า True หากมีความคล้ายคลึงกันเกินเกณฑ์ที่กำหนด
    """
    hash1 = imagehash.average_hash(Image.open(image1_path))
    hash2 = imagehash.average_hash(Image.open(image2_path))
    similarity = 100 - (hash1 - hash2)
    return similarity >= threshold





app = Flask(__name__)
run_with_ngrok(app)  # เริ่ม ngrok เมื่อแอปเริ่มทำงาน



ngrok.set_auth_token("2o0eKXKbEsEflTnDpwxf4v6ZO6r_77R596zwNDkpZ419uqBBR") # Replace with your token if it's different
public_url = ngrok.connect(5000).public_url # Connects to port 5000
print(f" * Running on {public_url}")

@app.route('/compare', methods=['POST'])
def compare():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    image = request.files['image']
    image.save('uploaded_image.jpg')
    similarity = compare_images('mdes.jpeg', 'uploaded_image.jpg')
    return jsonify({'similar': similarity})


@app.route("/")
def home():
    return "<h1>Hello from Flask YUUUU!</h1>"

if __name__ == "__main__":
    app.run()