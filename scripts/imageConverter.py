import cv2
import numpy as np
import os

class imageConvert:
    def __init__(self):
        pass

    def process(self, input_file, output_dir):
        """
        Process the input file to create a white mask with unique island coloring.

        Args:
            input_file (str): Path to the input grayscale image.
            output_dir (str): Directory to save the processed output.

        Returns:
            str: Path to the saved output file.

        Raises:
            Exception: If the input file cannot be processed.
        """
        print("Image analysis: Starting process...")

        # Verify input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Image analysis: Input file '{input_file}' not found.")

        # Load the image in grayscale
        print(f"Image analysis: Loading image from {input_file}")
        image = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Image analysis: Failed to load input image from {input_file}")

        # Threshold the image to separate white islands from the background
        print("Image analysis: Thresholding image...")
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        # Find contours of white islands
        print("Image analysis: Finding contours...")
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a blank image for coloring the white islands
        colored_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

        # Assign a unique value to the red channel of each white island
        print(f"Image analysis: Coloring {len(contours)} white islands...")
        for i, contour in enumerate(contours):
            # Get the red channel value for the current island
            red_value = i + 1

            # Create a mask for the current island contour
            mask = np.zeros_like(image)
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

            # Color all the pixels within the contour
            colored_image[:, :, 2] = np.where((mask > 0) & (image == 255), red_value, colored_image[:, :, 2])

        # Save the colored image as an 8bpc RGB PNG
        output_file = os.path.join(output_dir, "processed_image.png")
        print(f"Image analysis: Saving processed image to {output_file}")
        cv2.imwrite(output_file, colored_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

        print("Image analysis: Processing completed.")
        return output_file
