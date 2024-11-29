import xml.etree.ElementTree as ET
import os

class FinalizeFieldCoordinates:
    def process(self, input_file, output_dir):
        """
        Processes the marked field coordinates to finalize the XML structure.
        
        Args:
            input_file (str): Path to the input XML file.
            output_dir (str): Directory to save the processed XML file.
        
        Returns:
            str: Path to the saved processed XML file.
        """
        def process_field(field):
            """Process a single field and finalize its coordinates."""
            field_id = field.get("ID")
            x_attr = field.get("X", "0")  # Preserve X attribute
            y_attr = field.get("Y", "0")  # Preserve Y attribute

            print(f"Processing Field ID: {field_id}")
            output_field = ET.SubElement(output_root, "Field", {"ID": field_id, "X": x_attr, "Y": y_attr})

            # Extract Loop 1 and all other loops
            loop1 = field.find("./Loop[@ID='1']")
            if loop1 is None:
                print(f"No Loop ID='1' found in Field ID={field_id}. Skipping.")
                return

            merge_points = []
            other_loops = {}

            # Collect merge points and other loops
            for loop in field.findall("Loop"):
                loop_id = loop.get("ID")
                if loop_id == "1":
                    for coordinate in loop.findall("coordinate"):
                        merge_id = coordinate.get("mergeID")
                        if merge_id:
                            merge_points.append((merge_id, coordinate))
                            print(f"Found merging point in Field ID={field_id}, Loop ID={loop_id}: mergeID={merge_id}")
                else:
                    other_loops[loop_id] = [coord.attrib for coord in loop.findall("coordinate")]

            # Rearrange coordinates in Loop 1 with merging logic
            ordered_coords = []
            for coord in loop1.findall("coordinate"):
                ordered_coords.append(coord.attrib)
                if coord.get("mergeID"):
                    merge_id = coord.get("mergeID")
                    if merge_id in other_loops:
                        print(f"Inserting coordinates from Loop ID={merge_id} into Loop ID=1 for Field ID={field_id}")
                        # Insert matching loop coordinates after this merging point
                        ordered_coords.extend(other_loops[merge_id])
                        del other_loops[merge_id]  # Remove merged loop from other_loops

            # Add ordered coordinates to output
            for coord in ordered_coords:
                ET.SubElement(output_field, "coordinate", coord)

        # Define output file path
        output_file = os.path.join(output_dir, "final_field_coordinates.xml")
        
        try:
            # Load XML file
            print(f"Loading XML file: {input_file}")
            tree = ET.parse(input_file)
            root = tree.getroot()

            # Initialize output XML structure
            output_root = ET.Element("Fields")

            # Process each field
            for field in root.findall("Field"):
                process_field(field)

            # Write to output XML
            print(f"Writing output XML to: {output_file}")
            tree = ET.ElementTree(output_root)
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            print("Processing completed successfully.")

            return output_file

        except Exception as e:
            print(f"An error occurred while processing the XML: {e}")
            raise
