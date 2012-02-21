#!/usr/local/bin/python

#===============================================================================
# Author  : F.Kermarrec
# Data    : 14/02/2011
# Purpose : parseFiles.py
#           Parser for VHDL Files
#===============================================================================

#=================================
# Import of useful libs
#=================================
#Python Standard Libs
import os
import re
import sys
import logging  

#Generic Infos Ranks
FILENAME_RK                    = 0
LINENUMBER_RK                  = 1
TYPE_RK                        = 2
TYPE_NAME_RK                   = 3


#=================================
# Global Variables
#=================================
parseInfo = []
parseInfoReduce = []
parseStat = []

#=================================
# Global Variables
#=================================
logging.basicConfig(filemode='w',filename='parse.log',format='%(levelname)s:%(message)s', level=logging.DEBUG)


#=================================
# parseFiles Function
#=================================
def parseVhdlFiles(fileList,mode):

  verboseMode = mode

  #Return Parse Informations from a VHDL File List
  fileNumber = 0
  errorNumber = 0
  lineNumber             = 0
  totalCommentLineNumber = 0
  totalTagLineNumber     = 0
  totalLineNumber        = 0
  totalErrorNumber       = 0
  totalEntityNumber      = 0
  totalFunctionNumber    = 0
  totalProcessNumber     = 0
  
    
  print "-=====================================================================-"
  print " Start Parsing VHDL files..."
  print "-=====================================================================-"
  
  
  #===============
  # VHDL File Loop
  #===============
  for vhdlFile in fileList:
    
    #Calc Stats
    fileNumber = fileNumber + 1
    lineNumber       = 0
    errorNumber      = 0
    
    #===============
    # File Line Loop
    #===============
    with open(vhdlFile) as p_vhdlFile:
    
      #Init
      isInEntity       = False
      isInPackage      = False
      isInArchitecture = False
      isAfterArchitectureBegin = False
      isInProcess      = False
      libraryName      = ""
      entityName       = ""
      packageName      = ""
      architectureName = ""
      instanceName     = ""
      instanceEntity   = ""
      instanceNotSure  = False
      processName      = ""
      processSensitivity = ""
      
      #Tag
      commentTag       = ""
      linkTagType      = ""
      linkTagName      = ""
      titleTag         = ""
      briefTag         = ""
      detailsTag       = ""
      figTagName       = ""
      figTagFilename   = ""
      
      linkToType  = ""
      linkToName  = ""
      commentType = ""
      
      briefIsValid   = False
      detailsIsValid = False
      
      #Message
      
      logging.debug(" Parsing file %s..." %(vhdlFile))
      logging.debug("------------------------------------------------------------------")
    
      for line in p_vhdlFile:
      
         ############################
         # Very Basic Line Analysis
         ############################
             
         #===============
         # Line Analysis
         #===============
         continueLineAnalysis = True
                    
         #Is it a Comment Line? (--)
         isCommentLine = False
         if  re.search('^ *--*',line,re.I):
           isCommentLine = True
           totalCommentLineNumber = totalCommentLineNumber + 1
         if isCommentLine:
           continueLineAnalysis = False
         
         #====================
         # Tag Line Analysis?  
         #====================
         isTagLine = False
         
         #Is it a Tag Comment Line (--*)  
         if  re.search('^ *--\*',line,re.I):
           isTagLine = True
           totalTagLineNumber = totalTagLineNumber + 1
         if isTagLine:
           continueLineAnalysis = False 
           
         #======================================================================
         # Analysis of Tag Line  
         #======================================================================
         #==================================
         #Search for "--* xxx"
         #==================================
         commentTagLineFound = False
         
         if isTagLine == True:
          if  not re.search('^ *--\* *@',line,re.I):
            m=re.match('^ *--\* *(.+)',line,re.I)
            commentTag = m.group(1)
            commentTagLineFound = True
            logging.debug("%05d: Found Comment Tag" %(lineNumber))
         
         #==================================
         #Search for "--* @link [xxx] [xxx]"
         #==================================
         linkTagLineFound = False
         
         if isTagLine == True:
            m = re.search('^ *--\* *@link +\[([A-Za-z0-9_]+)\] +\[([A-Za-z0-9_]+)\]',line,re.I)
            if m is not None:
              linkTagType = m.group(1)
              linkTagName = m.group(2)
              linkTagLineFound = True
              logging.debug("%05d: Found Link Tag %s %s" %(lineNumber,linkTagType,linkTagName))

         #==================================
         #Search for "--* @title xxx"
         #==================================
         titleTagLineFound = False
         
         if isTagLine == True:
           m = re.search('^ *--\* *@title *(.+)',line,re.I)
           if m is not None:
             titleTag = m.group(1)
             titleTagLineFound = True
             logging.debug("%05d: Found Title Tag" %(lineNumber))
         
         #==================================
         #Search for "--* @brief xxx"
         #==================================
         briefTagLineFound = False
         
         if isTagLine == True:
          m = re.search('^ *--\* *@brief *(.+)',line,re.I)
          if m is not None:
            briefTag = m.group(1)
            briefTagLineFound = True
            logging.debug("%05d: Found Brief Tag" %(lineNumber))
                    
         #==================================
         #Search for "--* @details xxx"
         #==================================
         detailsTagLineFound = False
         
         if isTagLine == True:
           m = re.search('^ *--\* *@details *(.+)',line,re.I)
           if m is not None:
             detailsTag = m.group(1)
             detailsTagLineFound = True
             logging.debug("%05d: Found Details Tag" %(lineNumber))
         
         #==================================
         #Search for "--* @fig [xxx] [xxx]"
         #==================================
         figTagLineFound = False
         
         if isTagLine == True:
           m = re.search('^ *--\* *@fig +\[([A-Za-z0-9_: ]+)\] +\[([A-Za-z0-9_.]+)\]',line,re.I)
           if m is not None:
             figTagName     = m.group(1)
             figTagFilename = m.group(2)
             figTagLineFound = True
             logging.debug("%05d: Found Fig Tag %s" %(lineNumber,figTagName))

              
         #======================================================================
         # Analysis of VHDL Line  
         #======================================================================  
                 
         #========================
         # Comments Suppress
         #========================  
         if continueLineAnalysis:
          commentIndex = line.find('--',0,len(line)-1)
          if  commentIndex >= 0:
            line = line[0:commentIndex]
        
        
         #========================
         #Seach for "library xxx;"
         #========================
         libraryLineFound = False
         
         if continueLineAnalysis:
           m=re.search('^ *library +([A-Za-z0-9]+) *; *',line,re.I)
           if m is not None:
             libraryName      = m.group(1)
             libraryLineFound = True
             continueLineAnalysis = False
             logging.debug("%05d: Found Library %s" %(lineNumber,libraryName))
         
         #=======================
         #Seach for "use xxx.xxx"
         #=======================
         useLineFound = False
         
         if continueLineAnalysis:
           m=re.search('^ *use *([A-Za-z0-9_]+\.[A-Za-z0-9_]+\.[A-Za-z0-9_]+) *; *',line,re.I)
           if m is not None:
             useName      = m.group(1)
             useLineFound = True
             logging.debug("%05d: Found Use %s" %(lineNumber,useName))
              
         #=========================     
         #Seach for "entity xxx is"
         #=========================
         entityStartFound = False
         entityEndFound   = False
         entityLineFound  = False
         
         #Search for Entity Start
         if continueLineAnalysis:
           m=re.search('^ *entity *([A-Za-z0-9_]+) *is *',line,re.I) 
           if m is not None:
             entityName      = m.group(1)
             entityStartFound = True
             totalEntityNumber = totalEntityNumber + 1 ;
              
         entitySignalLineFound = False
              
         #Search for Entity Signals
         if continueLineAnalysis:
           if isInEntity:
             m=re.search('^ *([A-Za-z0-9_]+) +: +([inout]+) +([A-Za-z0-9_ ()\-\*]+);*',line,re.I)
             if m is not None:
               entitySignalName      = m.group(1)
               entitySignalDirection = m.group(2)
               entitySignalType      = m.group(3)
               entitySignalLineFound = True
               logging.debug("%05d: Found Entity Signal %s " %(lineNumber,entitySignalName))
              
         #Search for Entity End
         if continueLineAnalysis:
           m=re.search('^ *end +([A-Za-z0-9_]+) *; *',line,re.I)
           if m is not None:
             if entityName == m.group(1):
               entityEndFound = True
                
         #Entity Error Handling
         #Start Entity Detection while in entity
         if entityStartFound:
           if isInEntity:
              logging.error("/!\\Error/!\\ - file:%s line:%d Entity declaration found while already in!" %(vhdlFile,lineNumber))
              errorNumber = errorNumber + 1
           else:
              isInEntity = True
              entityLineFound = True
              if verboseMode:
               logging.debug("%05d: Found Entity %s" %(lineNumber,entityName))
         if entityEndFound:
           isInEntity = False 
           
         #=========================     
         #Seach for "package xxx is"
         #=========================
         packageStartFound = False
         packageEndFound   = False
         packageLineFound  = False
         
         #Search for Package Start
         if continueLineAnalysis:
           m=re.match('^ *package *([A-Za-z0-9_]+) *is *',line,re.I)
           if m is not None:
             packageName      = m.group(1)
             packageStartFound = True
         
         #Search for Package End
         if continueLineAnalysis:
           m=re.match('^ *end +([A-Za-z0-9_]+) *; *',line,re.I)
           if m is not None:
             if packageName == m.group(1):
               packageEndFound = True
                
         #Package Error Handling
         #Start Package Detection while in entity
         if packageStartFound:
           if isInPackage:
              logging.error(" /!\\Error/!\\ - file:%s line:%d Package declaration found while already in!" %(vhdlFile,lineNumber))
              errorNumber = errorNumber + 1
           else:
              isInPackage = True
              packageLineFound = True
              logging.debug("%05d: Found Package %s" %(lineNumber,packageName))
         if packageEndFound:
           isInPackage = False
           
         #=============================     
         #Seach for "function xxx(xxx)"
         #=============================
         functionLineFound = False
         
         if continueLineAnalysis:
           if isInPackage: 
             m=re.search('^ *function +([A-Za-z0-9_]+)\( *',line,re.I)
             if m is not None:
               functionName      = m.group(1)
               functionLineFound = True
               totalFunctionNumber = totalFunctionNumber + 1 ;
               logging.debug("%05d: Found Function %s" %(lineNumber,functionName))
  
         #======================================     
         #Search for "architecture xxx of xxx is"
         #======================================
         architectureStartFound = False
         architectureBeginFound = False
         architectureEndFound   = False
         architectureLineFound  = False
         
         #Search for Architecture Start
         if continueLineAnalysis:
           m=re.search('^ *architecture *([A-Za-z0-9_]+) +of +([A-Za-z0-9_]+) +is *',line,re.I)
           if m is not None:
             if entityName == m.group(2):  
               architectureName  = m.group(1)
               architectureStartFound = True
                
         #Search for Architecture Begin
         if continueLineAnalysis:
           if  re.search('^ *begin *',line,re.I):
              if  isInArchitecture :
                architectureBeginFound = True
                
                
         #Search for Architecture End
         if continueLineAnalysis:
           m=re.search('^ *end *([A-Za-z0-9_]+) *; *',line,re.I)
           if m is not None:
             if architectureName == m.group(1):
               architectureEndFound = True
                
         #Architecture Error Handling
         #Start Architecture Detection while in architecture
         if architectureStartFound:
           if isInArchitecture:
              logging.error(" /!\\Error/!\\ - file:%s line:%d Architecture declaration found while already in!" %(vhdlFile,lineNumber))
              errorNumber = errorNumber + 1
           else:
              isInArchitecure = True
              architectureLineFound = True
              logging.debug("%05d: Found Architecture %s" %(lineNumber,architectureName))
              
         if architectureBeginFound:
           if isInArchitecture:
            isAfterArchitectureBegin = True
            logging.debug("%05d: Found Architecture Begin" %(lineNumber))
         
         if architectureEndFound:
           if isInArchitecture:
            isInArchitecture = False 
            
         #========================
         #Seach for "component xxx"
         #========================
         componentLineFound = False
         
         if continueLineAnalysis:
           m=re.match('^ *component +([A-Za-z0-9_]+) *',line,re.I)
           if m is not None:
             componentName      = m.group(1)
             componentLineFound = True
             logging.debug("%05d: Found Component %s" %(lineNumber,componentName))
          
        
         #======================================     
         #Search for Instanciation " xxx : xxx "
         #======================================
         instanceLineFound = False
         
         #Search for Instanciation Confirmation
         if continueLineAnalysis:
           if  instanceNotSure:
             if  re.search('^ *port map *',line,re.I):
               instanceLineFound = True
               logging.debug("%05d: Found Instance %s" %(lineNumber-1,instanceName))
             elif re.search('^ *generic map *',line,re.I):
               logging.debug("%05d: Found Instance %s" %(lineNumber-1,instanceName))
               instanceLineFound = True
             else:
               instanceLineFound = False
               instanceNotSure = False

         #Search for Instanciation Start
         if continueLineAnalysis:
           m=re.search('^ *([A-Za-z0-9_]+) *: *([A-Za-z0-9_]+) *',line,re.I)
           if m is not None:
             instanceName = m.group(1)
             instanceEntity = m.group(2)
             instanceNotSure  = True
             
         #Search for Instanciation Start using Already Compiled library    
         if continueLineAnalysis:
           m=re.search('^ *([A-Za-z0-9_]+) *: *entity +[A-Za-z0-9_]+(.+[A-Za-z0-9_]+) *port *map',line,re.I)
           if m is not None:
             instanceName = m.group(1)
             instanceEntity = m.group(2)
             instanceEntity = str.replace(instanceEntity,".","")
             componentName     = instanceEntity
             componentLineFound = True
             instanceLineFound = True
             instanceNotSure  = False    
             
         #======================================     
         #Search for Process " xxx : xxx "
         #======================================    
         processStartFound  = False
         processEndFound    = False
         processLineFound   = False
         
         #Search for Process Start
         if continueLineAnalysis:
           m=re.match('^ *([A-Za-z0-9_]+) +: +process *(\([A-Za-z0-9_ ,]+\)) *',line,re.I)
           if m is not None:
             processName = m.group(1)
             processSensitivity = m.group(2)
             processStartFound = True
             totalProcessNumber = totalProcessNumber + 1 ;
         
         #Search for Process End
         if continueLineAnalysis:
           m=re.search('^ *end +process +([A-Za-z0-9_]+) *',line,re.I)
           if m is not None:
             if processName == m.group(1):
               processEndFound =True        
                
         #Process Error Handling
         #Start Process Detection while in process
         if processStartFound:
           if isInProcess:
              logging.error(" /!\\Error/!\\ - file:%s line:%d Process declaration found while already in!" %(vhdlFile,lineNumber))
              errorNumber = errorNumber + 1
           else:
              isInProcess = True
              processLineFound = True
              logging.debug("%05d: Found Process %s" %(lineNumber,processName))
         
         if processEndFound:
           if isInProcess:
            isInProcess = False      
        
         #Line Incr
         lineNumber = lineNumber+1  
              
         
         ###############################
         # Ok, Let's Go
         ###############################
         #ParseInfo format is simple to be exported easily 
      
         #======================================================================
         # Write Tag Data  
         #======================================================================
               
         #Find Link
         if linkTagLineFound:
           linkToType = linkTagType;
           linkToName = linkTagName;
         #Link Raz  
         elif not isTagLine:
           linkToType = "";
           linkToName = "";
         
         #Find brief
         if briefTagLineFound:
           commentType = "brief";
           briefIsValid = True
         #Link Raz  
         elif not isTagLine:
           commentType = "comment";
           briefIsValid = False     
         
         #Find details
         if detailsTagLineFound:
           commentType = "details";
           detailsIsValid = True
         #Link Raz  
         elif not isTagLine:
           commentType = "comment";
           detailsIsValid = False    
         
         #Comment Tag 
         #Structure: [file,lineNumber,"tag",commentType,linkToType,linkToName,commentTag,Null,Null]
         if commentTagLineFound:
          parseInfo.append([vhdlFile,lineNumber,"tag",commentType,linkToType,linkToName,commentTag,True,""])
        
         #Title Tag 
         #Structure: [file,lineNumber,"tag","title",linkToType,linkToName,titleTag,Null,Null]
         if titleTagLineFound:
          parseInfo.append([vhdlFile,lineNumber,"tag","title",linkToType,linkToName,titleTag,False,""])
           
         #Brief Tag 
         #Structure: [file,lineNumber,"tag","brief",linkToType,linkToName,briefTag,Null,Null]
         if briefTagLineFound:
          parseInfo.append([vhdlFile,lineNumber,"tag","brief",linkToType,linkToName,briefTag,False,""])
          
         #Details Tag 
         #Structure: [file,lineNumber,"tag","details",linkToType,linkToName,briefTag,Null,Null]
         if detailsTagLineFound:
          parseInfo.append([vhdlFile,lineNumber,"tag","details",linkToType,linkToName,detailsTag,False,""])
            
         #Fig Tag 
         #Structure: [file,lineNumber,"tag","fig",linkToType,linkToName,figTagName,figTagFilename,Null]
         if figTagLineFound:
          parseInfo.append([vhdlFile,lineNumber,"tag","fig",linkToType,linkToName,figTagName,figTagFilename,""])

     
         #======================================================================
         # Write VHDL Data  
         #======================================================================
         #Library 
         #Structure: [file,lineNumber,"library",libraryName,Null,Null,Null,Null,Null]
         if libraryLineFound:
           libraryList = [vhdlFile,lineNumber,"library",libraryName,"","","","","",""]
           libraryListNoLineNumber = libraryList
           libraryListNoLineNumber[1] = ""
           existInParseInfo = False
           for parseList in parseInfo:
             parseList[1] = ""
             if libraryListNoLineNumber == parseList:
               existInParseInfo = True
           if existInParseInfo == False:
             parseInfo.append(libraryList)
          
         #Use 
         #Structure: [file,lineNumber,"use",useName,Null,Null,Null,Null,Null]
         if useLineFound:
           useList = [vhdlFile,lineNumber,"use",useName,libraryName,"","","","",""]
           useListNoLineNumber = useList
           useListNoLineNumber[1] = ""
           existInParseInfo = False
           for parseList in parseInfo:
             parseList[1] = ""
             if useListNoLineNumber == parseList:
               existInParseInfo = True
           if existInParseInfo == False:
             parseInfo.append(useList)
             
         #Entity 
         #Data Structure: [file,lineNumber,"entity",entityName,"",Null,Null,Null,Null]
         if entityLineFound:
           parseInfo.append([vhdlFile,lineNumber,"entity",entityName,"","","","","",""])
          
         #Entity Signal
         #Data Structure: [file,lineNumber,"entitySignal",entitySignalName,entitySignalDirection,entitySignalType,entityName,Null,Null]
         if entitySignalLineFound:
           parseInfo.append([vhdlFile,lineNumber,"entitySignal",entitySignalName,entitySignalDirection,entitySignalType,entityName,"",""])
         
         #Package
         #Data Structure: [file,lineNumber,"package",packageName,Null,Null,Null,Null,Null]
         if packageLineFound:
           parseInfo.append([vhdlFile,lineNumber,"package",packageName,"","","","","",""])
         
         #Function
         #Data Structure: [file,lineNumber,"function",functionName,packageName,Null,Null,Null,Null]
         if functionLineFound:
           parseInfo.append([vhdlFile,lineNumber,"function",functionName,packageName,"","","","",""]) 
           
         #Architecture 
         #Data Structure: [file,lineNumber,"architecture",architectureName,entityName,Null,Null,Null,Null] 
         if architectureLineFound:
           parseInfo.append([vhdlFile,lineNumber,"architecture",architectureName,entityName,"","","","",""])
        
         #Component 
         #Data Structure: [file,lineNumber,"component",componentName,architectureName,entityName,Null,Null,Null] 
         if componentLineFound:
           parseInfo.append([vhdlFile,lineNumber,"component",componentName,architectureName,entityName,"","","",""]) 
         
         #Instance 
         #Data Structure: [file,lineNumber,"instance",instanceName,entityName,Null,Null,Null,Null] 
         if instanceLineFound:
           parseInfo.append([vhdlFile,lineNumber,"instance",instanceName,instanceEntity,"","","",""])
                  
         #Process 
         #Data Structure: [file,lineNumber,"process",architectureName,entityName,processName,processSensitivity,Null,Null] 
         if processLineFound:
           parseInfo.append([vhdlFile,lineNumber,"process",processName,processSensitivity,architectureName,entityName,"",""])
   
   
    #Calc Stat
    totalLineNumber  = totalLineNumber  + lineNumber
    totalErrorNumber = totalErrorNumber + errorNumber  
 
  #Create a Reduce List of info
  for parseElt in parseInfo:
    if parseElt[TYPE_RK] in ["library","use","package","entity","component","instance"]:
      parseInfoReduce.append(parseElt)
 
  #Fill Stat
  parseStat.append([fileNumber,"Files"])
  parseStat.append([totalLineNumber,"Lines"])
  parseStat.append([totalCommentLineNumber,"Comment Lines"])
  parseStat.append([totalErrorNumber,"Errors"])
  parseStat.append([totalEntityNumber,"Entities"])
  parseStat.append([totalProcessNumber,"Process"])
  parseStat.append([totalFunctionNumber,"Functions"])
  parseStat.append([totalTagLineNumber,"Tag Lines"])

  
  print "-=====================================================================-"
  print " End Parsing VHDL files"
  print " - %d Files , %d Lines parsed"  %(fileNumber,totalLineNumber)
  if totalErrorNumber:
   print " - /!\\%d Errors found/!\\ --> Doc Generation Stop!"  %(totalErrorNumber)
   print "  Switch to verboseMode to help Errors Fix"
  else:
   print " - %d Errors found"  %(totalErrorNumber)
  print "-=====================================================================-"
  
  #Return
  return totalErrorNumber
        