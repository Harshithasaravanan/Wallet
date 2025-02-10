import cv2
import numpy as np
import random
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import os
import requests
from datetime import datetime

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

def register():
    name = simpledialog.askstring("Registration", "Enter your name:")
    phone = simpledialog.askstring("Registration", "Enter your phone:")
    email = simpledialog.askstring("Registration", "Enter your email:")
    
    image_path = filedialog.askopenfilename()
    if not image_path:
        messagebox.showerror("Error", "No image selected.")
        return
    
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Image could not be loaded.")
        return
    
    user_details = f"{name} {phone} {email} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    watermarked_image = add_watermark(image.copy(), user_details)
    cv2.imwrite('Water_Marked_img.png', watermarked_image)
    
    files = {'file': open('wat.png', 'rb')}
    response = requests.post("http://localhost:5000/register", files=files)
    messagebox.showinfo("Response", response.text)

def login():
    share_path = filedialog.askopenfilename()
    if not share_path:
        messagebox.showerror("Error", "No share selected.")
        return
    
    files = {'file': open(share_path, 'rb')}
    response = requests.post("http://localhost:5000/login", files=files)
    messagebox.showinfo("Response", response.text)
    
app = tk.Tk()
app.title("User Authentication")

tk.Button(app, text="Register", command=register).pack(pady=10)
tk.Button(app, text="Login", command=login).pack(pady=10)
app.mainloop()
