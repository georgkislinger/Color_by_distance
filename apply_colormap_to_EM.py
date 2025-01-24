import numpy as np
import cv2
import os
from tqdm import tqdm

# Define the function to overlay colormap on raw data
def overlay_colormap_on_raw(input_image_folder, input_mask_folder, output_folder,
                            input_image_template, input_mask_template, output_template,
                            upscale_mask=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in tqdm(range(len(os.listdir(input_image_folder))), desc="Processing images"):
        # Paths for input image and mask
        image_path = os.path.join(input_image_folder, input_image_template % i)
        mask_path = os.path.join(input_mask_folder, input_mask_template % i)

        # Ensure both files exist
        if not os.path.exists(image_path) or not os.path.exists(mask_path):
            continue

        # Load raw image (grayscale) and mask (RGBA)
        raw_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel

        # Determine scale factors
        raw_h, raw_w = raw_image.shape
        mask_h, mask_w = mask.shape[:2]

        if upscale_mask:
            scale_factor = (raw_w // mask_w, raw_h // mask_h)
        else:
            scale_factor = (mask_w // raw_w, mask_h // raw_h)

        # Resize the mask if needed
        if upscale_mask:
            resized_mask = cv2.resize(mask, (raw_w, raw_h), interpolation=cv2.INTER_NEAREST)
        else:
            resized_mask = cv2.resize(mask, (mask_w // scale_factor[0], mask_h // scale_factor[1]), interpolation=cv2.INTER_NEAREST)

        # Extract the alpha channel for masking
        alpha = resized_mask[:, :, 3] / 255.0  # Normalize alpha channel

        # Convert mask to RGB format for overlay (avoid reordering to BGR)
        mask_rgb = resized_mask[:, :, :3]

        # Initialize the output overlay as the raw image
        overlay = np.repeat(raw_image[:, :, None], 3, axis=2).astype(np.float32)

        # Apply mask only where raw image is not black
        non_black_mask = raw_image > 0
        overlay[non_black_mask] = (
            overlay[non_black_mask] * (1 - alpha[non_black_mask][:, None]) +
            mask_rgb[non_black_mask] * alpha[non_black_mask][:, None]
        )

        # Clip to valid range and convert to uint8
        overlay = np.clip(overlay, 0, 255).astype(np.uint8)

        # Save the output
        output_path = os.path.join(output_folder, output_template % i)
        cv2.imwrite(output_path, overlay)

# Define parameters
input_image_folder = r"\\DZNE-MU-208\shared_drive\notch_50x50x200_final\img\mip2"
input_mask_folder = r"\\DZNE-MU-208\shared_drive\notch_50x50x200_final\seg\CbD_colormap_2"
output_folder = r"\\DZNE-MU-208\shared_drive\notch_50x50x200_final\seg\CbD_on_EM_2"
input_image_template = "mip2_%04d.tif"
input_mask_template = "CbD_mask_%04d.png"
output_template = "CbD_EM_%04d.png"

# Run the overlay function
overlay_colormap_on_raw(input_image_folder, input_mask_folder, output_folder,
                        input_image_template, input_mask_template, output_template,
                        upscale_mask=True)
