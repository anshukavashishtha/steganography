import cv2
import os
import string

img = cv2.imread("photo.jpeg") #file path

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

height, width, _ = img.shape  

if len(msg) > height * width:
    print("Message too long for the image!")
    exit()

index = 0
for i in range(height):
    for j in range(width):
        if index < len(msg):
            img[i, j, 0] = ord(msg[index]) 
            index += 1

cv2.imwrite("encryptedImage.jpg", img)
os.system("open encryptedImage.jpg") 

message = ""
index = 0
pas = input("Enter passcode for Decryption: ")

if password == pas:
    for i in range(height):
        for j in range(width):
            if index < len(msg):
                message += chr(img[i, j, 0]) 
                index += 1
    print("Decryption message:", message)
else:
    print("YOU ARE NOT AUTHORIZED")
