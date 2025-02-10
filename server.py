"""import os
import subprocess
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, send_file
from utils import * 
from shamir import * 
from utils import add_watermark
import jsonify 
import requests 
from datetime import datetime 

app = Flask(__name__)

SECRET_KEY = os.urandom(24)

@app.route('/register', methods=['POST'])
def register():
    
    file = request.files['file']
    print(request.data)
    phone = request.form.get('phone') 
    name = request.form.get('name') 
    email = request.form.get('email') 
    file.save("wat.png")

    img = cv2.imread(r'wat.png')

    user_details = f"{name} {phone} {email} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    watermarked_image = add_watermark(img.copy(), user_details)
    cv2.imwrite('Water_Marked_img.png', watermarked_image)


    img_flattened, shape = preprocessing('Water_Marked_img.png')
    secret_imgs, imgs_extra = polynomial(img_flattened, n=3, r=2)
    to_save = secret_imgs.reshape(3, *shape)
    
    print("share gebn")
    for i, img in enumerate(to_save):
        secret_img_path = f"secret_{i + 1}.png"
        encrypted_img_path = f"secret_{i + 1}.png.enc"
        Image.fromarray(img.astype(np.uint8)).save(secret_img_path)
        img_extra = str(list((imgs_extra[i]))).encode()
        insert_text_chunk(secret_img_path, secret_img_path, img_extra)
        with open(secret_img_path, "rb") as f:
            encrypted_data = encrypt_aes(f.read(), SECRET_KEY)
        with open(encrypted_img_path, "wb") as f:
            f.write(encrypted_data)

    print("ikdhfv")
    encrypted_share = r'secret_1.png.enc'
    target_ip = "http://10.21.14.107:8000"

    files = {"file": open(encrypted_share, "rb")}  # Keep file open during request
    response = requests.post(target_ip, files=files)
    files["file"].close()  # Manually close the file after sending

    return "Registration successful, shares encrypted."


@app.route('/login', methods=['POST'])
def login():
    file = request.files['file']
    file.save("uploaded_share.png")

    with open("uploaded_share.png", "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = decrypt_aes(encrypted_data, SECRET_KEY)
        with open("decrypted_share.png", "wb") as f:
            f.write(decrypted_data)
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 400

    command = ['python', 'Shamir.py', '-d', 'decrypted_share.png', '-r', '2', '-i', '1', '2']
    subprocess.run(command)
    compare_images('Water_Marked_img.png', 'decrypted_share.png')

    # Encrypt and save the processed share
    encrypted_share_path = "encoded_share.png.enc"
    with open("decrypted_share.png", "rb") as f:
        encrypted_data = encrypt_aes(f.read(), SECRET_KEY)
    with open(encrypted_share_path, "wb") as f:
        f.write(encrypted_data)

    # Send the encrypted file back to the client

if __name__ == "__main__":
    app.run(host='10.21.13.36', port=8000)"""



"""import os
import subprocess
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, send_file, jsonify
from utils import * 
from shamir import * 
from utils import add_watermark
import requests 
from datetime import datetime 
import random 

app = Flask(__name__)

SECRET_KEY = b')\xb7(<\xdd\xda\xed\x96\xb3\x1aHP^Ao\x10<\xd4\x16\x8c3\x04\xc9\xe0'

@app.route('/register', methods=['POST'])
def register():
    # Get files from the request
    file2 = request.files.get('file1')
    file3 = request.files.get('file2')

    org  =request.files.get('org')
    org.save(r'org.png')

    # Save the files to disk
    if file2:
        file2.save(r'secret_2.png')
    if file3:
        file3.save(r'secret_3.png')


    # Return a success message
    return jsonify({'message': 'Files saved successfully'}), 200

@app.route('/login' , methods = ['POST'])
def login():

    file1 = request.files.get('file')
    file2 = request.files.get('dec')

    file1.save(r'secret_1.png')
    file2.save(r'restored.png')

    image1 = cv2.imread(r'org.png')
    image2 = cv2.imread(r'restored.png')

    mse = (np.mean((image1 - image2) ** 2) / (255 * 255))

    return jsonify({"mse": mse}), 200

    #if (np.mean((image1 - image2) ** 2) / (255 * 255) )
    #random_share =  random.choice([2, 3])

    #share1 = open(r'share1.enc' , 'wb')

    # share1 = cv2.imread(r'secret_1.png')
    # # with open(r'share1.enc' , 'rb') as f:
    # #     share1 = decrypt_aes(f.read() , SECRET_KEY)

    # if random_share == 1:
    #     share2 = cv2.imread('secret_2.png')
    # else:
    #     share2 = cv2.imread('secret_3.png')

    # #share2 = open(r'share3.enc' , 'rb')
    
    # cv2.imwrite('secret_1.png' , share1)
    # cv2.imwrite(f'secret_{random_share}.png' , share2)

    # print("&&&&&&&&&&&&&&&&&&&&&770 " , random_share)
    # command = ['python', 'shamir.py', '-d', 'reconstucted_img.png', '-r', '2', '-i', str(1) , str(random_share)]
    # subprocess.run(command)
    # print("done")
    # #cv2.imwrite(r'org.png',  org)

    # compare_images(r'reconstucted_img.png', r'org.png')

    return jsonify({"message": "Share received, decrypted, and processed for authentication."})





# @app.route('/register', methods=['POST'])
# def register():

#     file2 = request.files.get('file1')
#     file3 = request.files.get('file2')

    # print(file2)
    # with open('share2.enc', 'wb') as f:
    #     f.write(file2)

    # with open('share3.enc', 'wb') as f:
    #     f.write(file2)
    #file2.save(r'share2.enc')
    #file3.save(r'share3.enc')

    #return jsonify{}
    # with open(r'share1.enc' , '')
    # try:
    #     file = request.files.get('file')
    #     if not file:
    #         return jsonify({"error": "No file uploaded"}), 400

    #     phone = request.form.get('phone', '')
    #     name = request.form.get('name', '')
    #     email = request.form.get('email', '')

    #     if not name or not phone or not email:
    #         return jsonify({"error": "Missing required fields"}), 400

    #     file.save("wat.png")

    #     img = cv2.imread("wat.png")
    #     if img is None:
    #         return jsonify({"error": "Failed to load image"}), 400

    #     user_details = f"{name} {phone} {email} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    #     watermarked_image = add_watermark(img.copy(), user_details)
    #     cv2.imwrite('Water_Marked_img.png', watermarked_image)

    #     img_flattened, shape = preprocessing('Water_Marked_img.png')
    #     secret_imgs, imgs_extra = polynomial(img_flattened, n=3, r=2)
    #     to_save = secret_imgs.reshape(3, *shape)

    #     for i, img in enumerate(to_save):
    #         secret_img_path = f"secret_{i + 1}.png"
    #         encrypted_img_path = f"secret_{i + 1}.png.enc"
    #         Image.fromarray(img.astype(np.uint8)).save(secret_img_path)
    #         img_extra = str(list((imgs_extra[i]))).encode()
    #         insert_text_chunk(secret_img_path, secret_img_path, img_extra)

    #         with open(secret_img_path, "rb") as f:
    #             encrypted_data = encrypt_aes(f.read(), SECRET_KEY)
    #         with open(encrypted_img_path, "wb") as f:
    #             f.write(encrypted_data)

    #     return send_file("secret_1.png.enc", as_attachment=True)

    # except Exception as e:
    #     return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='10.21.13.36', port=8000)"""


import cv2 
import os 
addresses = [
    "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
    "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
    "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
    "0x90F79bf6EB2c4f870365E785982E1f101E93b906",
    "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65",
    "0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc",
    "0x976EA74026E726554dB657fA54763abd0C3a0aa9",
    "0x14dC79964da2C08b23698B3D3cc7Ca32193d9955",
    "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f",
    "0xa0Ee7A142d267C1f36714E4a8F75612F20a79720"
]

balance = ["10000.000000000000000000" * 10]

private_keys = [
    "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
    "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",
    "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a",
    "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6",
    "0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a",
    "0x8b3a350cf5c34c9194ca85829a2df0ec3153be0318b5e2d3348e872092edffba",
    "0x92db14e403b83dfe3df233f83dfa3a0d7096f21ca9b0d6d6b8d88b2b4ec1564e",
    "0x4bbbf85ce3377467afe5d46f804f221813b2bb87f24d81f60f1fcdbf7cbf4356",
    "0xdbda1821b80551c9d65939329250298aa3472ba22feea921c0cf5d620ea67b97",
    "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"
]

import os 

user_index = 0 

roster = r'D:/temthon/Final/Type/NewType/roster'
def store_mapping(user_index , user_name , phone , email  , share2 , share3):
    addr = addresses[user_index]
    bal = balance[user_index]
    priv_key = private_keys[user_index]

    if user_name in os.listdir(roster):
        print("Username already exists")
        return False 
    else:

        print("apjvnkfldnjvfk;" , roster , user_name)
        os.mkdir(os.path.join(roster , user_name))
        os.chdir(os.path.join(roster , user_name))
        with open(r'details.txt' , 'w') as f:
            f.write(user_name)
            f.write(f"Username: {user_name}\n")
            f.write(f"Phone: {phone}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Address: {addr}\n")
            f.write(f"Balance: {bal}\n")
            f.write(f"Private Key: {priv_key}\n")
    

        #cv2.imwrite(r'share2.png' , share2 )
        #cv2.imwrite(r'share3.png' , share3)

        share2.save(r'share2.png')
        share3.save(r'share3.png')

        user_index+=1 
    
        return True
    
import os
import subprocess
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, send_file, jsonify
from utils import * 
from shamir import * 
from utils import add_watermark
import requests 
from datetime import datetime 
import random
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Initialize Flask-Limiter with in-memory storage
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Use the client's IP address as the key
    default_limits=["200 per day", "50 per hour"]  # Default limits for all routes
)

SECRET_KEY = b')\xb7(<\xdd\xda\xed\x96\xb3\x1aHP^Ao\x10<\xd4\x16\x8c3\x04\xc9\xe0'

@app.route('/register', methods=['POST'])
@limiter.limit("10 per minute")  # Limit to 10 requests per minute per IP
def register():
    # Get files from the request
    file2 = request.files.get('file1')
    file3 = request.files.get('file2')
    org = request.files.get('org')

    username = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    print(username , phone , email , "&&&&")

    store_mapping(user_index , username , phone , email , file2  , file3)
    if not org:
        return jsonify({'error': 'No file uploaded'}), 400

    org.save(r'org.png')

    # Save the files to disk
    # if file2:
    #     file2.save(r'secret_2.png')
    # if file3:
    #     file3.save(r'secret_3.png')

    # Return a success message
    return jsonify({'message': 'Files saved successfully'}), 200

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
def login():

    roster = r'D:/temthon/Final/Type/NewType/roster'

    file1 = request.files.get('file')
    file2 = request.files.get('dec')

    user_name = request.form.get('name')

    if not file1 or not file2:
        return jsonify({'error': 'No file uploaded'}), 400

    import os 
    file1.save(os.path.join(roster , user_name , 'secret2.png'))
    file2.save(os.path.join(roster , user_name , 'restored.png'))

    image1 = cv2.imread(os.path.join(roster , user_name , 'org.png'))
    image2 = cv2.imread(os.path.join(roster , user_name , 'restored.png'))

    if image1 is None or image2 is None:
        return jsonify({'error': 'Failed to load images'}), 400

    print(image1.shape , image2.shape)
    if (image1.shape!=image2.shape):
        return jsonify({"error" : "Incorrect Shape"}) , 400
    mse = (np.mean((image1 - image2) ** 2) / (255 * 255))

    return jsonify({"mse": mse}), 200

# Error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "You have exceeded the allowed request rate."
    }), 429

if __name__ == "__main__":
    app.run(host='10.21.13.36', port=8000) # the file

# import os
# import cv2
# import numpy as np
# from PIL import Image
# from flask import Flask, request, send_file, jsonify
# from utils import *  # Assuming custom utilities
# from shamir import *  # Assuming some implementation for Shamir's Secret Sharing
# from utils import add_watermark  # Custom watermark function
# import requests  # If you plan to use this for HTTP requests
# from datetime import datetime
# import random  # Importing random for any random operations in the code
# from flask_limiter import Limiter  # For rate limiting requests
# from flask_limiter.util import get_remote_address  # For rate limiting based on IP address
# import ssl  # Use Python's ssl module instead of OpenSSL directly

# app = Flask(__name__)

# # Initialize Flask-Limiter with in-memory storage
# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"],
#     storage_uri="memory://"
# )

# SECRET_KEY = b')\xb7(<\xdd\xda\xed\x96\xb3\x1aHP^Ao\x10<\xd4\x16\x8c3\x04\xc9\xe0'

# @app.route('/register', methods=['POST'])
# @limiter.limit("10 per minute")  # Limit to 10 requests per minute per IP
# def register():
#     # Get files from the request
#     file2 = request.files.get('file1')
#     file3 = request.files.get('file2')
#     org = request.files.get('org')

#     if not org:
#         return jsonify({'error': 'No file uploaded'}), 400

#     org.save(r'org.png')

#     # Save the files to disk
#     if file2:
#         file2.save(r'secret_2.png')
#     if file3:
#         file3.save(r'secret_3.png')

#     # Return a success message
#     return jsonify({'message': 'Files saved successfully'}), 200

# @app.route('/login', methods=['POST'])
# @limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
# def login():
#     file1 = request.files.get('file')
#     file2 = request.files.get('dec')

#     if not file1 or not file2:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file1.save(r'secret_1.png')
#     file2.save(r'restored.png')

#     image1 = cv2.imread(r'org.png')
#     image2 = cv2.imread(r'restored.png')

#     if image1 is None or image2 is None:
#         return jsonify({'error': 'Failed to load images'}), 400

#     mse = (np.mean((image1 - image2) ** 2) / (255 * 255))

#     return jsonify({"mse": mse}), 200

# # Error handler for rate limit exceeded
# @app.errorhandler(429)
# def ratelimit_handler(e):
#     return jsonify({
#         "error": "Rate limit exceeded",
#         "message": "You have exceeded the allowed request rate."
#     }), 429

# if __name__ == "__main__":
#     # Define certificate and key file names
#     cert_file = "server.pem"
#     key_file = "server.key"

#     # Check if SSL certificates exist, if not generate them
#     if not os.path.exists(cert_file) or not os.path.exists(key_file):
#         print("Certificates not found. Generating self-signed certificates...")

#         # Generate self-signed certificates using Python's ssl module
#         context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#         context.set_ciphers('HIGH:!aNULL:!eNULL')

#         # Generate a self-signed certificate and private key
#         # Save the key and certificate to files in .pem format
#         context.keyfile = key_file
#         context.certfile = cert_file

#         # Write out the certificates
#         with open(cert_file, "w") as cert_out, open(key_file, "w") as key_out:
#             cert_out.write(context.certfile)
#             key_out.write(context.keyfile)

#     # Run the Flask app with HTTPS
#     app.run(host='172.28.135.183', port=8000, ssl_context=(cert_file, key_file))

# import os
# import subprocess
# import cv2
# import numpy as np
# from PIL import Image
# from flask import Flask, request, send_file, jsonify
# from utils import * 
# from shamir import * 
# from utils import add_watermark
# import requests 
# from datetime import datetime 
# import random
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from flask_talisman import Talisman

# app = Flask(__name__)

# # Use Flask-Talisman for secure headers
# talisman = Talisman(app)

# # Initialize Flask-Limiter with in-memory storage
# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,  # Use the client's IP address as the key
#     default_limits=["200 per day", "50 per hour"]  # Default limits for all routes
# )

# SECRET_KEY = b')\xb7(<\xdd\xda\xed\x96\xb3\x1aHP^Ao\x10<\xd4\x16\x8c3\x04\xc9\xe0'

# # Ensure communication is over HTTPS and set up headers
# @app.before_request
# def enforce_https():
#     if not request.is_secure:
#         return jsonify({"error": "Connection must be over HTTPS"}), 400

# @app.route('/register', methods=['POST'])
# @limiter.limit("10 per minute")  # Limit to 10 requests per minute per IP
# def register():
#     # Get files from the request
#     file2 = request.files.get('file1')
#     file3 = request.files.get('file2')
#     org = request.files.get('org')

#     if not org:
#         return jsonify({'error': 'No file uploaded'}), 400

#     org.save(r'org.png')

#     # Save the files to disk
#     if file2:
#         file2.save(r'secret_2.png')
#     if file3:
#         file3.save(r'secret_3.png')

#     # Return a success message
#     return jsonify({'message': 'Files saved successfully'}), 200

# @app.route('/login', methods=['POST'])
# @limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
# def login():
#     file1 = request.files.get('file')
#     file2 = request.files.get('dec')

#     if not file1 or not file2:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file1.save(r'secret_1.png')
#     file2.save(r'restored.png')

#     image1 = cv2.imread(r'org.png')
#     image2 = cv2.imread(r'restored.png')

#     if image1 is None or image2 is None:
#         return jsonify({'error': 'Failed to load images'}), 400

#     mse = (np.mean((image1 - image2) ** 2) / (255 * 255))

#     return jsonify({"mse": mse}), 200

# # Error handler for rate limit exceeded
# @app.errorhandler(429)
# def ratelimit_handler(e):
#     return jsonify({
#         "error": "Rate limit exceeded",
#         "message": "You have exceeded the allowed request rate."
#     }), 429

# if __name__ == "__main__":
#     # Ensure your server uses SSL certificates
#     app.run(host='10.21.13.36', port=8000, ssl_context=('cert.pem', 'key.pem'))  # Use your actual SSL certificate and key paths
