import xml.etree.ElementTree as ET
from shapely.geometry import LineString, Polygon
import os

class SimplifyFieldLoops:
    def process(self, input_file, output_dir, simplification_strength, shrink_distance):
        """
        Simplify all loops and shrink loop ID=1 in an XML file.

        Args:
            input_file (str): Path to the input XML file.
            output_dir (str): Directory to save the simplified XML file.
            simplification_strength (float): Simplification tolerance.
            shrink_distance (float): Distance to shrink loop ID=1.

        Returns:
            str: Path to the saved simplified XML file.
        """
        def simplify_coordinates(coordinates, tolerance):
            """Simplify coordinates using the Ramer-Douglas-Peucker algorithm."""
            line = LineString(coordinates)
            simplified_line = line.simplify(tolerance, preserve_topology=True)
            return list(simplified_line.coords)

        def shrink_loop(coordinates, distance):
            """
            Shrink or expand a loop contour by a specified distance.
            Args:
                coordinates (list of tuples): List of (x, y) tuples representing the polygon's vertices.
                distance (float): Distance to shrink or expand (negative for inward shrinking).
            Returns:
                list of tuples: Modified coordinates.
            """
            polygon = Polygon(coordinates)
            if not polygon.is_valid:
                polygon = polygon.buffer(0)  # Attempt to fix invalid polygons
            
            shrunk_polygon = polygon.buffer(-distance)  # Negative for shrinking, positive for expanding
            
            if shrunk_polygon.is_empty:
                print("Shrinking resulted in an empty polygon. Returning original coordinates.")
                return coordinates  # Return original if shrinking collapses the polygon

            if shrunk_polygon.geom_type == "MultiPolygon":
                print("Shrinking resulted in multiple polygons. Selecting the largest polygon.")
                shrunk_polygon = max(shrunk_polygon, key=lambda p: p.area)  # Select the largest polygon

            if shrunk_polygon.geom_type == "Polygon":
                return list(shrunk_polygon.exterior.coords)
            
            print(f"Unexpected geometry type after shrinking: {shrunk_polygon.geom_type}")
            return coordinates


        def process_loop(loop_element, tolerance, shrink_distance):
            """Process, simplify, and optionally shrink coordinates within a Loop XML element."""
            original_coords = []
            for coord in loop_element.findall('coordinate'):
                x = float(coord.get('X'))
                y = float(coord.get('Y'))
                original_coords.append((x, y))

            # Simplify the loop
            simplified_coords = simplify_coordinates(original_coords, tolerance)

            # If the loop ID is 1, perform shrinking
            loop_id = loop_element.get('ID')
            if loop_id == "1" and shrink_distance is not None:
                modified_coords = shrink_loop(simplified_coords, shrink_distance)
            else:
                modified_coords = simplified_coords

            removed = len(original_coords) - len(modified_coords)

            # Clear the original coordinates and replace them with the modified ones
            for coord in list(loop_element):
                loop_element.remove(coord)

            for x, y in modified_coords:
                ET.SubElement(loop_element, 'coordinate', X=str(x), Y=str(y))

            return removed

        # Define output file path
        output_file = os.path.join(output_dir, "simplified_field_loops.xml")

        # Load and process the XML file
        print(f"Loading XML file: {input_file}")
        tree = ET.parse(input_file)
        root = tree.getroot()

        total_original_coords = 0
        total_removed_coords = 0

        for field in root.findall('.//Field'):
            for loop in field.findall('.//Loop'):
                original_count = len(loop.findall('coordinate'))
                removed = process_loop(loop, simplification_strength, shrink_distance if loop.get('ID') == "1" else None)
                total_original_coords += original_count
                total_removed_coords += removed
                print(f"Processed loop ID={loop.get('ID')}: {original_count} points, reduced by {removed} points.")

        reduction_percentage = (total_removed_coords / total_original_coords) * 100 if total_original_coords else 0
        print(f"Total original points: {total_original_coords}, points removed: {total_removed_coords}, "
                     f"reduction: {reduction_percentage:.2f}%")

        print(f"Writing simplified XML to: {output_file}")
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

        return output_file
