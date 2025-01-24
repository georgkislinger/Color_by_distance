# README: Colormap Application and Distance Mapping Scripts

DISCLAIMER: This README is AI-generated and may contain errors.
This repository contains two Python scripts designed for electron microscopy (EM) data processing. These scripts focus on applying colormaps to EM data and generating distance-based visualizations for enhanced analysis. Below is a comprehensive guide to setting up the environment and using these scripts effectively.

---

## Table of Contents
1. [Overview](#overview)
2. [Environment Setup](#environment-setup)
3. [Script Descriptions](#script-descriptions)
4. [How to Use](#how-to-use)
    - [Script 1: Apply Colormap to EM Images](#apply-colormap-to-em-images)
    - [Script 2: Generate Distance-Based Colormap](#generate-distance-based-colormap)
    - [Script 3: Color Vertices by Distance in Blender](#color-vertices-by-distance-in-blender)
5. [Troubleshooting](#troubleshooting)

---

## Overview
The repository includes:
- **`apply_colormap_to_EM.py`**: Overlays a colormap mask onto raw EM grayscale images.
- **`color_by_distance_2D.py`**: Creates a distance-based colormap from segmentation data, with an optional scale bar for visualization.
- **`Color_by_distance_Blender.py`**: Colors the vertices of a Blender object based on their distances to another object.

These tools are useful for creating visually intuitive overlays for microscopy data, making it easier to interpret segmentation results and analyze spatial distributions.

---

## Environment Setup

### Prerequisites
- Python 3.8+
- A machine with OpenCV and NumPy support.
- Blender 2.8 or higher (for the Blender script).

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scriptsctivate    # Windows
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies
These scripts require the following Python libraries:
- `numpy`
- `opencv-python`
- `matplotlib`
- `scipy`
- `tqdm`

To install them manually, use:
```bash
pip install numpy opencv-python matplotlib scipy tqdm
```

---

## Script Descriptions

### 1. `apply_colormap_to_EM.py`
This script overlays a colormap on grayscale EM images based on an RGBA mask. It supports automatic resizing of the mask to match the dimensions of the raw images.

**Inputs:**
- Folder of raw grayscale images.
- Folder of RGBA colormap masks.

**Outputs:**
- Folder of processed images with the colormap applied.

### 2. `color_by_distance_2D.py`
This script computes a distance transform from segmentation masks and generates a colormap representing the distance to the nearest segmentation boundary. It also provides an option to create a scale bar for the distance map.

**Inputs:**
- Folder of grayscale segmentation images.
- Distance in physical units per pixel.

**Outputs:**
- Folder of distance-based colormap images.
- Scale bar image (optional).

### 3. `Color_by_distance_Blender.py`
This Blender script colors the vertices of a mesh object based on their distances to another object in the scene. It uses KDTree algorithms for efficient distance computation and assigns vertex colors accordingly.

**Inputs:**
- Two objects in a Blender scene: a source object and a target object.

**Outputs:**
- Vertex colors applied to the source object, representing their distance to the target object.

---

## How to Use

### Apply Colormap to EM Images
1. Edit the script parameters:
   Open `apply_colormap_to_EM.py` and update the following variables to match your data paths:
   ```python
   input_image_folder = r"<path-to-raw-images>"
   input_mask_folder = r"<path-to-mask-images>"
   output_folder = r"<path-to-output-folder>"
   input_image_template = "<raw-image-template>"
   input_mask_template = "<mask-image-template>"
   output_template = "<output-image-template>"
   ```
2. Run the script:
   ```bash
   python apply_colormap_to_EM.py
   ```
3. Check the `output_folder` for processed images.

### Generate Distance-Based Colormap
1. Edit the script parameters:
   Open `color_by_distance_2D.py` and update the following variables:
   ```python
   input_folder = r"<path-to-segmentation-images>"
   output_folder = r"<path-to-output-folder>"
   pixel_size = <physical-size-per-pixel>
   segmentation_value = <segmentation-gray-value>
   ```
2. Run the script:
   ```bash
   python color_by_distance_2D.py
   ```
3. Check the `output_folder` for colormap images and scale bar.

### Color Vertices by Distance in Blender
1. Open Blender and load your scene with the source and target objects.
2. Install the script:
   - Open the Scripting tab in Blender.
   - Create a new script or load `Color_by_distance_Blender.py`.
   - Run the script by clicking **Run Script**.
3. Follow the script's instructions to:
   - Select the source object (whose vertices will be colored).
   - Select the target object (to compute distances).
4. Check the Vertex Paint mode of the source object to view the applied vertex colors.

---

## Troubleshooting

### Common Issues
1. **Input files not found:**
   Ensure the file paths and templates are correct.

2. **Output folder not created:**
   Verify you have write permissions for the specified directory.

3. **Dependencies missing:**
   Double-check that all required Python packages are installed.

### Debugging
Add print statements or use a debugger (e.g., `pdb`) to identify issues in the code.

---

This README should help you get started with the scripts and adapt them for your specific use case. If you encounter issues or have suggestions for improvement, feel free to reach out.
