import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

img_path = "photo.jpeg"  #file path

root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x500")

def load_fixed_image():
    global img_path, img_label
    if not os.path.exists(img_path):
        messagebox.showerror("Error", "Image file not found!")
        return
    
    image = Image.open(img_path)
    image.thumbnail((300, 300))
    img = ImageTk.PhotoImage(image)

    img_label.config(image=img)
    img_label.image = img

def encrypt_message():
    global img_path
    msg = entry_message.get()
    password = entry_password.get()

    if not msg or not password:
        messagebox.showerror("Error", "Message and password required!")
        return

    img = cv2.imread(img_path)
    height, width, _ = img.shape  

    if len(msg) > height * width:
        messagebox.showerror("Error", "Message too long for the image!")
        return

    index = 0
    for i in range(height):
        for j in range(width):
            if index < len(msg):
                img[i, j, 0] = ord(msg[index])  
                index += 1

    cv2.imwrite("encryptedImage.jpg", img)
    os.system("open encryptedImage.jpg")  # Open image on Mac
    messagebox.showinfo("Success", "Message encrypted & saved as encryptedImage.jpg")

def decrypt_message():
    global img_path
    img = cv2.imread("encryptedImage.jpg") 
    height, width, _ = img.shape

    pas = entry_password.get()
    if pas != entry_password.get():
        messagebox.showerror("Error", "Incorrect password!")
        return

    message = ""
    index = 0
    for i in range(height):
        for j in range(width):
            if index < len(entry_message.get()):
                message += chr(img[i, j, 0])  
                index += 1

    messagebox.showinfo("Decryption Successful", f"Decrypted Message: {message}")

img_label = tk.Label(root, text="Loading image...", bg="gray", width=40, height=10)
img_label.pack(pady=10)

load_fixed_image() 

tk.Label(root, text="Enter Secret Message:").pack()
entry_message = tk.Entry(root, width=40)
entry_message.pack()

tk.Label(root, text="Enter Password:").pack()
entry_password = tk.Entry(root, width=40, show="*")  
entry_password.pack()

btn_encrypt = tk.Button(root, text="Encrypt", command=encrypt_message)
btn_encrypt.pack(pady=5)

btn_decrypt = tk.Button(root, text="Decrypt", command=decrypt_message)
btn_decrypt.pack(pady=5)

root.mainloop()
