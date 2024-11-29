import xml.etree.ElementTree as ET
import math
import os

class MarkFieldLoops:
    def process(self, input_file, output_dir):
        """
        Marks and processes field loops in the input XML file.
        
        Args:
            input_file (str): Path to the input XML file.
            output_dir (str): Directory to save the processed XML file.
        
        Returns:
            str: Path to the saved processed XML file.
        """
        def calculate_distance(x1, y1, x2, y2):
            """Calculate Euclidean distance between two points."""
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        def process_field(field):
            """Process a single field and mark the loops."""
            x_attr = field.attrib.get("X", "0")  # Preserve X attribute
            y_attr = field.attrib.get("Y", "0")  # Preserve Y attribute
            
            loops = field.findall("Loop")
            main_loop = [
                (float(coord.attrib["X"]), float(coord.attrib["Y"]))
                for coord in loops[0].findall("coordinate")
            ]
            
            print(f"Processing Field ID: {field.attrib['ID']}, Main Loop has {len(main_loop)} coordinates.")
            
            for loop in loops[1:]:
                other_coords = [
                    (float(coord.attrib["X"]), float(coord.attrib["Y"]))
                    for coord in loop.findall("coordinate")
                ]
                
                # Find the closest coordinate in the main loop
                min_distance = float("inf")
                min_main_index = -1
                min_other_index = -1
                
                for main_index, (main_x, main_y) in enumerate(main_loop):
                    for other_index, (other_x, other_y) in enumerate(other_coords):
                        distance = calculate_distance(main_x, main_y, other_x, other_y)
                        if distance < min_distance:
                            min_distance = distance
                            min_main_index = main_index
                            min_other_index = other_index
                
                # Mark the closest coordinate in the main loop
                merge_id = loop.attrib["ID"]
                main_coord = loops[0].findall("coordinate")[min_main_index]
                main_coord.set("mergeID", merge_id)
                
                print(f"Marking Main Loop Coord: {main_coord.attrib} with mergeID {merge_id}")
                
                # Duplicate the marked coordinate
                duplicate_coord = ET.Element("coordinate", main_coord.attrib)
                loops[0].insert(min_main_index + 1, duplicate_coord)
                
                # Reorder the loop to start at the closest coordinate
                reordered_coords = other_coords[min_other_index:] + other_coords[:min_other_index]
                for i, coord_elem in enumerate(loop.findall("coordinate")):
                    coord_elem.set("X", str(reordered_coords[i][0]))
                    coord_elem.set("Y", str(reordered_coords[i][1]))
                
                print(f"Reordered Loop ID {merge_id} to start at index {min_other_index}.")
                
                # Append the first coordinate to close the loop
                first_coord = loop.findall("coordinate")[0]
                closing_coord = ET.Element("coordinate", first_coord.attrib)
                loop.append(closing_coord)
                
                print(f"Loop ID {merge_id} closed with coordinate {closing_coord.attrib}.")
            
            # Reassign the preserved X and Y attributes back to the <Field> tag
            field.set("X", x_attr)
            field.set("Y", y_attr)

        # Load the XML file
        print(f"Loading XML file: {input_file}")
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Process each field
        for field in root.findall("Field"):
            process_field(field)
        
        # Save the processed XML file
        output_file = os.path.join(output_dir, "field_coordinates_marked.xml")
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"Processed XML saved to {output_file}.")
        return output_file
