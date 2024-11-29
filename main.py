from scripts.gui import App  # type: ignore
from scripts.imageConverter import imageConvert  # type: ignore
from scripts.imageToCoordinates import createCoordinates  # type: ignore
from scripts.processFieldLoops import ProcessFieldLoops  # type: ignore
from scripts.simplifyFieldLoops import SimplifyFieldLoops  # type: ignore
from scripts.markFieldLoops import MarkFieldLoops  # type: ignore
from scripts.finalizeFieldCoordinates import FinalizeFieldCoordinates  # type: ignore
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
    print("Starting the pipeline...")

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
        self.ood_button.configure(command=self.open_output_folder)

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
            print("Running pipeline...")
            final_output = run_pipeline(input_file, simplificationStrength, distanceThreshold, borderReduction, demSize)
        except Exception as e:
            self.log_message(f"Pipeline error: {e}")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
