import cv2
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# 🔹 Fixed Image Path (Change if needed)
img_path = "/Users/anshukavashishtha/Desktop/photo.jpeg"  

# 🔹 GUI Setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x500")

# 🔹 Function to Load Fixed Image
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

# 🔹 Function to Encrypt Message
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
                img[i, j, 0] = ord(msg[index])  # Store ASCII in Blue channel
                index += 1

    cv2.imwrite("encryptedImage.jpg", img)
    os.system("open encryptedImage.jpg")  # Open image on Mac
    messagebox.showinfo("Success", "Message encrypted & saved as encryptedImage.jpg")

# 🔹 Function to Decrypt Message
def decrypt_message():
    global img_path
    img = cv2.imread("encryptedImage.jpg")  # Read the encrypted image
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
                message += chr(img[i, j, 0])  # Convert ASCII back to text
                index += 1

    messagebox.showinfo("Decryption Successful", f"Decrypted Message: {message}")

# 🔹 GUI Layout
img_label = tk.Label(root, text="Loading image...", bg="gray", width=40, height=10)
img_label.pack(pady=10)

load_fixed_image()  # Load image at startup

tk.Label(root, text="Enter Secret Message:").pack()
entry_message = tk.Entry(root, width=40)
entry_message.pack()

tk.Label(root, text="Enter Password:").pack()
entry_password = tk.Entry(root, width=40, show="*")  # Password input
entry_password.pack()

btn_encrypt = tk.Button(root, text="Encrypt", command=encrypt_message)
btn_encrypt.pack(pady=5)

btn_decrypt = tk.Button(root, text="Decrypt", command=decrypt_message)
btn_decrypt.pack(pady=5)

root.mainloop()
