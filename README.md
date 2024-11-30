# FS25_ImageToField

#### For any code wizards looking at this... I'm sorry. I have almost no programming experience and a lot of the code is the work of me with the help of chatGPT. The code is most definately not perfectly set up  

FS25_ImageToField is a tool for easy creation of field dimensions for FS25. It takes a white on black field mask as input and creates coordinates based on the image. Through some processing it verifies that the coordinates are ordered in a way that allows for complex field shapes. The final processed coordinates are run through the xmlToFields.lua which creates fields and their respective polygons. The GE script also aligns the polygonpoints to the terrain and repaints all fields. All you have to do at the end is run the repaint farmalnds function in the fieldToolkit of GE.

![image](https://github.com/user-attachments/assets/cb449c51-b168-4172-9053-d082ce425be3)

## This is what a proper field mask looks like
![image](https://github.com/user-attachments/assets/072c551c-b220-487e-8f28-8bebe1ef1e2a)


## How to use
1. Make sure that you have a clean field mask. There can be no mistakes in it or you will get a bad result. Common mistakes are: stray white pixels in non-field areas or black pixels in white areas.

2. Run the .exe from the latest release (or main.py if you want more work)

3. Click "Browse" and choose your field mask.

4. Make sure to set the correct DEM size. This is the resolution of your DEM.png in the data folder of your map (-1 pixel). 

5. It is recommended to not change the settings on the first run but to go with the defaults. Change the settings and run again if you want to make any tweaks to the output.

6. Press "Run" to start the processing. The log will tell you the output directory.

7. After the processing is finished, you can press "Visualize fields" to show the final output. Toggle the IDs on and off by pressing "Toggle Field IDs".

8. Go into Giants Editor and make sure that you have a "Fields" group with the correct attributes. Also remove any childs of the Fields transform group.

9. Create a new script in GE and paste the xmlToFields.lua contents to the file. Or just drop the whole .lua in your scripts folder for GE.

10. Change the filepath at the bottom of the .lua file. It should point to the location of your final_field_coordinates.xml

11. Execute the script. This will clear all existing painted field ground, generate the fields from coordinates, align them to the terrain and then repaint the fields.



