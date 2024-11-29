import xml.etree.ElementTree as ET
import math
import os


class ProcessFieldLoops:
    def process(self, input_file, output_dir, threshold=10):
        """
        Process field loops in the input XML file and save the updated XML.

        Args:
            input_file (str): Path to the input XML file.
            output_dir (str): Directory to save the output XML file.
            threshold (float): Distance threshold for segmenting loops.

        Returns:
            str: Path to the saved output XML file.

        Raises:
            Exception: If any error occurs during processing.
        """
        def euclidean_distance(coord1, coord2):
            """Calculate Euclidean distance between two coordinates."""
            return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

        def close_loop(loop):
            """Ensure the loop starts and ends at the same coordinate."""
            if loop and loop[0] != loop[-1]:
                loop.append(loop[0])
            return loop

        def rearrange_loops(base_loop, other_loops):
            """Rearrange loops so loops with ID > 1 are adjacent to the nearest point in base_loop."""
            print(f"Rearranging {len(other_loops)} additional loops relative to the base loop.")
            rearranged = []
            for loop in other_loops:
                closest_base = min(
                    base_loop, 
                    key=lambda base: min(euclidean_distance(base, coord) for coord in loop)
                )
                rearranged.append((closest_base, loop))
            rearranged.sort(key=lambda x: x[0])  # Sort by proximity to base_loop
            return [item[1] for item in rearranged]

        # Define the output file path
        output_file = os.path.join(output_dir, "field_loops.xml")
        print(f"Starting to process field loops from {input_file}")

        # Parse the input XML file
        try:
            tree = ET.parse(input_file)
            root = tree.getroot()
            print(f"Successfully parsed XML file: {input_file}")
        except ET.ParseError as e:
            print(f"Failed to parse XML file: {e}")
            raise ValueError(f"Failed to parse XML file: {e}")

        for field in root.findall("Field"):
            field_id = field.attrib.get('ID', 'unknown')
            x_attr = field.attrib.get('X', '0')
            y_attr = field.attrib.get('Y', '0')

            print(f"Processing Field ID: {field_id}")

            coordinates = []
            for coord in field.findall("coordinate"):
                try:
                    x = float(coord.attrib['X'])
                    y = float(coord.attrib['Y'])
                    coordinates.append((x, y))
                except (KeyError, ValueError) as e:
                    print(f"Skipping invalid coordinate: {e}")

            if not coordinates:
                print(f"No valid coordinates for Field ID: {field_id}")
                continue

            # Segment coordinates into loops
            print(f"Segmenting coordinates into loops for Field ID: {field_id}")
            loops = []
            current_loop = [coordinates[0]]
            for i in range(1, len(coordinates)):
                if euclidean_distance(coordinates[i - 1], coordinates[i]) > threshold:
                    loops.append(close_loop(current_loop))
                    current_loop = []
                current_loop.append(coordinates[i])
            loops.append(close_loop(current_loop))
            print(f"Segmented {len(loops)} loops for Field ID: {field_id}")

            # Rearrange loops
            base_loop = loops[0]
            other_loops = loops[1:]
            rearranged_loops = rearrange_loops(base_loop, other_loops)
            print(f"Rearranged loops for Field ID: {field_id}")

            # Update field with segmented and rearranged loops
            field.clear()
            field.attrib['ID'] = field_id
            field.attrib['X'] = x_attr
            field.attrib['Y'] = y_attr

            for i, loop in enumerate([base_loop] + rearranged_loops, start=1):
                loop_element = ET.SubElement(field, "Loop", ID=str(i))
                for x, y in loop:
                    ET.SubElement(loop_element, "coordinate", X=str(x), Y=str(y))

        # Write the updated XML to the output file
        try:
            tree.write(output_file, encoding="utf-8", xml_declaration=True)
            print(f"Processed field loops saved to {output_file}")
        except Exception as e:
            print(f"Failed to write output XML file: {e}")
            raise

        return output_file
