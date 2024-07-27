#/usr/bin/python3
#===============================================================================
#
#  Name: PyPhotoArchiver.py
#
#  Description:
#
#
#
#
from __future__ import division
__author__ = "Markus Faust (markus.faust@t-online.de)"
__version__ = "1.0.0"
__date__ = "$Date: 24.07.2024 16:50:32 $"
__copyright__ = "Copyright (c) 2024 Markus Faust"
__license__ = "MIT license"
#
#===============================================================================
#...5...10....5...20....5...30....5...40....5...50....5...60....5...70....5...80....5...90
# History:
# V 1.0.0, 24.07.2024: initial version

import os, string, shutil, time, exifread, datetime
from copy_from_cam_lib import *

# Set these 2 parameters to suit your camera
camera_abrev = 'Pxl7'
iskip = 3

dir_abrev = camera_abrev
if camera_abrev == '':
    dir_abrev = 'cam'

actpath = os.getcwd()

F_dir = os.path.join(actpath, 'tmp_photos')
files = os.listdir(F_dir)
os.chdir(F_dir)
ext_list = FindAllExtensionsInDir(files)

ext_dict = {}
for ext in ext_list:
    ext_dict[ext] = []
for f in files:
    words = f.split('.')
    ext_f = words[-1]
    ext_dict[ext_f].append(f)

for ext in ext_list:
    print('\n','The following files with extension ', ext, ' are copied')
    k = 0
    for f in ext_dict[ext]:
        k = k+1
        dts, mts = creation_modification_date_(f)
        fnew = HandleCamFileNames(f, camera_abrev, iskip)
        new_dir = dir_abrev + '-' + mts
        DirOfFile = os.path.join(actpath, 'sorted', new_dir)
        CopyFileInDir(F_dir, f, DirOfFile, fnew)
        print(k, f, fnew, mts)
