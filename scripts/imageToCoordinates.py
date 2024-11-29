import cv2
import numpy as np
import xml.etree.ElementTree as ET
import os

class createCoordinates:
    def process(self, input_image_path, output_dir, dem_size):
        """
        Extract field coordinates with 3D center from an image and save to "coordinates1.xml".

        Args:
            input_image_path (str): Path to the input image file.
            output_dir (str): Directory to save the output XML file.
            dem_size (int): Size of the DEM for coordinate calculations.

        Returns:
            str: Path to the saved XML file.

        Raises:
            Exception: If the input image cannot be loaded or processing fails.
        """
        print("Creating coordinates: Starting to process the image...")

        # Verify the input image exists and is readable
        if not os.path.exists(input_image_path):
            raise FileNotFoundError(f"Input image file does not exist: {input_image_path}")

        # Ensure output directory exists
        print(f"Creating coordinates: Ensuring directory exists: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

        # Construct the output XML file path
        output_xml_path = os.path.join(output_dir, "coordinates1.xml")
        print(f"Creating coordinates: Output XML path set to {output_xml_path}")

        # Verify directory permissions
        if not os.access(output_dir, os.W_OK):
            raise PermissionError(f"Directory is not writable: {output_dir}")



        # Load the image
        image = cv2.imread(input_image_path)
        if image is None:
            print(f"Creating coordinates: Failed to load image from {input_image_path}.")
            raise FileNotFoundError(f"Image file not found or unreadable: {input_image_path}")

        print(f"Creating coordinates: Image loaded successfully. Processing dimensions and red channel...")
        height, width, _ = image.shape
        ratio = width / dem_size
        red_channel = image[:, :, 2]
        unique_red_values = sorted(set(np.unique(red_channel)) - {0})

        root = ET.Element("Fields")
        print(f"Creating coordinates: Detected {len(unique_red_values)} unique field regions to process.")

        for idx, red_value in enumerate(unique_red_values, start=1):
            print(f"Creating coordinates: Processing field {idx}/{len(unique_red_values)} with red value {red_value}...")
            mask = (red_channel == red_value).astype(np.uint8) * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            field_coordinates = [
                (round((point[0][0] - (width // 2)) / ratio, 2),
                 round(((height // 2) - point[0][1]) / ratio, 2))
                for contour in contours for point in contour
            ]

            M = cv2.moments(mask)
            center_x, center_y = (0, 0)
            if M["m00"] != 0:
                center_x = round((int(M["m10"] / M["m00"]) - (width // 2)) / ratio, 2)
                center_y = round(((height // 2) - int(M["m01"] / M["m00"])) / ratio, 2)

            adjusted_coordinates = [
                (round(coord[0] - center_x, 2), round(coord[1] - center_y, 2))
                for coord in field_coordinates
            ]

            field_element = ET.SubElement(root, "Field", ID=str(int(red_value)),
                                          X=str(center_x), Y=str(center_y))
            for coord in adjusted_coordinates:
                ET.SubElement(field_element, "coordinate", X=str(coord[0]), Y=str(coord[1]))

        tree = ET.ElementTree(root)
        print(f"Creating coordinates: Saving XML to: {output_xml_path}")
        with open(output_xml_path, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

        print(f"Creating coordinates: Processing complete. XML file saved to {output_xml_path}.")
        return output_xml_path
