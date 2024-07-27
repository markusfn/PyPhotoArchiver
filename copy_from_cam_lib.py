#/usr/bin/python3
#===============================================================================
#
#  Name: copy_from_cam_lib.py
#
#  Description:
#
#
#
#
from __future__ import division
__author__ = "Markus Faust (markus.faust@t-online.de)"
__version__ = "1.1.0"
__date__ = "$Date: 27.07.2024 11:22:50 $"
__copyright__ = "Copyright (c) 2024 Markus Faust"
__license__ = "MIT license"
#
#===============================================================================
#...5...10....5...20....5...30....5...40....5...50....5...60....5...70....5...80....5...90
# History:
# V 1.0.0, 24.07.2024: initial version
# V 1.1.0, 27.07.2024: added function ReadExifDdata extract
#                      Exif metadata from digital image files

import os, string, shutil, time, exifread, datetime

def FindAllExtensionsInDir(files):
    ext_list = []
    for f in files:
        words = f.split('.')
        ext = words[-1]
        if ext not in ext_list:
            ext_list.append(ext)
    return ext_list


def HandleCamFileNames(filename, camera_abrev, iskip):
    '''Takes filename of camerra file which typically is something like
    name.ext, splits it into parts separated by a dot,
    skips iskip characters of words[0], adds a new abbreviation for the camera
    and puts it together again.'''
    words = filename.split(".")
    fnew = camera_abrev + words[0][iskip:]
    nw = len(words)
    for i in range(1,nw):
        fnew = fnew + "." + words[i]
    return fnew

def creation_modification_date_(file):
    '''extract creation date and modification date of file and
    return as string'''
    ct = os.path.getctime(file) # creation date and time
    mt = os.path.getmtime(file) # modification date and time
    dt_ct = datetime.datetime.fromtimestamp(ct)
    mt_ct = datetime.datetime.fromtimestamp(mt)
    dts = dt_ct.strftime("%Y%m%d")
    mts = mt_ct.strftime("%Y%m%d")
    return dts, mts

def CheckIfDirIsEmpty(ppath, text):
    '''check if directory is empty and raise an error if not.'''
    dir_name = ppath
    if os.path.isdir(dir_name):
        if not os.listdir(dir_name):
            print("Directory ", ppath," is empty")
        else:
            print("Directory ", ppath," is not empty")
    else:
        print("Given directory",ppath," doesn't exist")
    return

def CopyFileInDir(source_dir, source_fname, new_dir, new_fname):
    '''shell command to copy file in directory of the day it was created.'''
    if os.path.exists(new_dir):
        src = os.path.join(source_dir, source_fname)
        dst = os.path.join(new_dir, new_fname)
        shutil.copyfile(src, dst)
    else:
        os.makedirs(new_dir)
        src = os.path.join(source_dir, source_fname)
        dst = os.path.join(new_dir, new_fname)
        shutil.copyfile(src, dst)

def ReadExifDdata(file):
    '''extract Exif metadata from digital image files,
    supported formats: TIFF, JPEG, PNG, Webp, HEIC using ExifRead
    (see https://pypi.org/project/ExifRead/);
    returns date, i.e. in format 20240715 and exif tags
    '''
    tags = exifread.process_file(file)
    dts = tags['EXIF DateTimeDigitized'].values
    [Y, M, D] = dts.split()[0].split(':')
    CreateDate = Y + M + D
    return CreateDate, tags
