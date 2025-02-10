from flask import Flask, request, jsonify
import os
import subprocess
import cv2
import numpy as np
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from shamir import * # preprocessing, polynomial, insert_text_chunk, get_file_size  # Ensure these exist

app = Flask(__name__)

# Securely store this key (use a database or environment variable in production)
SECRET_KEY = os.urandom(24)  # 24-byte key for Triple DES

def encrypt_triple_des(data, key):
    """Encrypt data using Triple DES (3DES) with CBC mode."""
    backend = default_backend()
    iv = os.urandom(8)  # 3DES requires an 8-byte IV
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    # Pad the data to fit block size
    padder = padding.PKCS7(algorithms.TripleDES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data  # Store IV at the beginning

def decrypt_triple_des(encrypted_data, key):
    """Decrypt data using Triple DES (3DES) with CBC mode."""
    backend = default_backend()
    iv = encrypted_data[:8]  # Extract IV
    encrypted_data = encrypted_data[8:]  # Get actual encrypted content

    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    
    return decrypted_data

@app.route('/register', methods=['POST'])
def register():
    file = request.files['file']
    file.save("wat.png")

    # Preprocess the image and generate shares
    img_flattened, shape = preprocessing('wat.png')
    secret_imgs, imgs_extra = polynomial(img_flattened, n=3, r=2)
    
    to_save = secret_imgs.reshape(3, *shape)
    
    for i, img in enumerate(to_save):
        secret_img_path = f"secret_{i + 1}.png"
        encrypted_img_path = f"secret_{i + 1}.png.enc"

        # Save the share image
        Image.fromarray(img.astype(np.uint8)).save(secret_img_path)
        
        # Embed extra data into the share
        img_extra = str(list((imgs_extra[i]))).encode()
        insert_text_chunk(secret_img_path, secret_img_path, img_extra)

        # Encrypt the share
        with open(secret_img_path, "rb") as f:
            encrypted_data = encrypt_triple_des(f.read(), SECRET_KEY)

        with open(encrypted_img_path, "wb") as f:
            f.write(encrypted_data)

        size = get_file_size(encrypted_img_path)
        print(f"{encrypted_img_path} saved. Size: {size} bytes")

    return jsonify({"message": "Registration successful, shares encrypted."})

@app.route('/login', methods=['POST'])
def login():
    file = request.files['file']
    file.save("uploaded_share.png")

    # Decrypt the received share
    with open("uploaded_share.png", "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = decrypt_triple_des(encrypted_data, SECRET_KEY)
        with open("decrypted_share.png", "wb") as f:
            f.write(decrypted_data)
        print("Decryption successful.")
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"})

    import time 
    command = ['python', 'Shamir.py', '-d', 'decrypted_share.png', '-r', '2', '-i', '1', '2']
    # start_time = time.time()
    # print("\n=== Starting image decoding process ===")


    # input_imgs = []
    # input_imgs_extra = []
    # indices = [1 , 2]
    # for i in indices:
    #     secret_img_path = f"secret_{i}.png"
    #     img_extra = read_text_chunk(secret_img_path)
    #     img, shape = preprocessing(secret_img_path)
    #     input_imgs.append(img)
    #     input_imgs_extra.append(img_extra)
    # input_imgs = np.array(input_imgs)
    # origin_img = decode(input_imgs, input_imgs_extra, indices, r=2)
    # origin_img = origin_img.reshape(*shape)
    # Image.fromarray(origin_img.astype(np.uint8)).save('decrypted_share.png')
    # size = get_file_size('decrypted_share.png')

    # end_time = time.time()


    #print("=== Image decoding completed. Time elapsed: {:.2f} seconds ===".format(end_time - start_time))
  
    subprocess.run(command)

    compare_images(r'Water_Marked_img.png', r'decrypted_share.png')

    return jsonify({"message": "Share received, decrypted, and processed for authentication."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
