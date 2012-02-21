#!/usr/local/bin/python

#===============================================================================
# Author  : F.Kermarrec
# Data    : 25/02/2011
# Purpose : generateLatex.py
#           Generate Documentation in Latex
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
import re
import sys
import time
import datetime
from shutil import copytree,rmtree
from configVhdl2Doc    import *
from parseFiles        import *                 
from generateHierarchy import * 

global styleDir


#=================================
# prepareLatexDir Function
#=================================
def prepareLatexDir():

  #Create all Directory & copy Style File
  dirList = []
  dirList.append(latexDocDir)
  
  #Create Directories,SubDirectories&Style Dir
  for dirElement in dirList:
  
    #Create directory
    if not os.path.exists(dirElement):
     os.makedirs(dirElement)       

#=====================================
# generateConfigurationLatex Function
#=====================================
def generateConfigurationLatex(p_file):

  projectName = "FPGA_DEMO"
  
  #Configuration
  print >> p_file, "%--------------------------------------------------"
  print >> p_file, "% Generation automatique de la documentation       "
  print >> p_file, "% Projet :"+projectName
  print >> p_file, "%--------------------------------------------------"
  print >> p_file, ""
  print >> p_file, "%--------------------------------------------------"
  print >> p_file, "% Configuration Latex du document"
  print >> p_file, "\\documentclass[a4paper]{article}"
  print >> p_file, "\\usepackage[latin1]{inputenc}"
  print >> p_file, "\\usepackage[T1]{fontenc}"
  print >> p_file, "\\usepackage{geometry}"
  print >> p_file, "\\usepackage[francais]{babel}"
  print >> p_file, "\\usepackage[pdftex]{graphicx}"
  print >> p_file, "\\usepackage[nottoc, notlof, notlot]{tocbibind}"
  print >> p_file, "\\usepackage{fancyhdr}"
  print >> p_file, "\\pagestyle{fancy}"
  print >> p_file, "%--------------------------------------------------"
  print >> p_file, ""
  
#=====================================
# generateFrontPageLatex Function
#=====================================
def generateFrontPageLatex(p_file):

  projectName   = "FPGA DEMO"
  projectAuthor = "Florent Kermarrec"
  
  #Front Page
  print >> p_file, "%--------------------------------------------------"
  print >> p_file, "% Front Page"
  print >> p_file, "\\title{\\textbf{%s}}" %projectName
  print >> p_file, "\\author{%s}" %projectAuthor
  print >> p_file, "\\begin{document}" 
  print >> p_file, "\\maketitle"
  print >> p_file, "%--------------------------------------------------"
  print >> p_file, ""
  
#=====================================
# generateEmptyPageLatex Function
#=====================================
def generateEmptyPageLatex(p_file):

  #Empty Page
  
  print >> p_file,"%--------------------------------------------------"
  print >> p_file,"% Page Vierge"
  print >> p_file,"\\newpage"
  print >> p_file,"%--------------------------------------------------"
  print >> p_file,""
  
#=======================================
# generateTableOfContentsLatex Function
#=======================================
def generateTableOfContentsLatex(p_file):
  
  #Empty Page
  print >> p_file,"%--------------------------------------------------"
  print >> p_file,"% Table of contents"
  print >> p_file,"\\newpage"
  print >> p_file,"\\vspace{20mm}"
  print >> p_file,"\\tableofcontents"
  print >> p_file,"%--------------------------------------------------"
  print >> p_file,""

#=======================================
# generateListOfFiguresLatex Function
#=======================================
def generateListOfFiguresLatex(p_file):
  
  #Empty Page
  print >> p_file,"%--------------------------------------------------"
  print >> p_file,"% List of figures"
  print >> p_file,"\\newpage"
  print >> p_file,"\\vspace{20mm}"
  print >> p_file,"\\listoffigures"
  print >> p_file,"%--------------------------------------------------"
  print >> p_file,"" 
  

#=====================================
# generateEndLatex Function
#=====================================
def generateEndLatex(p_file):
  
  #Configuration
  print >> p_file,"\\end{document}"
  
  
#=====================================
# generateDocumentationLatex Function
#=====================================
def generateDocumentationLatex(latexFilename):
  
  prepareLatexDir()
  
  #Open File
  f = open(os.path.join(latexDocDir,latexFilename), 'w+')
  
  generateConfigurationLatex(f)
  generateFrontPageLatex(f)
  generateEmptyPageLatex(f)
  generateTableOfContentsLatex(f)
  generateListOfFiguresLatex(f)
  generateEndLatex(f)
  
  #Close File
  f.close()
  
   
