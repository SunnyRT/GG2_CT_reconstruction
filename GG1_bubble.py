import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def is_majority_red(image, mask, threshold=0.25):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2
    red_pixels = cv2.bitwise_and(red_mask, red_mask, mask=mask)
    red_area = np.sum(red_pixels > 0)
    total_area = np.sum(mask > 0)
    if total_area == 0:
        return False
    return red_area / total_area > threshold

def calculate_ellipse_area(ellipse):
    _, (MA, ma), _ = ellipse
    return np.pi * (MA / 2) * (ma / 2)

def is_majority_black(image, mask, threshold=0.5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, black_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    black_pixels = cv2.bitwise_and(black_mask, black_mask, mask=mask)
    black_area = np.sum(black_pixels > 0)
    total_area = np.sum(mask > 0)
    if total_area == 0:
        return False
    return black_area / total_area > threshold

def process_image(file_path, area_threshold=100, color_threshold=0.25, expansion_factor=1.2):
    img = cv2.imread(file_path)
    if img is None:
        print(f"Error: Unable to read image file {file_path}")
        return [], []
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 | mask2
    
    kernel = np.ones((5, 5), np.uint8)
    red_mask_cleaned = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(red_mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    inner_areas = []
    outer_areas = []
    outer_ellipses = []
    
    for contour in contours:
        if cv2.contourArea(contour) > area_threshold:
            if len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                
                mask = np.zeros_like(gray)
                cv2.ellipse(mask, ellipse, 255, -1)
                
                if is_majority_red(img, mask, color_threshold):
                    cv2.ellipse(img, ellipse, (255, 0, 0), 2)  # Blue color for inner ellipse
                    inner_areas.append(calculate_ellipse_area(ellipse))
                    
                    (x, y), (MA, ma), angle = ellipse
                    outer_center = (int(x), int(y))
                    outer_axes = (int(MA * expansion_factor / 2), int(ma * expansion_factor / 2))
                    
                    mask = np.zeros_like(gray)
                    cv2.ellipse(mask, (outer_center, outer_axes, angle), 255, -1)
                    
                    while not is_majority_black(img, mask, 0.25) and outer_axes[0] > MA / 2 and outer_axes[1] > ma / 2:
                        outer_axes = (outer_axes[0] + 2, outer_axes[1] + 2)  # Increase by 2 pixels each iteration
                        mask = np.zeros_like(gray)
                        cv2.ellipse(mask, (outer_center, outer_axes, angle), 255, -1)
                    
                    # Ensure the outer ellipse contains the inner ellipse and does not overlap with other objects
                    valid_outer = True
                    for existing_outer in outer_ellipses:
                        dist = np.linalg.norm(np.array(existing_outer[0]) - np.array(outer_center))
                        if dist < (existing_outer[1][0] + outer_axes[0]) / 2:
                            valid_outer = False
                            break
                    
                    if valid_outer:
                        cv2.ellipse(img, outer_center, outer_axes, angle, 0, 360, (0, 255, 0), 2)  # Green color for outer ellipse
                        outer_area = np.pi * outer_axes[0] * outer_axes[1]
                        outer_areas.append(outer_area)
                        outer_ellipses.append((outer_center, outer_axes))
    
    # Detect edges using Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours from the detected edges
    edge_contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for edge_contour in edge_contours:
        if cv2.contourArea(edge_contour) > area_threshold:
            if len(edge_contour) >= 5:
                cv2.drawContours(img, [edge_contour], -1, (0, 0, 255), 2)  # Blue color for separation contour
    
    # Display the image with ellipses and contours
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Ellipses in {os.path.basename(file_path)}")
    plt.show()
    
    return inner_areas, outer_areas

# Directory containing the images
directory = '/Users/tonganze/Desktop/Cam IIA/GG1/Bubbles'

# Process each image file in the directory
all_inner_areas = []
all_outer_areas = []

for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Add more extensions if needed
        file_path = os.path.join(directory, filename)
        inner_areas, outer_areas = process_image(file_path, area_threshold=100, color_threshold=0.25)
        all_inner_areas.extend(inner_areas)
        all_outer_areas.extend(outer_areas)
        
        # Calculate statistics for each image
        if inner_areas:
            avg_inner_area = np.mean(inner_areas)
            std_inner_area = np.std(inner_areas)
            print(f"Image: {filename}")
            print(f"Number of bubbles: {len(inner_areas)}")
            print(f"Areas of bubbles: {[f'{area:.3f}' for area in inner_areas]}")
            print(f"Average inner ellipse area: {avg_inner_area:.3f}")
            print(f"Standard deviation of inner ellipse areas: {std_inner_area:.3f}")
            print()
        else:
            print(f"Image: {filename}")
            print("No inner ellipses detected")
            print()

        if outer_areas:
            avg_outer_area = np.mean(outer_areas)
            std_outer_area = np.std(outer_areas)
            print(f"Image: {filename}")
            print(f"Number of outer ellipses: {len(outer_areas)}")
            print(f"Areas of outer ellipses: {[f'{area:.3f}' for area in outer_areas]}")
            print(f"Average outer ellipse area: {avg_outer_area:.3f}")
            print(f"Standard deviation of outer ellipse areas: {std_outer_area:.3f}")
            print()
        else:
            print(f"Image: {filename}")
            print("No outer ellipses detected")
            print()

# Calculate and print average areas for all images
if all_inner_areas:
    avg_inner_area = np.mean(all_inner_areas)
    std_inner_area = np.std(all_inner_areas)
    print(f"Overall average inner ellipse area: {avg_inner_area:.3f}")
    print(f"Overall standard deviation of inner ellipse areas: {std_inner_area:.3f}")
else:
    print("No inner ellipses detected in any image")

if all_outer_areas:
    avg_outer_area = np.mean(all_outer_areas)
    std_outer_area = np.std(all_outer_areas)
    print(f"Overall average outer ellipse area: {avg_outer_area:.3f}")
    print(f"Overall standard deviation of outer ellipse areas: {std_outer_area:.3f}")
else:
    print("No outer ellipses detected in any image")
