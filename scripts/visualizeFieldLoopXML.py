import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import argparse

def parse_field_coordinates(file_path, field_id):
    """
    Parse the XML file to extract coordinates for a specific field ID.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    for field in root.findall("Field"):
        if field.attrib.get("ID") == field_id:
            loops = []
            for loop in field.findall("Loop"):
                coordinates = [
                    (float(coord.attrib["X"]), float(coord.attrib["Y"]))
                    for coord in loop.findall("coordinate")
                ]
                loops.append(coordinates)
            return loops
    return None

def visualize_coordinates(loops, field_id):
    """
    Visualize the coordinates of the given loops.
    """
    plt.figure(figsize=(10, 8))
    for loop in loops:
        x, y = zip(*loop)
        plt.plot(x, y, label=f"Loop in Field {field_id}")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title(f"Visualization of Field ID: {field_id}")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Visualize field loops from XML.")
    parser.add_argument("file", help="Path to the XML file.")
    parser.add_argument("field_id", help="Field ID to visualize.")
    args = parser.parse_args()

    loops = parse_field_coordinates(args.file, args.field_id)
    if loops:
        visualize_coordinates(loops, args.field_id)
    else:
        print(f"No data found for Field ID: {args.field_id}")

if __name__ == "__main__":
    main()
