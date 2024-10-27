import cv2
import imagehash
from PIL import Image
from flask import Flask, request, jsonify
from pyngrok import ngrok

# ฟังก์ชันสำหรับเปรียบเทียบความเหมือนของภาพ
def compare_images(image1_path, image2_path, threshold=80):
    hash1 = imagehash.average_hash(Image.open(image1_path))
    hash2 = imagehash.average_hash(Image.open(image2_path))
    similarity = 100 - (hash1 - hash2)
    return similarity >= threshold

# เริ่ม Flask
app = Flask(__name__)

# ตั้งค่า ngrok
ngrok.set_auth_token("2o0eKXKbEsEflTnDpwxf4v6ZO6r_77R596zwNDkpZ419uqBBR")
public_url = ngrok.connect(5000).public_url
print(f" * Running on {public_url}")

# กำหนด endpoint สำหรับการเปรียบเทียบภาพ
@app.route('/compare', methods=['POST'])
def compare():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # บันทึกภาพที่อัปโหลดขึ้นเซิร์ฟเวอร์
    image = request.files['image']
    upload_path = 'uploaded_image.jpg'
    image.save(upload_path)
    
    # เปรียบเทียบภาพที่อัปโหลดกับ mdes.jpg
    similarity = compare_images('mdes.jpg', upload_path)
    return jsonify({'similar': similarity})

# กำหนด endpoint สำหรับหน้าแรก
@app.route("/")
def home():
    return "<h1>Hello from Flask YUUUU!</h1>"

if __name__ == "__main__":
    # รัน Flask server บนพอร์ต 5000
    app.run(port=5000)
