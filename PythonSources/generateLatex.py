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
  print("%--------------------------------------------------", file=p_file)
  print("% Generation automatique de la documentation       ", file=p_file)
  print("% Projet :"+projectName, file=p_file)
  print("%--------------------------------------------------", file=p_file)
  print("", file=p_file)
  print("%--------------------------------------------------", file=p_file)
  print("% Configuration Latex du document", file=p_file)
  print("\\documentclass[a4paper]{article}", file=p_file)
  print("\\usepackage[latin1]{inputenc}", file=p_file)
  print("\\usepackage[T1]{fontenc}", file=p_file)
  print("\\usepackage{geometry}", file=p_file)
  print("\\usepackage[francais]{babel}", file=p_file)
  print("\\usepackage[pdftex]{graphicx}", file=p_file)
  print("\\usepackage[nottoc, notlof, notlot]{tocbibind}", file=p_file)
  print("\\usepackage{fancyhdr}", file=p_file)
  print("\\pagestyle{fancy}", file=p_file)
  print("%--------------------------------------------------", file=p_file)
  print("", file=p_file)
  
#=====================================
# generateFrontPageLatex Function
#=====================================
def generateFrontPageLatex(p_file):

  projectName   = "FPGA DEMO"
  projectAuthor = "Florent Kermarrec"
  
  #Front Page
  print("%--------------------------------------------------", file=p_file)
  print("% Front Page", file=p_file)
  print("\\title{\\textbf{%s}}" %projectName, file=p_file)
  print("\\author{%s}" %projectAuthor, file=p_file)
  print("\\begin{document}", file=p_file) 
  print("\\maketitle", file=p_file)
  print("%--------------------------------------------------", file=p_file)
  print("", file=p_file)
  
#=====================================
# generateEmptyPageLatex Function
#=====================================
def generateEmptyPageLatex(p_file):

  #Empty Page
  
  print("%--------------------------------------------------", file=p_file)
  print("% Page Vierge", file=p_file)
  print("\\newpage", file=p_file)
  print("%--------------------------------------------------", file=p_file)
  print("", file=p_file)
  
#=======================================
# generateTableOfContentsLatex Function
#=======================================
def generateTableOfContentsLatex(p_file):
  
  #Empty Page
  print("%--------------------------------------------------", file=p_file)
  print("% Table of contents", file=p_file)
  print("\\newpage", file=p_file)
  print("\\vspace{20mm}", file=p_file)
  print("\\tableofcontents", file=p_file)
  print("%--------------------------------------------------", file=p_file)
  print("", file=p_file)

#=======================================
# generateListOfFiguresLatex Function
#=======================================
def generateListOfFiguresLatex(p_file):
  
  #Empty Page
  print("%--------------------------------------------------", file=p_file)
  print("% List of figures", file=p_file)
  print("\\newpage", file=p_file)
  print("\\vspace{20mm}", file=p_file)
  print("\\listoffigures", file=p_file)
  print("%--------------------------------------------------", file=p_file)
  print("", file=p_file) 
  

#=====================================
# generateEndLatex Function
#=====================================
def generateEndLatex(p_file):
  
  #Configuration
  print("\\end{document}", file=p_file)
  
  
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
  
   
