import cv2
import numpy as np
import random
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from shamir import * 
import subprocess 

def add_watermark(image, text):
    height, width, _ = image.shape
    font_types = [
        cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_DUPLEX,
        cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_TRIPLEX, cv2.FONT_HERSHEY_COMPLEX_SMALL,
        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    ]
    for char in text:
        org = (random.randint(0, width - 1), random.randint(0, height - 1))
        font = random.choice(font_types)
        font_scale = random.uniform(0.5, 2.0)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        thickness = random.randint(1, 3)
        cv2.putText(image, char, org, font, font_scale, color, thickness, cv2.LINE_AA)
    return image


# Main function
def main():
    # Load the original image
    image = cv2.imread('samp.jpg')
    if image is None:
        print("Error: Image not found.")
        return

    user_details = "Aniruth 8825842250 aniruths10@gmail.com " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    watermarked_image = add_watermark(image.copy(), user_details)

    cv2.imwrite('wat.png' , watermarked_image )

    command1 = ['python', 'Shamir.py', '-e', 'wat.png', '-n', '3', '-r', '2']

    result = subprocess.run(command1)

    key = os.urandom(32)

    command2 = ['python', 'Shamir.py', '-d', 'recondfkj.png', '-r', '2', '-i', '1' ,  '2']

    result = subprocess.run(command2)

    print("Testing with valid shares:")
    try:
        command3 = ['python' , 'Shamir.py' , '-c' , 'wat.png' , 'recondfkj.png']

        result = subprocess.run(command3)


    except Exception as e:
        print(f"An error occurred during reconstruction: {e}")

main()