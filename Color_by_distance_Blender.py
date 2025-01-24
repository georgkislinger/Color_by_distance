import bpy
import bmesh
import numpy as np
from mathutils import kdtree

def sample_distances(obj_a, obj_b):
    """Calculate distances from vertices of obj_a to the nearest vertex of obj_b."""
    # Ensure both objects have meshes
    if obj_a.type != 'MESH' or obj_b.type != 'MESH':
        print("Both objects must be meshes")
        return None

    # Get the vertex coordinates of both objects
    mesh_a = obj_a.data
    mesh_b = obj_b.data

    # Convert obj_b's vertices to KDTree for nearest neighbor search
    kd = kdtree.KDTree(len(mesh_b.vertices))
    for i, vert in enumerate(mesh_b.vertices):
        kd.insert(obj_b.matrix_world @ vert.co, i)  # Transform to world coordinates
    kd.balance()

    # Calculate distances for each vertex of obj_a
    distances = np.zeros(len(mesh_a.vertices))
    for i, vert in enumerate(mesh_a.vertices):
        co_world = obj_a.matrix_world @ vert.co  # Transform to world coordinates
        loc, index, dist = kd.find(co_world)  # Find the nearest vertex in obj_b
        distances[i] = dist

    print(f"Distance calculation complete. Total vertices: {len(distances)}")
    return distances

def hex_to_rgba(hex_color):
    """Convert a hex color to an RGBA tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

def interpolate_color(color_start, color_end, factor):
    """Linearly interpolate between two RGBA colors."""
    return tuple((1 - factor) * cs + factor * ce for cs, ce in zip(color_start, color_end))

def apply_color_ramp(obj_a, distances, min_dist, max_dist, color_start, color_end, col_name):
    """Apply a color ramp to the object based on distances."""
    mesh = obj_a.data

    # Normalize distances to range [0, 1]
    normalized_distances = (distances - min_dist) / (max_dist - min_dist)
    normalized_distances = np.clip(normalized_distances, 0, 1)

    # Create or use the specified vertex color layer
    if col_name not in mesh.vertex_colors:
        mesh.vertex_colors.new(name=col_name)
    
    color_layer = mesh.vertex_colors[col_name]

    # Apply color ramp
    for poly in mesh.polygons:
        for loop_index in poly.loop_indices:
            loop = mesh.loops[loop_index]
            vert_idx = loop.vertex_index
            factor = normalized_distances[vert_idx]
            color = interpolate_color(color_start, color_end, factor)
            color_layer.data[loop_index].color = color

    mesh.update()

def generate_col_name(min_dist, max_dist, color_start, color_end):
    """Generate a descriptive name for the vertex color layer."""
    return f"{min_dist:.2f}m-{max_dist:.2f}m-{color_start[0]:.0f}%orange_to_{color_end[0]:.0f}%purple"

def main():
    # Define objects
    obj_a = bpy.context.scene.objects['Cube.002']  # Object to be colored
    obj_b = bpy.context.scene.objects['Cube.001']       # Reference object

    # Step 1: Calculate distances and store in the "Col" vertex color layer
    distances = sample_distances(obj_a, obj_b)
    if distances is None:
        return

    # Print the actual distance range
    actual_min = distances.min()
    actual_max = distances.max()
    print(f"Actual distance range: min = {actual_min:.2f}, max = {actual_max:.2f}")

    # Define color ramp (purple to orange gradient)
    color_start = hex_to_rgba('#FFA500')  # Orange
    color_end = hex_to_rgba('#800080')    # Purple

    # Define thresholds for color ramps
    thresholds = [
        (0, actual_max * 0.3),
        (actual_max * 0.25, actual_max * 0.5),
        (actual_max * 0.2, actual_max * 0.4),
        (actual_max * 0.1, actual_max * 0.7),
        (actual_max * 0.6, actual_max * 0.8),
        (actual_max * 0.75, actual_max),
    ]

    # Apply multiple color ramps
    for min_dist, max_dist in thresholds:
        col_name = generate_col_name(min_dist, max_dist, color_start, color_end)
        print(f"Applying color ramp: {col_name} (min = {min_dist:.2f}, max = {max_dist:.2f})")
        apply_color_ramp(obj_a, distances, min_dist, max_dist, color_start, color_end, col_name)

# Run the script
main()
