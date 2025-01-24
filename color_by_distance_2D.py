import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt
from matplotlib.colors import LinearSegmentedColormap
import cv2
import os
from tqdm import tqdm

# Function to convert hex color to RGBA
def hex_to_rgba(hex_color, alpha=0.2):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (alpha,)

# Define start, end, and intermediate colors for colormap using hex codes
colors_and_distances = [
    (hex_to_rgba("#009600", 0.2), 0),    # Green at 0 microns
    (hex_to_rgba("#4C4CB5", 0.2), 10),   # Blue-purple at 10 microns
    (hex_to_rgba("#960000", 0.2), 20)   # Dark red at 20 microns
]

# Function to create a continuous colormap with specified distances for colors
def create_distance_colormap(colors_and_distances):
    colors, distances = zip(*colors_and_distances)
    max_distance = max(distances)
    distances_normalized = [d / max_distance for d in distances]
    return LinearSegmentedColormap.from_list("distance_colormap", list(zip(distances_normalized, colors)))

# Function to create and save distance maps
def create_distance_map(input_folder, output_folder, colormap, pixel_size, segmentation_value):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, filename in enumerate(tqdm(os.listdir(input_folder), desc="Processing images")):
        if filename.endswith(".png") or filename.endswith(".tif"):
            filepath = os.path.join(input_folder, filename)
            segmentation = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

            # Create binary mask based on segmentation value
            binary_segmentation = segmentation == segmentation_value

            # Compute distance transform in physical units
            distances = distance_transform_edt(~binary_segmentation) * pixel_size

            # Exclude distances inside the segmentation area
            distances[binary_segmentation] = np.nan

            # Normalize distances and apply colormap
            max_distance = max(d for _, d in colors_and_distances)
            normalized_distances = np.clip(distances / max_distance, 0, 1)
            colored_map = colormap(normalized_distances)

            # Set areas inside the segmentation to be fully transparent
            colored_map[np.isnan(distances)] = [0, 0, 0, 0]

            # Convert RGBA to BGRA and normalize for saving
            colored_map_uint8 = (colored_map * 255).astype(np.uint8)

            # Save the result
            output_path = os.path.join(output_folder, f"CbD_mask_{i:04d}.png")
            cv2.imwrite(output_path, cv2.cvtColor(colored_map_uint8, cv2.COLOR_RGBA2BGRA))

# Function to create a scale bar that adapts to the colormap
def create_scale_bar(output_folder, colormap, max_distance, pixel_size, scale_bar_height=50, image_width=600):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Add padding to the image for labels
    padding = 50  # Extra space for labels
    usable_width = image_width - 2 * padding
    scale_bar_pixels = usable_width

    # Create the gradient for the scale bar
    gradient = np.linspace(0, 1, scale_bar_pixels)
    scale_bar = colormap(gradient).reshape(1, -1, 4)
    scale_bar_image = np.tile(scale_bar, (scale_bar_height, 1, 1))

    # Create a new image with padding for labels
    padded_image = np.ones((scale_bar_height + padding, image_width, 4), dtype=np.float32)
    padded_image[:, :, :3] = 1  # Set transparent background
    padded_image[:scale_bar_height, padding:padding + scale_bar_image.shape[1]] = scale_bar_image

    # Add ticks and labels
    ticks = np.array([d for _, d in colors_and_distances])
    tick_positions = (ticks / max_distance * usable_width).astype(int) + padding
    for idx, tick in enumerate(ticks):
        cv2.line(padded_image, (tick_positions[idx], scale_bar_height), (tick_positions[idx], scale_bar_height + 10), (0, 0, 0, 1), 1)
        cv2.putText(padded_image, f"{int(tick)} um", (tick_positions[idx] - 20, scale_bar_height + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0, 1), 1, cv2.LINE_AA)

    # Add total length label
    cv2.putText(padded_image, f"{max_distance} um", (image_width - padding - 60, scale_bar_height + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0, 1), 1, cv2.LINE_AA)

    # Convert to uint8 and save
    scale_bar_uint8 = (padded_image * 255).astype(np.uint8)
    scale_bar_path = os.path.join(output_folder, "scale_bar.png")
    cv2.imwrite(scale_bar_path, cv2.cvtColor(scale_bar_uint8, cv2.COLOR_RGBA2BGRA))

# Define parameters
input_folder = r"\\DZNE-MU-208\shared_drive\Misgeld_notch_bv-seg_mip2_8bit"
output_folder = r"\\DZNE-MU-208\shared_drive\notch_50x50x200_final\seg\CbD_colormap"
pixel_size = 0.2  # Physical size of a pixel in microns
segmentation_value = 191  # Grey value representing the segmentation

# Create and apply the colormap
colormap = create_distance_colormap(colors_and_distances)
create_distance_map(input_folder, output_folder, colormap, pixel_size, segmentation_value)

# Create the scale bar image
max_distance = max(d for _, d in colors_and_distances)
create_scale_bar(output_folder, colormap, max_distance, pixel_size)
