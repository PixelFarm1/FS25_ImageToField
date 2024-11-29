import customtkinter as ctk
import tkinter.filedialog as fd
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FS25 Image to fields")
        self.geometry("920x800")
        ctk.set_appearance_mode("dark")
        theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme.json")
        if not os.path.exists(theme_path):
            print(f"Error: Theme file not found at {theme_path}")
        ctk.set_default_color_theme(theme_path)
        
        self.info_box = None
        self.hover_job = None

        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=5)
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(2, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self.log_frame, text="Information", fg_color="#659927", corner_radius=5, height=30, font=("Roboto",15,"bold"))
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="new")
        self.log_box = ctk.CTkTextbox(self.log_frame, width=600, height=750, state="normal", wrap="word")
        self.log_box.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.log_box.configure(state="disabled")  # Initially read-only

        # Input frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=1, sticky="nsew", pady=10, padx=5)
        self.input_frame.grid_rowconfigure(2, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)  # Ensure var_frame can expand

        self.files_frame = ctk.CTkFrame(self.input_frame)
        self.files_frame.grid(row=0, padx=10, pady=10, sticky="nsew")
        self.files_frame.grid_columnconfigure(0, weight=1)

        # File input
        self.file_input = ctk.CTkEntry(self.files_frame, placeholder_text="Select PNG file for processing")
        self.file_input.grid(pady=5, padx=5, sticky="ew")
        self.browse_button = ctk.CTkButton(self.files_frame, text="Browse", font=("", 15, "bold"), command=self.browse_file)
        self.browse_button.grid(pady=5, padx=5, sticky="ew")

        self.var_frame = ctk.CTkFrame(self.input_frame)
        self.var_frame.grid(row=1, padx=10, pady=10, sticky="nsew")
        self.var_frame.grid_rowconfigure(0, weight=1)  # For dem_frame
        self.var_frame.grid_rowconfigure(1, weight=1)  # For slider_frame
        self.var_frame.grid_columnconfigure(0, weight=1)

        self.dem_frame = ctk.CTkFrame(self.var_frame)
        self.dem_frame.grid(row=0, padx=10, pady=10, sticky="nsew")
        self.dem_frame.grid_columnconfigure(0, weight=1)

        #DEM size
        self.demSize_label = ctk.CTkLabel(self.dem_frame, text="Select the size of your DEM")
        self.demSize_label.grid(pady=5, padx=5, sticky="ew")
        self.demSize = ctk.CTkComboBox(self.dem_frame, values=["1024", "2048", "4096", "8192"])
        self.demSize.set("2048")
        self.demSize.grid(pady=5, padx=5, sticky="ew")


        # Add sliders for variables
        self.slider_frame = ctk.CTkFrame(self.var_frame)
        self.slider_frame.grid(row=1, padx=10, pady=10, sticky="nsew")
        self.slider_frame.grid_columnconfigure(0, weight=1)

        self.slider1_label = ctk.CTkLabel(self.slider_frame, text="Simplification Strength")
        self.slider1_label.grid(sticky="ew", pady=5, padx=5)

        self.slider1 = ctk.CTkSlider(self.slider_frame, from_=0, to=1, number_of_steps=10,
                command=self.update_simplification_strength,
                progress_color="#7cbb32",
                button_color="#7cbb32",
                button_hover_color="#7cbb32")
        self.slider1.set(0.2)
        self.slider1.grid(sticky="ew", pady=5, padx=5)

        self.slider1_dis = ctk.CTkEntry(self.slider_frame)
        self.slider1_dis.grid(sticky="ew", pady=5, padx=5)
        self.slider1_dis.insert(0, str(0.2))

        self.slider1.bind("<B1-Motion>", lambda e: self.slider1_dis.delete(0, "end") or self.slider1_dis.insert(0, round(self.slider1.get(),1)))
        self.slider1_dis.bind("<Return>", lambda e: self.slider1.set(float(self.slider1_dis.get())))

        self.slider2_label = ctk.CTkLabel(self.slider_frame, text="Distance Threshold")
        self.slider2_label.grid(sticky="ew", pady=5, padx=5)

        self.slider2 = ctk.CTkSlider(self.slider_frame, from_=0, to=20, number_of_steps=20,
                command=self.update_distance_threshold,
                progress_color="#7cbb32",
                button_color="#7cbb32",
                button_hover_color="#7cbb32")
        self.slider2.set(10)
        self.slider2.grid(sticky="ew", pady=5, padx=5)

        self.slider2_dis = ctk.CTkEntry(self.slider_frame)
        self.slider2_dis.grid(sticky="ew", pady=5, padx=5)
        self.slider2_dis.insert(0, 10)

        self.slider2.bind("<B1-Motion>", lambda e: self.slider2_dis.delete(0, "end") or self.slider2_dis.insert(0, int(self.slider2.get())))
        self.slider2_dis.bind("<Return>", lambda e: self.slider2.set(int(self.slider2_dis.get())))
        
        self.slider3_label = ctk.CTkLabel(self.slider_frame, text="Border reduction")
        self.slider3_label.grid(sticky="ew", pady=5, padx=5)

        self.slider3 = ctk.CTkSlider(self.slider_frame, from_=0, to=10, number_of_steps=10,
                command=self.update_shrink_amount,
                progress_color="#7cbb32",
                button_color="#7cbb32",
                button_hover_color="#7cbb32")
        self.slider3.set(0)
        self.slider3.grid(sticky="ew", pady=5, padx=5)

        self.slider3_dis = ctk.CTkEntry(self.slider_frame)
        self.slider3_dis.grid(sticky="ew", pady=5, padx=5)
        self.slider3_dis.insert(0, 0)

        self.slider3.bind("<B1-Motion>", lambda e: self.slider3_dis.delete(0, "end") or self.slider3_dis.insert(0, int(self.slider3.get())))
        self.slider3_dis.bind("<Return>", lambda e: self.slider3.set(int(self.slider3_dis.get())))

        self.run_frame = ctk.CTkFrame(self.input_frame)
        self.run_frame.grid(row=2, column=0, padx=10, pady=10, sticky="new")
        self.run_frame.grid_columnconfigure(0, weight=1)

        # Run button
        self.run_button = ctk.CTkButton(self.run_frame, text="Run", height=50, font=("",20))
        self.run_button.grid(column=0, row=0, pady=5, padx=5, sticky="ew")

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        self.slider1_label_tooltip = "Controls the level of simplification applied to the geometry."
        self.slider2_label_tooltip = "Sets the maximum allowable distance between points to class it as an 'island'."
        self.slider3_label_tooltip = "Units of reduction of the field outline. Only affects the outer loop."
        self.demSize_label_tooltip = "If DEM is size 2049x2049. Choose 2048."
        self.bind_tooltip("slider1_label")
        self.bind_tooltip("slider2_label")
        self.bind_tooltip("slider3_label")
        self.bind_tooltip("demSize_label")


    def update_simplification_strength(self, value):
        self.simplification_strength = round(float(value), 2)

    def update_distance_threshold(self, value):
        self.distance_threshold = int(value)

    def update_shrink_amount(self, value):
        self.shrink_amount = int(value)

    #Information boxes
    def show_info(self, event, text):
        # Schedule the info box to appear after a delay (e.g., 500ms)
        self.hover_job = self.after(200, lambda: self._create_info_box(event, text))

    def _create_info_box(self, event, text):
        # Ensure only one info box is visible
        if self.info_box is not None:
            self.info_box.destroy()

        # Create a new info box
        self.info_box = ctk.CTkToplevel(self)
        self.info_box.wm_overrideredirect(True)
        self.info_box.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        # Add content to the info box
        info_label = ctk.CTkLabel(self.info_box, text=text, padx=10, pady=5, corner_radius=5)
        info_label.pack()

    def hide_info(self, event):
        # Cancel the scheduled job if it exists
        if self.hover_job is not None:
            self.after_cancel(self.hover_job)
            self.hover_job = None

        # Destroy the current info box
        if self.info_box is not None:
            self.info_box.destroy()
            self.info_box = None
    
    def bind_tooltip(self, widget_name):
        # Dynamically construct the tooltip variable name
        tooltip_name = f"{widget_name}_tooltip"
        
        # Check if the tooltip variable exists
        tooltip_text = getattr(self, tooltip_name, None)
        
        if tooltip_text is not None:  
            widget = getattr(self, widget_name)  
            widget.bind("<Enter>", lambda e: self.show_info(e, tooltip_text))
            widget.bind("<Leave>", self.hide_info)

    def browse_file(self):
        # Open a file dialog to select a file
        file_path = fd.askopenfilename(
            title="Select a PNG File",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*"))  
        )
        
        # If a file is selected, set its path in the file_input entry
        if file_path:
            self.file_input.delete(0, "end")  # Clear the entry
            self.file_input.insert(0, file_path)  # Insert the selected file path

    def log_message(self, message):
        self.log_box.configure(state="normal")  # Enable editing
        self.log_box.insert("end", f"{message}\n")  # Insert the message
        self.log_box.see("end")  # Auto-scroll to the end
        self.log_box.configure(state="disabled")  # Disable editing

if __name__ == "__main__":
    app = App()
    app.mainloop()