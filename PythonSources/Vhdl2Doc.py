#!/usr/local/bin/python

#===============================================================================
# Author  : F.Kermarrec
# Data    : 14/02/2010
# Purpose : Vhdl2Doc.py
#           Main of VHDL2Doc
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
import sys
import os
from optparse import OptionParser

#Python Customs Libs
from configVhdl2Doc    import *
from searchFiles       import *
from parseFiles        import *
from generateHierarchy import *
from generateHtml      import *
from generateLatex     import *

#=================================
# VHDL2Doc Program arguments
#=================================
parser = OptionParser()
parser.add_option("-t","--top",dest="designEntity", help ="Vhdl2Doc Top Entity",metavar="designEntity")
parser.add_option("-v","--verbose",dest="verboseMode",action="store_false", help ="Verbose Mode On")
parser.add_option("-f","--force",dest="forceMode",action="store_false", help ="Force Generation on Errors in Parsing")
(options, args) = parser.parse_args()

print options.designEntity


#Get Design Top Entity if defined
if options.designEntity == None:
  designEntitySelect = True
else:
  designEntity = options.designEntity
  designEntitySelect = False
  
#Get Verbose Mode
if options.verboseMode == None:
  verboseMode = False
else:
  verboseMode = True

#Get Verbose Mode
if options.forceMode == None:
  forceMode = False
else:
  forceMode = True  

#=================================
# Search VHDL Files in Directory
#=================================
globalPath = os.curdir + "\\" + localPath

#Recursive Search of Files
fileList = searchVhdlFiles(globalPath)

#=================================
# Parse VHDL Files
#=================================
errorParse = parseVhdlFiles(fileList,verboseMode)

if (errorParse == 0 or forceMode == True):

  #=================================
  # Find Hierarchy in VHDL Files
  #=================================

  print "-=====================================================================-"              
  print " Start scrunching and twisting all VHDL Data together..."
  print "-=====================================================================-"
  #Find Orfan Entities
  orfanList = findOrfanEntity()

  #Select designEntity
  if designEntitySelect:  designEntity = selectOrfanEntity(orfanList)

  #Find Design Hierarchy
  findDesignHierarchy(designEntity,0)

  #=================================
  # Generate Html Documentation
  #=================================
  print "-=====================================================================-"              
  print " Start Html Generation..."
  print "-=====================================================================-"

  #Prepare Directories
  prepareHtmlDir(designEntity)

  #Generate Index   
  generateHomeHtml(designEntity,designHierarchyFileList)

  #Generate Utils
  designFileList = generateUtilsHtml(designEntity,designHierarchyFileList)

  #Generate Entities
  generateEntitiesListHtml(designFileList,"work",globalPath)

  #Generate Packages
  generatePackageListHtml(designFileList,"work",globalPath)

  #Generate Documentation
  generateDocumentationHtml()

  #Generate Sources List & Highlight
  generateSourcesListHtml(fileList,designFileList,globalPath)
  generateSourcesHighlightHtml(designFileList)

  #Generate About  
  generateAboutHtml()


  #=================================
  # Generate Latex Documentation
  #=================================
  print "-=====================================================================-"              
  print " Start Latex Generation..."
  print "-=====================================================================-"
  generateDocumentationLatex("documentationLatex.tex")