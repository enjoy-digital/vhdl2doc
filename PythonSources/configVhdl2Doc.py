#!/usr/local/bin/python

#===============================================================================
# Author  : F.Kermarrec
# Data    : 14/02/2010
# Purpose : configVhdl2Doc.py
#           Configuration of VHDL2Doc
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

#Python Customs Libs

#=================================
# Version 
#=================================
vhdl2DocVersion = "V0.1.1"
vhdl2DocDate    = "Mon Feb 21 2011"

#=================================
# Options 
#=================================

#=================================
# VHDL Files Directory
#=================================
localPath             = "SampleDesign"
localPathIllustration = "SampleIllustration" 
fileType = "vhd"
pythonSources = "PythonSources"

#=================================
# Design Configuration
#=================================
designCompileCommand = "vhdl work "

#=================================
# Configuration Html
#=================================
docDirHtml      = "Documentation_Html"
docDirLatex     = "Documentation_Latex"
styleDir        = "Style"
sourcesDir      = "Sources"
entitiesDir     = "Entities"
packagesDir     = "Packages"
illustationsDir = "Illustrations"

#=================================
# Configuration Html Style
#=================================
styleFooterButton = "footerBtn.jpg" 


#=================================
# Directories configuration
#    /!\ Don't Touch /!\
#=================================
htmlDocDir        = os.curdir  +"\\"+docDirHtml
latexDocDir       = os.curdir  +"\\"+docDirLatex
styleDocDir       = htmlDocDir +"\\"+styleDir
sourcesDocDir     = htmlDocDir +"\\"+sourcesDir
entitiesDocDir    = htmlDocDir +"\\"+entitiesDir
packagesDocDir    = htmlDocDir +"\\"+packagesDir
illustationDocDir = htmlDocDir +"\\"+illustationsDir




