# FS25_ImageToFields

> ## Download version 0.1.0 here: [https://github.com/PixelFarm1/FS25_ImageToFields/releases/tag/v0.1.0-experimental]

## German translation below ![image](https://github.com/user-attachments/assets/15acf8fb-474c-4326-a28c-885c138b1e4a)


#### For any code wizards looking at this... I'm sorry. I have almost no programming experience and a lot of the code is the work of me with the help of chatGPT. The code is most definately not perfectly set up  

FS25_ImageToFields is a tool for easy creation of field dimensions for FS25. It takes a white on black field mask as input and creates coordinates based on the image. Through some processing it verifies that the coordinates are ordered in a way that allows for complex field shapes. The final processed coordinates are run through the xmlToFields.lua which creates fields and their respective polygons. The GE script also aligns the polygonpoints to the terrain and repaints all fields. All you have to do at the end is run the repaint farmalnds function in the fieldToolkit of GE.

![image](https://github.com/user-attachments/assets/cb449c51-b168-4172-9053-d082ce425be3)

## This is what a proper field mask looks like
![image](https://github.com/user-attachments/assets/072c551c-b220-487e-8f28-8bebe1ef1e2a)


## How to use
1. Make sure that you have a clean field mask. There can be no mistakes in it or you will get a bad result or errors from the program. Common mistakes are: stray white pixels in non-field areas or black pixels in white areas. Too little space between 2 field boundarys (drive an imaginary 1x1 pixel size tractor along all field borders of the mask, if you cannot pass -> fix that area).

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

## Suggested workflow for converting FS22 maps
### Prerequisites: A FS22 map where all fields are painted with terrainDetail (May work if you take the densityMap_ground.gdm from a FS22 savegame too, not tested)

1. Convert the densityMap_ground.gdm using the converter at GDN

2. Open the converted file in GIMP and att a new layer with white fill

3. If the image turns all red and not white. Press Image -> Mode -> RGB to change to RGB mode. Then recreate the layer with white fill.

4. Set the blending mode to "Dodge" and merge the 2 layers

5. Press Select -> By color (Shift + O) and press one of the now bright red areas.

6. Look for any mistakes like missed pixels, stray pixels etc. They are more easy to spot when in the select mode. 

7. When you are done correcting the image. Create a new layer and with white fill.

8. Change blending mode to "HSV Saturation" and your field areas should turn white.

9. Merge the layers and repeat step 6 to find any mistakes in the mask. 

10. Export with these settings: 
![image](https://github.com/user-attachments/assets/b032a1dc-792b-4017-9600-4cf197ea9113)

11. Run the FS25_ImageToFields tool according to the instruction above



# Deutsche Übersetzung
#### Für alle Code-Zauberer, die sich das hier ansehen ... Es tut mir leid. Ich habe fast keine Programmiererfahrung, und ein Großteil des Codes entstand durch meine Arbeit mit der Hilfe von ChatGPT. Der Code ist mit Sicherheit nicht perfekt strukturiert.

FS25_ImageToFields ist ein Tool zur einfachen Erstellung von Feldgeometrien für FS25. Es nimmt eine Schwarz-Weiß-Feldmaske als Eingabe und erstellt basierend auf dem Bild Koordinaten. Durch eine Reihe von Verarbeitungsschritten wird sichergestellt, dass die Koordinaten in einer Weise geordnet sind, die komplexe Feldformen ermöglicht. Die final verarbeiteten Koordinaten werden durch die xmlToFields.lua-Datei verarbeitet, die Felder und deren jeweilige Polygone erstellt. Das GE-Skript richtet außerdem die Polygonpunkte am Gelände aus und übermalt alle Felder. Alles, was am Ende noch zu tun ist, ist die Funktion "Repaint Farmlands" im FieldToolkit von GE auszuführen.

![image](https://github.com/user-attachments/assets/cb449c51-b168-4172-9053-d082ce425be3)

## So sieht eine korrekte Feldmaske aus.
![image](https://github.com/user-attachments/assets/072c551c-b220-487e-8f28-8bebe1ef1e2a)

## Anleitung zur Verwendung
1. Stellen Sie sicher, dass Sie eine saubere Feldmaske haben.
Es dürfen keine Fehler in der Maske vorhanden sein, da dies zu einem schlechten Ergebnis führen kann. Häufige Fehler sind:

Vereinzelte weiße Pixel in Bereichen, die keine Felder sind.
Schwarze Pixel in weißen Feldbereichen.

2. Starten Sie die .exe aus der neuesten Version (oder main.py, falls Sie mehr Arbeit investieren möchten).

3. Klicken Sie auf "Browse" und wählen Sie Ihre Feldmaske aus.

4.Stellen Sie sicher, dass Sie die korrekte DEM-Größe einstellen. Dies ist die Auflösung Ihrer DEM.png im Datenordner Ihrer Karte minus 1 Pixel.

5. Ändern Sie beim ersten Durchlauf die Standardeinstellungen nicht. Verwenden Sie die Standardwerte und ändern Sie die Einstellungen erst nach dem ersten Durchlauf, wenn Sie Anpassungen am Ergebnis vornehmen möchten.

6. Drücken Sie auf "Run", um die Verarbeitung zu starten. Der Fortschritt wird im Protokoll angezeigt, und das Ausgabeverzeichnis wird dort angegeben.

7. Nach Abschluss der Verarbeitung können Sie auf "Visualize fields" klicken, um das endgültige Ergebnis anzuzeigen. Mit der Schaltfläche "Toggle Field IDs" können Sie die Feld-IDs ein- oder ausblenden.

8. Öffnen Sie den Giants Editor (GE) und stellen Sie sicher, dass Sie eine "Fields"-Gruppe mit den richtigen Attributen haben. Entfernen Sie außerdem alle untergeordneten Objekte der "Fields"-Transformationsgruppe.

9. Erstellen Sie ein neues Skript in GE und fügen Sie den Inhalt von xmlToFields.lua in die Datei ein. Alternativ können Sie die .lua-Datei in den Skriptordner von GE legen.

10. Passen Sie den Dateipfad am Ende der .lua-Datei an. Der Pfad sollte auf die final_field_coordinates.xml zeigen.

11. Führen Sie das Skript aus.Es wird alle vorhandenen gemalten Feldflächen löschen, die Felder aus den Koordinaten generieren, sie an das Gelände anpassen und die Felder neu bemalen.



