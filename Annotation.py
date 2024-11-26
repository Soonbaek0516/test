# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:35:23 2024

@author: UOU
"""
import cv2
import numpy as np
import os

# Parameters for drawing
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates of the region

# List to store segmentation points
annotations = []

# Mouse callback function to draw contours
def draw_contour(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        annotations.append([(x, y)])  # Start a new contour

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Add points to the current contour
            annotations[-1].append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Close the contour by connecting the last point to the first
        annotations[-1].append((x, y))

# Function to save annotations as (x, y, h, w)
def save_annotations(image_path):
    annotation_file = os.path.splitext(image_path)[0] + "_annotations.txt"
    with open(annotation_file, "w") as f:
        for contour in annotations:
            points = np.array(contour, dtype=np.int32)
            x, y, w, h = cv2.boundingRect(points)  # Calculate bounding box
            f.write(f"{x}, {y}, {w}, {h}\n")  # Save as (x, y, w, h)
    print(f"Annotations saved to {annotation_file}")

# Function to display the image and collect annotations
def segment_image(image_path):
    global annotations
    # Reset annotations for each image
    annotations = []

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found: {image_path}")
        return False

    # Create a clone of the image for annotation display
    annotated_image = image.copy()
    cv2.namedWindow("Image Segmentation")
    cv2.setMouseCallback("Image Segmentation", draw_contour)

    while True:
        # Show the annotations on the cloned image
        temp_image = annotated_image.copy()
        for contour in annotations:
            points = np.array(contour, dtype=np.int32)
            x, y, w, h = cv2.boundingRect(points)
            # Draw the bounding box
            cv2.rectangle(temp_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the image with annotations
        cv2.imshow("Image Segmentation", temp_image)
        
        # Press 'n' to go to the next image, 's' to save, 'c' to clear, and 'q' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("n"):
            # Save annotations and proceed to next image
            save_annotations(image_path)
            break
        elif key == ord("s"):
            # Save annotations without proceeding
            save_annotations(image_path)
        elif key == ord("c"):
            # Clear annotations
            annotations.clear()
            annotated_image = image.copy()
            print("Annotations cleared")
        elif key == ord("q"):
            cv2.destroyAllWindows()
            return False

    cv2.destroyAllWindows()
    return True

# Function to process multiple images
def process_images(image_folder):
    # Get list of image files in the folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    if not image_files:
        print("No images found in the folder!")
        return

    for image_file in image_files:
        print(f"Processing: {image_file}")
        if not segment_image(image_file):
            print("Exiting segmentation tool.")
            break

# Example usage
if __name__ == "__main__":
    image_folder = r"C:/Users/cic/Desktop/kimjw/DEC20_t/image file"
    process_images(image_folder)
