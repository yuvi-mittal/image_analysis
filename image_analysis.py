import numpy
import cv2
import matplotlib
import scipy

print("All libraries are installed and ready to use.")


print("Starting the image analysis script...")  # Add this at the beginning
while True:
    print("Waiting for user input...")  # Add this line
    image_path = input("Enter the path of the image file (or type 'done' to finish): ")
    if image_path.lower() == 'done':
        break
    
    try:
        concentration = float(input("Enter the known concentration for this image (e.g., in µg/mL): "))
    except ValueError:
        print("Invalid concentration value. Please enter a numerical value.")
        continue
