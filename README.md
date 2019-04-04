FUSION for Processing
---------------------

A QGIS plugin to use FUSION tools for LiDAR analysis and visualization.

This plugin is a port to QGIS 3 of the original FUSION provider that was a core element of Processing in QGIS 2

It is based on the initial porting of the FUSION provider to QGIS 3, done by Alexander Bruy.

Installation
--------------

Clone this repository and copy the `processing_fusion` folder to your QGIS plugins folder (in the folder correspodning to your current active QGIS profile)

Activate the plugin and activate the provider in the Processing settings. FUSION algorithms will appear in the Processing toolbox.

You do not need to install FUSION or configure it. The required FUSION binaries are already included in the `processing_fusion` folder.

Limitations
--------------

Currently, QGIS does not allow multiple files to be selected for the QgsProcessingParameterFile class. That means that, although most of the FUSION algorithms accept a set of .las files as input, you will only be able to select one in the corresponding file selector. 

You can, however, use a multiple input by directly typing the filepaths (not selecting it in the file selector) in the textbox, separated by semicolons (;)

