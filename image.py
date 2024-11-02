import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Lists to store calibration data
calibration_concentrations = []
calibration_intensities = []

def analyze_image(image_path, concentration):
    """
    This function loads an image, extracts the color intensity from the blue channel,
    and saves the intensity-concentration pair for calibration.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error loading image. Please check the file path.")
        return

    # Convert to the blue channel (index 0 in OpenCV BGR format)
    blue_channel = image[:, :, 0]

    # Define a Region of Interest (ROI) for intensity measurement
    # You might adjust these values based on the sample layout in your images
    roi_x, roi_y, roi_w, roi_h = 50, 50, 100, 100  # Example coordinates, customize as needed
    roi = blue_channel[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

    # Calculate mean intensity of the ROI
    mean_intensity = np.mean(roi)
    
    # Store the concentration-intensity pair
    calibration_concentrations.append(concentration)
    calibration_intensities.append(mean_intensity)

    print(f"Image analyzed. Mean Intensity: {mean_intensity:.2f} for concentration {concentration} µg/mL")

def plot_calibration_curve():
    """
    This function creates a calibration curve using the stored concentration-intensity pairs.
    It fits a linear regression model and plots the curve.
    """
    if len(calibration_concentrations) < 2:
        print("Need at least two data points to plot calibration curve.")
        return

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(calibration_intensities, calibration_concentrations)

    # Predict concentrations based on fitted model
    predicted_concentrations = [slope * i + intercept for i in calibration_intensities]

    # Plot the calibration curve
    plt.figure(figsize=(8, 6))
    plt.plot(calibration_intensities, calibration_concentrations, 'bo', label="Calibration Data")
    plt.plot(calibration_intensities, predicted_concentrations, 'r-', label=f"Fit: Concentration = {slope:.2f} * Intensity + {intercept:.2f}")
    plt.xlabel("Color Intensity (Blue Channel Mean)")
    plt.ylabel("Concentration (µg/mL)")
    plt.title("Calibration Curve: Intensity vs Concentration")
    plt.legend()
    plt.grid(True)
    plt.show()

# Main Loop for User Input
while True:
    image_path = input("Enter the path of the image file (or type 'done' to finish): ")
    if image_path.lower() == 'done':
        break
    
    try:
        concentration = float(input("Enter the known concentration for this image (e.g., in µg/mL): "))
    except ValueError:
        print("Invalid concentration value. Please enter a numerical value.")
        continue

    analyze_image(image_path, concentration)

# Plot the calibration curve once all images have been processed
plot_calibration_curve()
