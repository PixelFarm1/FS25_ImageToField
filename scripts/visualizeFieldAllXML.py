import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import random

def parse_all_field_coordinates_with_center_flipped_plane(file_path):
    """
    Parse the XML file to extract coordinates for all fields with respect to their center,
    flipping the entire Y-plane while preserving polygon orientation.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    fields = {}
    centers = {}
    for field in root.findall("Field"):
        field_id = field.attrib.get("ID")
        center_x = float(field.attrib.get("X"))
        center_y = -float(field.attrib.get("Y"))  # Flip the Y-plane for the center

        coordinates = [
            (center_x + float(coord.attrib["X"]), center_y - float(coord.attrib["Y"]))  # Flip Y-plane for center and coords
            for coord in field.findall("coordinate")
        ]
        fields[field_id] = coordinates
        centers[field_id] = (center_x, center_y)
    return fields, centers

def visualize_all_fields_with_labels(file_path):
    """
    Visualize the coordinates of all fields relative to their center, each in a unique color,
    with the entire Y-plane flipped and polygon orientation preserved. Field centers are labeled with IDs.
    """
    fields, centers = parse_all_field_coordinates_with_center_flipped_plane(file_path)
    plt.figure(figsize=(12, 12))
    
    for field_id, coords in fields.items():
        # Generate a random color for each field
        color = [random.random() for _ in range(3)]
        x, y = zip(*coords)
        plt.plot(x, y, label=f"Field {field_id}", color="black")
        # Mark the center point of the field and label it
        center_x, center_y = centers[field_id]
        #plt.scatter(center_x, center_y, color=color, edgecolor='black', zorder=5)
        plt.text(center_x, center_y, f"ID {field_id}", fontsize=9, ha='center', va='center', zorder=10)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate (Flipped Plane, Preserved Orientation)")
    plt.title("Visualization of All Fields with Flipped Y-Plane and Labels")
    plt.grid(True)
    plt.show()

# Path to the XML file
file_path = 'C:/Users/Willis/Desktop/FS25_ImageToField/FS25_ImageToField/output/final_field_coordinates.xml'

# Generate the visualization
visualize_all_fields_with_labels(file_path)
