from scripts.gui import App  
from scripts.imageConverter import imageConvert  
from scripts.imageToCoordinates import createCoordinates  
from scripts.processFieldLoops import ProcessFieldLoops  
from scripts.simplifyFieldLoops import SimplifyFieldLoops  
from scripts.markFieldLoops import MarkFieldLoops  
from scripts.finalizeFieldCoordinates import FinalizeFieldCoordinates  
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

def ensure_output_folder_exists():
    """
    Ensures the 'output' folder exists next to the main script.
    If the folder does not exist, it is created.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the 'output' folder next to the script
    output_folder = os.path.join(script_dir, "output")
    
    # Create the folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"'output' folder created at: {output_folder}")
    else:
        print(f"'output' folder already exists at: {output_folder}")
    
    return output_folder

def run_pipeline(input_file, simplificationStrength, distanceThreshold, borderReduction, demSize):
    print("Starting the tool...")

    # Ensure the 'output' folder exists
    output_folder = ensure_output_folder_exists()

    imageConverter = imageConvert()
    converted_image = imageConverter.process(input_file, output_folder)

    createCoordinates1 = createCoordinates()
    xml_coordinates = createCoordinates1.process(converted_image, output_folder, demSize)

    processFieldLoops = ProcessFieldLoops()
    processedLoops_xml = processFieldLoops.process(xml_coordinates, output_folder, distanceThreshold)

    simplifyFieldLoops = SimplifyFieldLoops()
    simplified_xml = simplifyFieldLoops.process(processedLoops_xml, output_folder, simplificationStrength, borderReduction)

    markFieldLoops = MarkFieldLoops()
    marked_xml = markFieldLoops.process(simplified_xml, output_folder)

    finalizeFieldCoordinates = FinalizeFieldCoordinates()
    final_output = finalizeFieldCoordinates.process(marked_xml, output_folder)

    return final_output  # Return the final output file path

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", message)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass

class MyApp(App):
    def __init__(self):
        super().__init__()
        sys.stdout = TextRedirector(self.log_box)
        sys.stderr = TextRedirector(self.log_box)
        self.run_button.configure(command=self.start_pipeline_thread)
        self.viz_button.configure(command=self.visualize_fields)

        


    def start_pipeline_thread(self):
        import threading
        input_file = self.file_input.get()
        simplificationStrength = float(self.slider1.get())
        distanceThreshold = int(self.slider2.get())
        borderReduction = int(self.slider3.get())
        demSize = int(self.demSize.get())
        threading.Thread(
            target=self.run_pipeline_safe,
            args=(input_file, simplificationStrength, distanceThreshold, borderReduction, demSize),
        ).start()

    def run_pipeline_safe(self, input_file, simplificationStrength, distanceThreshold, borderReduction, demSize):
        try:
            print("Running tool...")
            final_output = run_pipeline(input_file, simplificationStrength, distanceThreshold, borderReduction, demSize)
        except Exception as e:
            self.log_message(f"Error: {e}")

    

    def visualize_fields(self):
        """
        Searches the output folder for final_field_coordinates.xml and visualizes the fields.
        If the file is not found, prompts the user to run the pipeline first.
        """
        # Determine the output folder location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(script_dir, "output")
        final_output_file = os.path.join(output_folder, "final_field_coordinates.xml")

        if not os.path.exists(final_output_file):
            self.log_message(f"Error: {final_output_file} not found. Please run the tool first.")
            return

        try:
            self.log_message("Visualizing fields...")
            self.display_plot_in_gui(final_output_file)
            self.log_message("Visualization completed successfully.")
        except Exception as e:
            self.log_message(f"Visualization error: {e}")

    def display_plot_in_gui(self, file_path):
        """
        Renders the visualization directly in the GUI.
        """
        # Parse and generate the plot
        fields, centers = parse_all_field_coordinates_with_center_flipped_plane(file_path)
        fig, ax = plt.subplots(figsize=(6, 6))

        for field_id, coords in fields.items():
            x, y = zip(*coords)
            ax.plot(x, y, label=f"Field {field_id}", color="black")
            center_x, center_y = centers[field_id]
            ax.text(
                center_x, center_y, f"ID {field_id}", fontsize=9, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="#659927", alpha=0.8)
            )

        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Z Coordinate ")
        ax.set_title("Visualization of All Fields")
        ax.grid(True)

        # Embed the Matplotlib figure into the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)  # Use pack to display the plot widget

def parse_all_field_coordinates_with_center_flipped_plane(file_path):
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


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
