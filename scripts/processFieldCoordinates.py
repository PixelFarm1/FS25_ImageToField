import xml.etree.ElementTree as ET
import math
import os

class createLoops:
    def process(self, input_file, output_dir, threshold):
        """
        Process field coordinates in the input XML file and save the cleaned version.

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
            try:
                return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
            except TypeError:
                raise ValueError(f"Invalid coordinates: coord1={coord1}, coord2={coord2}")

        def close_loop(loop):
            """Ensure the loop starts and ends at the same coordinate."""
            if loop[0] != loop[-1]:
                loop.append(loop[0])
            return loop

        def integrate_loops(base_loop, other_loops):
            """
            Integrate other loops into the base loop:
            - Loops attach only to the main loop.
            - Rearrange coordinates of loops such that the beginning and end
              of each loop surround the attachment point in the main loop.
            """
            for loop in other_loops:
                # Find the closest point in base_loop to the start of the current loop
                start_coord = loop[0]
                closest_idx = min(
                    range(len(base_loop)),
                    key=lambda i: euclidean_distance(base_loop[i], start_coord)
                )
                # Rearrange the loop to ensure closure
                closed_loop = close_loop(loop)
                # Integrate the loop into the base loop with reordered coordinates
                base_loop = (
                    base_loop[:closest_idx + 1]
                    + closed_loop
                    + [base_loop[closest_idx]]  # Repeat the attachment point for closure
                    + base_loop[closest_idx + 1:]
                )
            return base_loop

        # Output file path
        output_file = os.path.join(output_dir, "processed_field_coordinates.xml")

        # Parse the input XML file
        try:
            tree = ET.parse(input_file)
            root = tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML file: {e}")

        for field in root.findall("Field"):
            field_id = field.attrib.get('ID', 'unknown')
            x_attr = field.attrib.get('X', None)  # Preserve X attribute
            y_attr = field.attrib.get('Y', None)  # Preserve Y attribute

            coordinates = []
            for coord in field.findall("coordinate"):
                try:
                    x = float(coord.attrib['X'])
                    y = float(coord.attrib['Y'])
                    coordinates.append((x, y))
                except (KeyError, ValueError):
                    continue

            if not coordinates:
                continue

            # Segment coordinates into loops
            loops = []
            current_loop = [coordinates[0]]
            for i in range(1, len(coordinates)):
                if euclidean_distance(coordinates[i - 1], coordinates[i]) > threshold:
                    loops.append(close_loop(current_loop))
                    current_loop = []
                current_loop.append(coordinates[i])
            loops.append(close_loop(current_loop))

            # Merge loops into a single loop
            base_loop = loops[0]
            other_loops = loops[1:]
            integrated_loop = integrate_loops(base_loop, other_loops)

            # Clear and restore coordinates in the original structure
            field.clear()  # Clear existing children but preserve attributes
            if field_id != 'unknown':
                field.set('ID', field_id)
            if x_attr:
                field.set('X', x_attr)
            if y_attr:
                field.set('Y', y_attr)

            for x, y in integrated_loop:
                ET.SubElement(field, "coordinate", X=str(x), Y=str(y))

        # Write the final cleaned XML to the output file
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        return output_file
