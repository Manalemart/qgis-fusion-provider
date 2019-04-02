# -*- coding: utf-8 -*-

"""
***************************************************************************
    ImageCreate.py
    ---------------------
    Date                 : January 2016
    Copyright            : (C) 2016 by Niccolo' Marchi
    Email                : sciurusurbanus at hotmail dot it
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = "Niccolo' Marchi"
__date__ = 'January 2016'
__copyright__ = "(C) 2016 by Niccolo' Marchi"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from qgis.core import (QgsProcessingException,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber
                      )

from processing_fusion.fusionAlgorithm import FusionAlgorithm
from processing_fusion import fusionUtils

class ImageCreate(FusionAlgorithm):

    INPUT = 'INPUT'
    COLOROPTION = 'COLOROPTION'
    GROUND = 'GROUND'
    PIXEL = 'PIXEL'
    RGB = 'RGB'
    SWITCH = 'SWITCH'
    OUTPUT = 'OUTPUT'

    def name(self):
        return 'imagecreate'

    def displayName(self):
        return self.tr('Image create')

    def group(self):
        return self.tr('Points')

    def groupId(self):
        return 'points'

    def tags(self):
        return self.tr('lidar')

    def shortHelpString(self):
        return ''

    def __init__(self):
        super().__init__()


    def initAlgorithm(self, config=None):    
        self.addParameter(QgsProcessingParameterFile(
            self.INPUT, self.tr('Input LAS layer'), extension = 'las'))        
        self.addParameter(QgsProcessingParameterFileDestination(self.OUTPUT,
                                                                self.tr('Output image')))        
        self.addParameter(QgsProcessingParameterEnum(
            self.COLOROPTION, self.tr('Method to assign color'),
            ['Intensity', 'Elevation', 'Height']))
        self.addParameter(QgsProcessingParameterFile(
            self.GROUND, self.tr("Ground file (used with 'Height' method)"), 
            extension = self.tr('DTM files (*.dtm *.DTM)')))        
        self.addParameter(QgsProcessingParameterBoolean(
            self.RGB, self.tr('Use RGB color model to create the color ramp'), False))
        self.addParameter(QgsProcessingParameterNumber(
            self.PIXEL, self.tr('Pixel size'), QgsProcessingParameterNumber.Double,
            minValue = 0, defaultValue = 1.0))
        self.addParameter(QgsProcessingParameterEnum(
            self.SWITCH, self.tr('Output format'), ['JPEG', 'Bitmap']))        

    def processAlgorithm(self, parameters, context, feedback):
        commands = [os.path.join(fusionUtils.fusionDirectory(), 'ImageCreate.exe')]        
        commands.append('/coloroption:' + self.parameterAsString(parameters, self.COLOROPTION, context))
        ground = self.parameterAsString(parameters, self.GROUND, context).strip()
        if ground:
            commands.append('/dtm:' + ground)
        if self.parameterAsBoolean(parameters, self.RGB, context):
            commands.append('/rgb')
        if self.parameterAsString(parameters, self.SWITCH, context) == 'JPEG':
            commands.append('/jpg')
        else:
            commands.append('/bmp')
        
        outputFile = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        commands.append(outputFile)
        commands.append(str(self.parameterAsDouble(parameters, self.PIXEL, context)))
        self.addInputFilesToCommands(commands, parameters, self.INPUT, context)        

        fusionUtils.execute(commands, feedback)

        return {self.OUTPUT, outputFile}
