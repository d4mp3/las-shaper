# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LasShaper
                                 A QGIS plugin
 Plugin for las files.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-04-17
        copyright            : (C) 2023 by d4mp3
        email                : pszdam@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LasShaper class from file LasShaper.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .las_shaper import LasShaper
    return LasShaper(iface)
