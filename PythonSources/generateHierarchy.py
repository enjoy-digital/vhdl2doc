#!/usr/local/bin/python

#===============================================================================
# Author  : F.Kermarrec
# Data    : 15/02/2010
# Purpose : generateHierarchy.py
#           Generate Hierarchy between VHDL Files
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

#Python Customs Libs
from configVhdl2Doc    import *
from parseFiles        import *

#Generic Infos Ranks
FILENAME_RK                    = 0
LINENUMBER_RK                  = 1
TYPE_RK                        = 2
TYPE_NAME_RK                   = 3

#Library Infos Ranks                  
LIBRARY_NAME_RK                = 3

#Use Infos Ranks
USE_NAME_RK                    = 3
USE_ENTITY_NAME_RK             = 4

#Entity Infos Ranks
ENTITY_NAME_RK                 = 3

#Entity Signals Infos Ranks
ENTITY_SIGNAL_NAME_RK          = 3
ENTITY_SIGNAL_DIRECTION_RK     = 4
ENTITY_SIGNAL_TYPE_RK          = 5
ENTITY_SIGNAL_ENTITY_NAME_RK   = 6

#Package Infos Ranks
PACKAGE_NAME_RK                = 3

#Function Infos Ranks
FUNCTION_NAME_RK               = 3
FUNCTION_PACKAGE_NAME_RK       = 4

#Architecture Infos Ranks
ARCHITECTURE_NAME_RK           = 3
ARCHITECTURE_ENTITY_NAME_RK    = 4

#Component Infos Ranks
COMPONENT_NAME_RK              = 3
COMPONENT_ARCHITECTURE_NAME_RK = 4
COMPONENT_ENTITY_NAME_RK       = 5

#Instance Infos Ranks
INSTANCE_NAME_RK               = 3
INSTANCE_ENTITY_NAME_RK        = 4

#Process Infos Ranks
PROCESS_NAME_RK                = 3
PROCESS_SENSITIVITY_RK         = 4
PROCESS_ARCHITECTURE_NAME_RK   = 5
PROCESS_ENTITY_NAME_RK         = 6

#Tag Infos Ranks
TAG_TYPE_RK                    = 3
TAG_LINK_TO_TYPE_RK            = 4
TAG_LINK_TO_NAME_RK            = 5
TAG_STRING_RK                  = 6
TAG_IS_VALID_RK                = 7
TAG_FIG_NAME                   = 6
TAG_FIG_FILENAME               = 7

#Hierarchy Infos Ranks
HIERARCHY_NAME_RK               = 0
HIERARCHY_TYPE_RK               = 1
HIERARCHY_ENTITY_NAME_RK        = 2
HIERARCHY_LEVEL_RK              = 3


#Global Variables
designHierarchyFileList = []


#=================================
# findOrfanEntity unction
#=================================
def findOrfanEntity ():

  orfanList = []
  print " Searching possible Top..."
  
  for parseElement in parseInfoReduce:
    
    elementType = parseElement[TYPE_RK]
    
    if elementType == "entity":
      entityName     = parseElement[ENTITY_NAME_RK]
      entityIsOrfan  = True
      
      for findOrfanElement in parseInfoReduce:
        findOrfanElementType     = findOrfanElement[TYPE_RK]
        findOrfanElementFilename = findOrfanElement[FILENAME_RK]
        if  findOrfanElementType == "instance":
            instanceEntity = findOrfanElement[INSTANCE_ENTITY_NAME_RK]
            if instanceEntity == entityName:
              entityIsOrfan = False

      if entityIsOrfan:
        orfanList.append(entityName)
   
  return orfanList
  
#=================================
# selectOrfanEntity Function
#=================================
def selectOrfanEntity (orfanList):
  #Show Orfans
  print " found:"    
  for orfanElement in orfanList:
    print " - " + orfanElement
  
  #Select Orfan Top
  top = raw_input(' Which one would you want to build? :')
  validChoice = False
  while not validChoice:
    for orfanElement in orfanList:
      if orfanElement == top:
        validChoice = True
    if not validChoice:
      top = raw_input(' Incorrect, Retry! :')
  
  return top
  
#=================================
# retrieveFilenameElement
#=================================
def retrieveFilenameElement(parseInfo,elType,elName):

  #Retrieve File Name 
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == elType:
      elementName = parseElement[TYPE_NAME_RK]
      if str.upper(elementName) == str.upper(elName):
        elementFilename = parseElement[FILENAME_RK]  
        return elementFilename
  return "" 
  
       
#=================================
# compareString
#=================================
def compareString(string1,string2):
  return str.upper(string1) == str.upper(string2)

  
#=================================
# findDesignHierarchy
#=================================
def findDesignHierarchy(designEntity,currentLevel):

  #Search Direct 
  if currentLevel == 0:
    print " Searching hierarchy of %s ..." %(designEntity)
  
  #Retrieve File Name
  designEntityFilename = retrieveFilenameElement(parseInfoReduce,"entity",designEntity)
    
  #=================
  #Search Packages
  #=================
  
  #Find Corresponding Packages
  for parseInfoElement in parseInfoReduce:
    elementFilename = parseInfoElement[FILENAME_RK]
    elementType     = parseInfoElement[TYPE_RK]
    if compareString(elementFilename,designEntityFilename):
      if elementType == "use":
        designHierarchyFileList.append([parseInfoElement[USE_NAME_RK],"package",designEntity,currentLevel])
  
  #=================
  #Search Instances
  #=================
  
  #Find Corresponding Instances
  for parseInfoElement in parseInfoReduce:
    elementFilename = parseInfoElement[FILENAME_RK]
    elementType     = parseInfoElement[TYPE_RK]
    
    if compareString(elementFilename,designEntityFilename):
      if elementType == "instance":
        designHierarchyFileList.append([parseInfoElement[USE_ENTITY_NAME_RK],"instance",designEntity,currentLevel])
        findDesignHierarchy(parseInfoElement[USE_ENTITY_NAME_RK],currentLevel+1)

        
#=================================
# isEntityLinkTo
#=================================
def isEntityLinkTo(designEntity):

  entityIsLinkTo = False

  #Find if at least one entity is link to current entity
  for listElement in designHierarchyFileList:
    if str.upper(listElement[HIERARCHY_ENTITY_NAME_RK]) == str.upper(designEntity):
      entityIsLinkTo = True
      
  return entityIsLinkTo
  
#=================================
# listDesignFilesOrdered
#=================================
def listDesignFilesOrdered(fileList,designFileList):
  
  designFileListOrdered = []

  #Find in fileList designFileList Elements
  for fileListElement in fileList:
    for designFileListElement in designFileList:
      if fileListElement == designFileListElement:
        designFileListOrdered.append(fileListElement)
        
  #return List
  return designFileListOrdered
  
#=================================
# listDataTag
#=================================
def listDataTag(tagType,tagName,tagFilename):

  #Create empty List
  dataTagList = []  
  
  
  #Search corresponding Tag
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    elementFilename = parseElement[FILENAME_RK]
    if (elementType == "tag" and elementFilename == tagFilename):
      if parseElement[TAG_LINK_TO_TYPE_RK] == tagType:
        if parseElement[TAG_LINK_TO_NAME_RK] == tagName:
          elementTagType        = parseElement[TAG_TYPE_RK]
          elementTagString      = parseElement[TAG_STRING_RK]
          elementTagIsValid     = parseElement[TAG_IS_VALID_RK]
          elementTagFigName     = parseElement[TAG_FIG_NAME]
          elementTagFigFilename = parseElement[TAG_FIG_FILENAME]
          
          dataTagList.append([elementTagType,elementTagString,elementTagIsValid,elementTagFigName,elementTagFigFilename])

  return dataTagList

#=================================
# listLibrary
#=================================
def listLibrary(entityFilename):

  libraryList = []

  for parseInfoElement in parseInfoReduce:
    
    elementType = parseInfoElement[TYPE_RK]
    
    #If it's a Library
    if elementType == "library":
    
      libraryName     =  parseInfoElement[LIBRARY_NAME_RK]
      libraryFilename =  parseInfoElement[FILENAME_RK]
       
      if compareString(libraryFilename,entityFilename):
      
        libraryList.append(["library",libraryName,"",""])
    
    #If it's a Use
    elif elementType == "use":
    
      useName     =  parseInfoElement[USE_NAME_RK]
      useFilename =  parseInfoElement[FILENAME_RK]
     
      if compareString(useFilename,entityFilename):
      
        #Find if library is in design
        libraryIsInDesign = False
        testUseName = str.replace(useName,libraryName+".","")
        testUseName = str.replace(testUseName,".all","")
        
        
        for testParseElement in parseInfoReduce:
          if testParseElement[TYPE_RK] == "package":
            if testUseName == testParseElement[PACKAGE_NAME_RK]:
              libraryIsInDesign = True
        
        libraryList.append(["use",useName,testUseName,libraryIsInDesign])

  return libraryList
  
#=================================
# listSignal
#=================================
def listSignal(entityName):

  signalList = []

  for parseInfoElement in parseInfo:
    elementType = parseInfoElement[TYPE_RK]
    
    #If it's a Signal
    if elementType == "entitySignal":
      
      entitySignalName        =  parseInfoElement[ENTITY_SIGNAL_NAME_RK]
      entitySignalDirection   =  parseInfoElement[ENTITY_SIGNAL_DIRECTION_RK]
      entitySignalType        =  parseInfoElement[ENTITY_SIGNAL_TYPE_RK]      
      entitySignalEntityName  =  parseInfoElement[ENTITY_SIGNAL_ENTITY_NAME_RK] 
      
      if compareString(entityName,entitySignalEntityName):
      
        signalList.append([entitySignalName,entitySignalDirection,entitySignalType])
      
  return signalList
  
#=================================
# listArchitecture
#=================================
def listArchitecture(entityName):

  architectureList = []

  for parseInfoElement in parseInfo:
    elementType = parseInfoElement[TYPE_RK]
    
    #If it's an Architectue
    if elementType == "architecture":
      architectureName         =  parseInfoElement[ARCHITECTURE_NAME_RK]
      architectureEntityName    =  parseInfoElement[ARCHITECTURE_ENTITY_NAME_RK]
      
      if compareString(entityName,architectureEntityName):
        architectureList.append(architectureName)
          
  return architectureList
  
#======================================
# GenerateHierarchyProtovis Function
#======================================
def generateHierarchyProtovis(designHierarchyFileList):
  
  #Open File
  fh = open(htmlDocDir+'\hierarchy.js', 'w+')
  
  #Define hierarchy variable
  print >> fh, "var hierarchy = {"
  
  #Show designEntity
  print >> fh, "%s:{"%(designEntity)
  
  #Initialize
  levelLast = 0;
  firstLoop = True
  
  #Loop on designHierarchyFileList
  for designHierarchyElement in designHierarchyFileList:
  
    #Exception on first Loop
    if firstLoop == False:
      #If Same Level "," to indicate next
      if levelLast == designHierarchyElement[HIERARCHY_LEVEL_RK]:
        print >> fh, ","
      #If last Level > current Level, close bracket(s)
      elif levelLast > designHierarchyElement[HIERARCHY_LEVEL_RK]:
        for i in range(levelLast-designHierarchyElement[HIERARCHY_LEVEL_RK]):
          print >> fh, "},"
    
    firstLoop = False
    
    #Indent Elements   
    for i in range(designHierarchyElement[HIERARCHY_LEVEL_RK]+1):
      print >> fh, "    ",
  
    #If Package
    if designHierarchyElement[HIERARCHY_TYPE_RK] == "package":
      #Suppress "."
      print >> fh, "%s : 1"%str.replace(designHierarchyElement[HIERARCHY_NAME_RK],".","_"),
    
    #If Instance
    elif designHierarchyElement[HIERARCHY_TYPE_RK] == "instance":
      
      #If Instance entity is link to others entity
      if isEntityLinkTo(designHierarchyElement[HIERARCHY_NAME_RK]):
        #Open bracket
        print >> fh, "%s : {" %designHierarchyElement[HIERARCHY_NAME_RK]
      else:
        #Show  Instance as Std Element
        print >> fh, "%s : 1" %(designHierarchyElement[HIERARCHY_NAME_RK]),
    
    #Update Last Level
    levelLast = designHierarchyElement[HIERARCHY_LEVEL_RK]
    
  #Close level brackets
  for i in range(levelLast+1):
    print >> fh, "}"
  
  #Close last brackets
  print >> fh, "};"
  
  #Close file
  fh.close()  
