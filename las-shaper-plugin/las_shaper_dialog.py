# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LasShaperDialog
                                 A QGIS plugin
 Plugin for las files.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-04-17
        git sha              : $Format:%H$
        copyright            : (C) 2023 by d4mp3
        email                : pszdam@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog
from .las_shaper_functions import *
from .classification_codes import *

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'las_shaper_dialog_base.ui'))


class LasShaperDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LasShaperDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Extract Las class frame
        self.cbClassificationCode.addItems(CLASSIFICATION_CODES.values())
        self.tbInputELC.clicked.connect(self.__get_elc_input)
        self.tbOutputELC.clicked.connect(self.__set_elc_output)
        self.pbELC.clicked.connect(self.__run_extract_las_class)

        # Clip XYZ to polygon frame
        self.tbInputPathCXTP.clicked.connect(self.__get_cxtp_xyz_input)
        self.tbInputPolygonPathCXTP.clicked.connect(self.__get_cxtp_polygon_input)
        self.tbOutputCXTP.clicked.connect(self.__set_cxtp_output)
        self.pbCXTP.clicked.connect(self.__run_clip_xyz_to_polygon)

        # Get max height frame
        self.tbDemInputGMH.clicked.connect(self.__get_gmh_dem_input)
        self.tbleDsmInputGMH.clicked.connect(self.__get_gmh_dsm_input)
        self.tbShpInputGMH.clicked.connect(self.__get_gmh_shp_input)
        self.tbOutputGMH.clicked.connect(self.__set_gmh_output)
        self.pbGMH.clicked.connect(self.__run_get_max_height)


        # Merge files frame
        self.tbInputMF.clicked.connect(self.__set_mf_input)
        self.tbOutputMF.clicked.connect(self.__get_mf_output)
        self.pbMF.clicked.connect(self.__run_merge_files)


        # Convert files frame
        self.tbInputCF.clicked.connect(self.__set_mf_input)
        self.tbOutputCF.clicked.connect(self.__get_mf_output)
        self.pbCF.clicked.connect(self.__run_convert_files)


    def __get_elc_input(self):
        input_path = QFileDialog.getOpenFileNames(self, "Open LAS Files", "", "LAS Files (*.las)")
        if len(input_path[0]) != 0:
            input_path = input_path[0]
            input_path = '; '.join(input_path)
            self.leInputELC.setText(str(input_path))


    def __set_elc_output(self):
        output_path = QFileDialog.getSaveFileName(self, "Save File", "", "LAS File (*.las)")
        if len(output_path[0]) != 0:
            self.leOutputELC.setText(str(output_path[0]))


    def __run_extract_las_class(self):
        las_class = [list(CLASSIFICATION_CODES.values()).index(self.cbClassificationCode.currentText())]
        if self.tbInputELC != '' and self.tbOutputELC != '':
            extract_las_class(self.leInputELC.text(), self.leOutputELC.text(), las_class)
        else:
            print('invalid input or output path')


    def __get_cxtp_xyz_input(self):
        input_path = QFileDialog.getOpenFileName(self, "Open XYZ File", "", "XYZ Files (*.xyz)")
        if len(input_path[0]) != 0:
            input_path = input_path[0]
            self.leInputPathCXTP.setText(str(input_path))


    def __get_cxtp_polygon_input(self):
        input_path = QFileDialog.getOpenFileName(self, "Open Shapefile", "", "Shapefile (*.shp)")
        if len(input_path[0]) != 0:
            input_path = input_path[0]
            self.leInputPolygonPathCXTP.setText(str(input_path))


    def __set_cxtp_output(self):
        output_path = QFileDialog.getSaveFileName(self, "Save File", "", "Shapefile (*.shp)")
        if len(output_path[0]) != 0:
            self.leOutputCXTP.setText(str(output_path[0]))


    def __run_clip_xyz_to_polygon(self):
        if self.leInputPathCXTP != '' and self.leInputPolygonPathCXTP != '' and self.leOutputCXTP != '':
            clip_xyz_to_poly(self.leInputPathCXTP.text(), self.leOutputCXTP.text(), self.leInputPolygonPathCXTP.text())
        else:
            print('invalid input or output path')


    def __get_gmh_dem_input(self):
        input_path = QFileDialog.getOpenFileName(self, "Open DEM points Shapefile", "", "Shapefile (*.shp)")
        if len(input_path[0]) != 0:
            input_path = input_path[0]
            self.leDemInputGMH.setText(str(input_path))


    def __get_gmh_dsm_input(self):
        input_path = QFileDialog.getOpenFileName(self, "Open DSM points Shapefile", "", "Shapefile (*.shp)")
        if len(input_path[0]) != 0:
            input_path = input_path[0]
            self.leDsmInputGMH.setText(str(input_path))


    def __get_gmh_shp_input(self):
        input_path = QFileDialog.getOpenFileName(self, "Open polygon Shapefile", "", "Shapefile (*.shp)")
        if len(input_path[0]) != 0:
            input_path = input_path[0]
            self.leShpInputGMH.setText(str(input_path))


    def __set_gmh_output(self):
        output_path = QFileDialog.getSaveFileName(self, "Save File", "", "Shapefile (*.shp)")
        if len(output_path[0]) != 0:
            self.leOutputGMH.setText(str(output_path[0]))


    def __run_get_max_height(self):
        if self.leDemInputGMH != '' and self.leDsmInputGMH != '' and self.leDsmInputGMH != '' and self.leOutputGMH != '':
            get_max_value(self.leShpInputGMH.text(), self.leDemInputGMH.text(), self.leDsmInputGMH.text(), self.leOutputGMH.text())
        else:
            print('invalid input or output path')


    def __set_mf_input(self):
        ...


    def __get_mf_output(self):
        ...


    def __run_merge_files(self):
        ...


    def __get_cf_input(self):
        ...


    def __set_cf_output(self):
        ...


    def __run_convert_files(self):
        ...
