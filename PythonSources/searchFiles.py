#!/usr/local/bin/python

#===============================================================================
# Author  : F.Kermarrec
# Data    : 14/02/2011
# Purpose : searchFiles.py
#           Files search functions
#===============================================================================
# Copyright (c) 2011  Enjoy-Digital Florent Kermarrec <florent@enjoy-digital.fr>  
#  
#  This file is free software: you may copy, redistribute and/or modify it  
#  under the terms of the GNU General Public License as published by the  
#  Free Software Foundation, either version 2 of the License, or (at your  
#  option) any later version.  
#  
#  This file is distributed in the hope that it will be useful, but  
#  WITHOUT ANY WARRANTY; without even the implied warranty of  
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU  
#  General Public License for more details.  
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  
#===============================================================================

#=================================
# Import of useful libs
#=================================
#Python Standard Libs
import os

#=================================
# dirEntries Function
#=================================
def dirEntries(dir_name, subdir, *args):
    '''Return a list of file names found in directory 'dir_name'
    If 'subdir' is True, recursively access subdirectories under 'dir_name'.
    Additional arguments, if any, are file extensions to match filenames. Matched
        file names are added to the list.
    If there are no additional arguments, all files found in the directory are
        added to the list.
    Example usage: fileList = dirEntries(r'H:\TEMP', False, 'txt', 'py')
        Only files with 'txt' and 'py' extensions will be added to the list.
    Example usage: fileList = dirEntries(r'H:\TEMP', True)
        All files and all the files in subdirectories under H:\TEMP will be added
        to the list.
    '''
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            if not args:
                fileList.append(dirfile)
            else:
                if os.path.splitext(dirfile)[1][1:] in args:
                    fileList.append(dirfile)
        # recursively access file names in subdirectories
        elif os.path.isdir(dirfile) and subdir:
            fileList.extend(dirEntries(dirfile, subdir, *args))
    return fileList
    
#=================================
# searchVhdlFiles Function
#=================================
def searchVhdlFiles(dir_name):
  print("-=====================================================================-")
  print(" Start Searching VHDL files...")
  print("-=====================================================================-")
  return dirEntries(dir_name,True,'vhd')


#=================================
# deletePyVhdlFiles Function
#=================================
def deletePyVhdlFiles(fileList):
  tmpFileList = []
  for fileElt in fileList:
    if ".py.vhd" not in fileElt:
      tmpFileList.append(fileElt)
  return tmpFileList