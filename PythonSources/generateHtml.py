#!/usr/local/bin/python

#===============================================================================
# Author  : F.Kermarrec / EnjoyDigital
# Data    : 14/02/2011
# Purpose : generateHtml.py
#           Generate Documentation in Html
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

global localDesignEntity


#=================================
# prepareHtmlDir Function
#=================================
def prepareHtmlDir(designEntity):

  #Create all Directory & copy Style File
  dirList = []
  dirList.append(htmlDocDir)
  dirList.append(sourcesDocDir)
  dirList.append(entitiesDocDir)
  dirList.append(packagesDocDir)
  
  #Create Directories,SubDirectories&Style Dir
  for dirElement in dirList:
  
    #Create directory
    if not os.path.exists(dirElement):
     os.makedirs(dirElement)
  
    #Copy Style Files
    styleRefDir    = os.curdir  +"\\"+pythonSources+"\\"+styleDir
    styleLocalDir = dirElement +"\\"+styleDir
    
    if os.path.exists(styleLocalDir):
      rmtree(styleLocalDir)
    copytree(styleRefDir,styleLocalDir) 
   
  #Creat Illustation Directory
  #Create directory
  if os.path.exists(illustationDocDir):
    rmtree(illustationDocDir)
     
  #Copy Illustation Files
  illustationsRefDir = os.curdir  +"\\"+localPathIllustration    
  copytree(illustationsRefDir,illustationDocDir)
  
  #Copy DesignEntity
  global localDesignEntity
  localDesignEntity = designEntity
         
  
#=================================
# generateHtmlHeader Function
#=================================
def generateHtmlHeader(p_file):

  #Get Design Title
  global localDesignEntity
  designFilename = retrieveFilenameElement(parseInfo,"entity",localDesignEntity)
  #print localDesignEntity
  #print designFilename
  dataTagList = listDataTag("entity",localDesignEntity,designFilename)
  #print dataTagList 
  
  docTitle = ""
  
  #Loop on dataTagList
  for dataTag in dataTagList:
  
    dataType        = dataTag[0]
    dataString      = dataTag[1]
    
    #Tag Brief
    if dataType == "title":
      docTitle = dataString                     
             
  #Write HtmlHeader
  print >> p_file, "<html>"
  print >> p_file, " <head>"
  print >> p_file, "  <title>VHDL Documentation %s</title>" %(docTitle)
  
  print >> p_file, "  <link rel=\"stylesheet\" media=\"screen\" type=\"text/css\" title=\"style\" href=\"%s/style.css\" />" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/shCore.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/shBrushVhdl.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/jquery.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/jquery_002.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/footer.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/ga.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/aboutSlider.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/protovis-d3.js\"></script>" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\" src=\"hierarchy.js\"></script>"
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/plot_hierarchy.js\"></script>" %(styleDir) 
  print >> p_file, "  <script type=\"text/javascript\" src=\"%s/javascript/back_to_top.js\"></script>" %(styleDir)
   
  print >> p_file, "  <link rel=\"stylesheet\" type=\"text/css\" href=\"%s/javascript/shCore.css\" />" %(styleDir)
  print >> p_file, "  <link rel=\"stylesheet\" type=\"text/css\" href=\"%s/javascript/shThemeDefault.css\" />" %(styleDir)
  print >> p_file, "  <script type=\"text/javascript\">SyntaxHighlighter.all();</script>"
  print >> p_file, " </head>"
  print >> p_file, "<body>"
          
  print >> p_file, "<div id=\"wrapper\">"
  print >> p_file, " <div id=\"headwrap\">"	
  print	>> p_file, "	  <div class=\"logo\">"
  print	>> p_file, " 	   <a href=\"http://www.enjoy-digital.fr/\" title=\"enjoydigital\" rel=\"home\"><img src=\"%s/images/Vhdl2Doc.png\" alt=\"EnjoyDigital\"></a>" %(styleDir)
  print	>> p_file, "   </div>"
  print	>> p_file, "   <div id=\"bigTitleCenter\">%s</div>" %(docTitle)
  print	>> p_file, "	</div>"
  
  print >> p_file, "<div id=\"content\">"
	
#=================================
# generateHtmlFilter Function
#=================================
def generateHtmlFilter(p_file,active,indentLevel):

  rel = ""

  #Change Link With Intentation Level
  if indentLevel == 0:
    rel = ""
  elif indentLevel == 1:
    rel = "../"
  elif indentLevel == 2:
    rel = "../../"
    
  #Define HtmlFilter List
  htmlFilter = []
  htmlFilter.append("Home")
  htmlFilter.append("Documentation")
  htmlFilter.append("Entities")
  htmlFilter.append("Packages")
  htmlFilter.append("Sources")
  htmlFilter.append("Utils")
  htmlFilter.append("About")
       

  #Write HtmlFilter
  print >> p_file, "<div id=\"worksFilter\" style=\"display: yes;\">"
  print >> p_file, "<ul id=\"filter\" >"
  
  for htmlFilterElement in htmlFilter:
    if active == htmlFilterElement:
      print	>> p_file, "<li class=\"active\" id=\"%s\"><a href=\"%s%s.html\" >%s</a></li>" %(htmlFilterElement,rel,str.lower(htmlFilterElement),htmlFilterElement)
    else:
      print	>> p_file, "<li id=\"%s\"><a href=\"%s%s.html\" >%s</a></li>" %(htmlFilterElement,rel,str.lower(htmlFilterElement),htmlFilterElement)
         	
  print >> p_file, "</ul>" 
  print >> p_file, "</div>"
  
     
#=================================
# generateHtmlFooter Function
#=================================
def generateHtmlFooter(p_file):

  #Write HtmlFooter
  
  #Get Time of the Day
  t = datetime.datetime.now()
  EpochSeconds = time.mktime(t.timetuple())
  now = datetime.datetime.fromtimestamp(EpochSeconds)
  
  #Presentation
  print >> p_file, "<br>"
  print >> p_file, "<br>"
  print >> p_file, "<br>"
  
  #Insert Date / Link / Version
  print >> p_file, "Generated on  %s with <a" %(now.ctime())
  print >> p_file, "href=\"http://www.enjoy-digital.fr/\">EnjoyDigital VHDL2Doc</a>"
  print >> p_file, vhdl2DocVersion
  
  #Presentation
  print >> p_file, "<br>"
  print >> p_file, "<br>"
  
  #Close Content
  print >> p_file, "</div>"
  
  #Start Footer
  print >> p_file, "<div id=\"footer\">"
  print >> p_file, "<div id=\"backToTop\"><a href=\"#\"><img src=\"%s/images/%s\" alt=\"EnjoyDigital\" /></a></div>" %(styleDir,styleFooterButton)
  
  print >> p_file, "<script language=\"javascript\">"
  print >> p_file, "back_to_top();"
  print >> p_file, "</script>"
	
  print >> p_file,	"<div id=\"footerLeftColumn\">"
  print >> p_file, "<div id=\"copyInfo\">"
  print >> p_file,	"CopyLeft 2011 . EnjoyDigital.<br>"
  print >> p_file, "</div>"
  print >> p_file, "</div>"
    
  print >> p_file, "<div id=\"footerRightColumn\">"
  print >> p_file,	"<div id=\"footer_address\">ENJOYDIGITAL<br>"
  print >> p_file,	"<div id=\"footer_contact\"><a href=\"mailto:florent@enjoy-digital.fr\">florent@enjoy-digital.fr</a></div>" 	 
  print >> p_file, "</div>"
  print >> p_file, "</div>"
  
  #Close Footer
  print >> p_file, "</div>"
  
  #Close Body
  print >> p_file, "</body>"
  
  #Close Html
  print >> p_file, "</html>"
  

#=================================
# insertVhdlCodeHtml Function
#=================================
def insertVhdlCodeHtml(p_file,vhdlFile):

  #Call of SyntaxHilighter
  print >> p_file, "<pre class=\"brush: vhdl;\">"
  
  #Open Vhdl File
  with open(vhdlFile) as p_vhdlFile:
    
    #Read each line
    for line in p_vhdlFile:
      print >> p_file, "%s" %(line),
  
  print >> p_file,"</pre>"


#=================================
# listSourcesHtml Function
#=================================
def listSourcesHtml(p_file,fileList,designFileList,srcDir):

  #===============
  # Presentation
  #===============
  print >> p_file, "<h1><img src=\"Style/icons/021.png\">  Source file overview</h1>"
  print >> p_file, "<p>The file paths link to HTML pages showing the sources; the links in brackets point to the actual source files.</p>"
  print >> p_file, "</div>"
  print >> p_file, "<div id=\"contentMini\">"


  #Generate Ordered File List
  designFileListOrdered = listDesignFilesOrdered(fileList,designFileList)
  
  
  #===============
  # Table Generation
  #===============
  
  #Open Table
  print >> p_file, "<table border=\"0\">"
  
  #Start Loop
  for designFile in designFileListOrdered:
    
    #Doc Filename : Add .html to filename
    docFilename  = sourcesDir +"/" + os.path.basename(designFile)+".html"
    
    #Show Filename : Remove Sources Base Directory from filename
    showFilename = str.replace(designFile,srcDir,"")
  
    #Presentation
    print >> p_file, "<tr>"
    print >> p_file, "<td>"
    print >> p_file, "<a href=\"%s\">%s</a>&nbsp;&nbsp;&nbsp;</td>" %(docFilename,showFilename)
    print >> p_file, "</tr>"                                                                                                                             
        
  #Close Table
  print >> p_file, "</table>"
  
  
#=================================
# generateSourcesListHtml Function
#=================================
def generateSourcesListHtml(fileList,designFileList,srcDir):

  #Message
  print " Start Sources Generation"
  print "------------------------------------------------------------------"

  #Open File
  f = open(htmlDocDir+'\\sources.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Sources",0)

  #Generate List of Sources and Link
  listSourcesHtml(f,fileList,designFileList,srcDir)
  
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()

#======================================
# GenerateSourcesHighlightHtml Function
#======================================
def generateSourcesHighlightHtml(designFileList):

  global styleDir

  #designFile Loop
  for designFile in designFileList:
  
    #Html Name Determination
    docVhdlFileName = sourcesDocDir +"\\" + os.path.basename(designFile)+".html" 

    #Open File
    f = open(docVhdlFileName, 'w+')  
  
    #Generate Html Header
    generateHtmlHeader(f)

    #Generate Html Filter
    generateHtmlFilter(f,"Sources",1)
    
    #Show FileName
    print >> f, "<h1><img src=\"Style/icons/028.png\">  Source file %s</h1>" %(os.path.basename(designFile))
    print >> f, "</div>"
    print >> f, "<div id=\"contentMini\">"

    #Syntax Highlighing
    insertVhdlCodeHtml(f,designFile)
    
    #Generate Html Footer
    generateHtmlFooter(f)

    #Close File
    f.close()
      

   
#======================================
# GenerateHomeHtml Function
#======================================
def generateHomeHtml(designEntity,designHierarchyFileList):
  
  #Message
  print " Start Home Generation"
  print "------------------------------------------------------------------"

   #Open File
  f = open(htmlDocDir+'\\home.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Home",0)
  
  #Show Project Description
  print >> f, "<h1><img src=\"Style/icons/019.png\">  Design brief</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  designFilename = retrieveFilenameElement(parseInfo,"entity",designEntity)
  tagInsertionHtml(f,designFilename,"entity",designEntity,True)

  #Show Hierarchy Overview
  #print >> f, "<h1>Hierarchy Quick Overview</h1>"
  #print >> f, "</div>"
  #print >> f, "<div id=\"contentMini\">"
  #generateHierarchyProtovis(designHierarchyFileList)
  #print >> f, "<script type=\"text/javascript+protovis\">plotHierarchy();</script>"
  #print >> f, "<br>"
  
  #Show Hierarchy Overview Html
  print >> f, "<h1><img src=\"Style/icons/024.png\">  Hierarchy Quick Overview</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "<div id=\"contentHierarchy\">"
  
  
  print >> f, "<b>[<a href=\"%s\" target=\"_blank\" >%s</a>]</b>:" %("Entities/work."+designEntity+".html",designEntity)
  print >> f, "<br>" 
  #Loop on designHierarchyFileList
  for designHierarchyElement in designHierarchyFileList:
    designLevel = designHierarchyElement[HIERARCHY_LEVEL_RK]
    designType  = designHierarchyElement[HIERARCHY_TYPE_RK]
    designName  = designHierarchyElement[HIERARCHY_NAME_RK]
  
    
    #for i in range(designLevel):
    #  print >> f, "&nbsp&nbsp<img src=\"Grey Ball.png\">"
      
    #print >> f, "&nbsp&nbsp<img src=\"Add Green Button.png\">"  
    
    
    for i in range(designLevel):
      print >> f, "&nbsp&nbsp|"
      
    print >> f, "&nbsp&nbsp+"  
    
    if designType == "instance":
      if isEntityLinkTo(designName):          
        print >> f, "<b>[<a href=\"%s\" target=\"_blank\">%s</a>]</b>:" %("Entities/work."+designName+".html",designName)
      else:
        print >> f, "<b>[%s]</b>:" %designName
      
    else:
      m=re.match('^([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)',designName,re.I)
      if compareString(m.group(1),"ieee"):
        print >> f, "<i>%s.%s.%s</i>:" %(m.group(1),m.group(2),m.group(3))
      else:
        print >> f, "<i>%s.[<a href=\"%s\" target=\"_blank\">%s</a>].%s</i>:" %(m.group(1),"Packages/"+m.group(1)+"."+m.group(2)+".html",m.group(2),m.group(3))
        
    print >> f, "<br>"   
  
  print >> f, "</div>"
  
  #Show Compliance Overview
  print >> f, "<h1><img src=\"Style/icons/014.png\">  Compliance Quick Overview</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "[To be done!]"

  
  #Show Design Stats
  print >> f, "<h1><img src=\"Style/icons/012.png\">  Design statistics</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "Statistics based on parsed files<br><br>"
  for parseStatElement in parseStat: 
    print >> f, "Nb %s : %s<br>" %(parseStatElement[1],parseStatElement[0])
  
  print >> f, "<br>"
  
  
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()
  
  
#======================================
# GenerateAboutHtml Function
#======================================
def generateAboutHtml():
  #Message
  print " Start About Generation"
  print "------------------------------------------------------------------"

  #Open File
  f = open(htmlDocDir+'\\about.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"About",0)
  
  #Why Vhdl2Doc
  print >> f, "<h1><img src=\"Style/icons/023.png\">  Why Vhdl2Doc?</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "I'm sometimes a bit lazy and have search last year on the net for an automatic documentation for VHDL code without success."
  print >> f, "That's why I decided to develop my own tool, I hope it will be useful for someone else ;-)"
  
  #What can be done with Vhdl2Doc
  print >> f, "<h1><img src=\"Style/icons/023.png\"> How can Vhdl2Doc be useful?</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "Vhdl2Doc is useful for automatic VHDL documentation."
  print >> f, "It can be used for a new project where specifics Tags will be used",
  print >> f, "to enhance documentation (Comments, Descriptions, Schematics, Synoptics,etc... See Below)"
  print >> f, "It can also be used to understand old projects where documentation is lost or very brief, it will allow to recover easily",
  print >> f, "design hierarchy, to navigates in entities, packages, etc..."
  
  #How it Works
  print >> f, "<h1><img src=\"Style/icons/023.png\"> How it works?</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print	>> f, "<img src=\"%s/images/Vhdl2DocSynoptic.png\" alt=\"EnjoyDigital\">" %(styleDir)
  print >> f, "Vhdl2Doc is developped in Python."
  print >> f, "You put all your VHDL files in a folder, Vhdl2Doc search the Vhdl files in this folder, analyse the files,"
  print >> f, "find the optional documentation Tags you put in the code, etc..."
  print >> f, "Once it's done, it propose you the possible design Top found in the repertory, you choose it and it will do the rest."
  
  #Documentation Tags examples
  #Comments
  print >> f, "<h1><img src=\"Style/icons/022.png\"> Documentation Tags examples:</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "<h2>Insertion of Comments in the documentation:</h2>"
  print >> f, "<pre class=\"brush: vhdl;\">"
  print >> f, "  --* This process defines a counter.  This is just to demonstrate"
  print >> f, "  --* how Vhdl2Doc documentation comments can extend over several "
  print >> f, "  --* comment lines."
  print >> f, "  --*"""
  print >> f, "  --* Here is a second paragraph, again designed to show"
  print >> f, "  --* how to write documentation for Vhdl2Doc."
  print >> f, "  Counter_p : process( rst_n, clk ) is"
  print >> f, "  begin"
  print >> f, "    if rst_n = '0' then "
  print >> f, "      counter <= (others => '0');"
  print >> f, "    elsif rising_edge(clk) then "
  print >> f, "      counter <= counter + 1;"
  print >> f, "    end if;  "
  print >> f, "  end process Counter_p; "
  print >> f, "</pre>"
  print >> f, "<br>"
  
  #Description
  print >> f, "<h2>Insertion of detailed information:</h2>"
  print >> f, "<pre class=\"brush: vhdl;\">"
  
  print >> f, "--------------------------------------------------------------------------------"
  print >> f, "--                            Entite                                            "
  print >> f, "--------------------------------------------------------------------------------"
  print >> f, "--* @link     [entity] [PwmDeadTime]                                             "
  print >> f, "--* @brief    Ce module gere la protection sur la commuation des Mos de pont en H"
  print >> f, "--* @details  Il realise:                                                         "
  print >> f, "--* @details  - l'inversion des signaux de commandes des Mos High et Low          "
  print >> f, "--* @fig      [Inversion Mos High et Low] [Inversion_Mos_High_Low.png]            "
  print >> f, "--* @details  - l'application d'un retard a la commutation pour compenser le delai"
  print >> f, "--*           de desactivation du Mos et eviter les bref courts circuits.         "
  print >> f, "--* @fig      [Retard a la commutation] [Retard_A_La_Commutation.png]             "
  print >> f, "--------------------------------------------------------------------------------  "
  print >> f, "entity PwmDeadTime is                                                             "
  print >> f, "generic (                                                                         "
  print >> f, "  PWM_NB     : natural := 3;          -- Nombre de voies PWM                      "
  print >> f, "  CLK_PERIOD : real    := 33.0;       -- Periode de l'horloge (ns)                "
  print >> f, "  DEAD_TIME  : real    := 0.6);       -- Dead Time Commutation Mos (us)           "
  print >> f, "port (                                                                            "
  print >> f, "   clk             : in std_logic;                                                "
  print >> f, "  rst_n           : in std_logic;                                                 "
  print >> f, "  switch_n        : in std_logic;                                                 "
  print >> f, "  pwmNoDeadTime   : in unsigned(PWM_NB-1 downto 0);                               "
  print >> f, "  pwmWithDeadTime : in unsigned(2*PWM_NB-1 downto 0)                              "
  print >> f, "  );                                                                              "
  print >> f, "end PwmDeadTime;                                                                  "
  print >> f, "</pre>"
  print >> f, "<br>"
  print >> f, "Here are some examples of Tags use:<br>"
  print >> f, "- Use @link    Tag to link the next Tags to specific Element<br>"
  print >> f, "- Use @brief   Tag to insert brief of the Elemetn(entity,package,process,instance,etc...)<br>"
  print >> f, "- Use @details Tag to insert more information about the element.<br>"
  print >> f, "- Use @req     Tag to specify to which requirement the element belongs.<br>"
  print >> f, "- Use @version Tag to specify to which version of the requirement the element belongs.<br>"
  print >> f, "- Use @fig     Tag to insert a figure of a schematic, synoptic, chronogram...<br>"
  print >> f, "Each Tags can be used more than one time for each element<br>"
  print >> f, "<br>"
  print >> f, "link is valid until a non-comment line is found<br>"
  
  #Todo List and limitations
  print >> f, "<h1><img src=\"Style/icons/016.png\">  Todo List and Limitations: (Vhdl2Doc %s , %s)</h1>" %(vhdl2DocVersion,vhdl2DocDate)
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "<h2>Todo</h2><br>"
  print >> f, " - Code Latex engine to generate PostScript,Pdf documentation<br>"
  print >> f, " - Move parts of hierarchy search done in Html Generation to Hierarchy engine(For Reuse in Latex)<br>"
  print >> f, " - Test & Improve parse engine on more designs and files<br>"
  print >> f, " - Improve hierarchy engine<br>"
  print >> f, " - Improve documentation presentation<br>"
  print >> f, " - Add Requirement Compliance resume<br>"
  print >> f, " - Add more Documentation Tags<br>"
  print >> f, " - Etc...<br>"
  print >> f, "<br>"
  print >> f, "You have ideas to improve Vhdl2Doc or want a specific function, feel free to contact me!<br>"
  
  print >> f, "<h2>Limitations</h2><br>"
  print >> f, " - More tests needs to be done one each engine(Parse,Hierarchy)<br>"
  print >> f, " - I'have test those engines on several designs. Still, it is possible that your"
  print >> f, "design may be incorrectly parsed. If so, you can help me greatly by sending me a copy of"
  print >> f, "the VHDL files witch failed to be parsed"

  
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()
  
  
#======================================
# tagInsertionHtml Function
#======================================  
def tagInsertionHtml(f,tagFilename,tagType,tagName,isHome):

  #Is it first Brief Tag?
  firstBrief = True
  
  #Get Data corresponding to Type
  dataTagList = listDataTag(tagType,tagName,tagFilename)
  
  #Loop on dataTagList
  for dataTag in dataTagList:
  
    dataType        = dataTag[0]
    dataString      = dataTag[1]
    dataIsValid     = dataTag[2]
    dataFigName     = dataTag[3]
    dataFigFilename = dataTag[4]
    
    #Tag Brief
    if dataType == "brief":
      #In Entity?
      if tagType == "entity":
          if dataIsValid:
            print >> f, "<h2>"+dataString+"</h2>"
          else:
            print >> f, "<br>"
            print >> f, "<h2>"+dataString+"</h2>"
      #Or something else
      else: 
          if not dataIsValid:
            if firstBrief == False:
              print >> f, "<br>"
              print >> f, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+dataString
            else:
              print >> f, "&nbsp;&nbsp;&nbsp;&nbsp;"+dataString
            firstBrief = False
          else:
            print >> f, dataString 
            
            
    # Tag Details        
    elif dataType == "details":
      if dataIsValid:
        print >> f, dataString
      else:
        print >> f, "<br>"
        print >> f, dataString
         
    # Tag Fig                
    elif dataType == "fig":
      if isHome:
        print >> f, "<br><div id=\"centerImg\"><img src=\"./%s/%s\" alt=\"EnjoyDigital\"><br>%s</div>" %(illustationsDir,dataFigFilename,dataFigName)
      else:       
        print >> f, "<br><div id=\"centerImg\"><img src=\"../%s/%s\" alt=\"EnjoyDigital\"><br>%s</div>" %(illustationsDir,dataFigFilename,dataFigName)
  
  
  
#======================================
# GenerateEntitiesHtml Function
#======================================
def generateEntitiesHtml(entityName,libraryName,srcDir):

  #Open File
  f = open(entitiesDocDir+'\\'+libraryName+"."+entityName+'.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Entities",1)
  
  #Title
  print >> f, "<h1><img src=\"Style/icons/028.png\">  Entity %s.%s </h1>" %(libraryName,entityName)
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  
  #Retrieve fileName
  entityFilename = retrieveFilenameElement(parseInfo,"entity",entityName)             
  docVhdlFileName = "../"+sourcesDir +"/" + os.path.basename(entityFilename)+".html"
  showVhdlFileName = str.replace(entityFilename,srcDir,"")
  
  ######################
  #Show Entity & Tags
  ######################
           
  print >> f, "File <a href=\""+docVhdlFileName+"\">"+showVhdlFileName+"</a><br>"
  tagInsertionHtml(f,entityFilename,"entity",entityName,False)
  
  
  ######################
  #Show Libraries
  ######################
  print >> f, "<h2><img src=\"Style/icons/006.png\">  Libraries</h2>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  
  #Get Library corresponding to File
  libraryList = listLibrary(entityFilename)
  
  #Start Table
  print >> f, "<table border=\"0\">"
  
  currentLibrary = ""
  
  for library in libraryList:
  
    libraryType       = library[0]
    libraryName       = library[1]
    libraryReduceName = library[2]
    libraryIsInDesign = library[3]
  
    if libraryType == "library":
      print >> f, "<tr><td>Library "+libraryName+"</a></td></tr>"
      currentLibrary = libraryName
    elif libraryType == "use":
      linkUseName = "../packages/"+currentLibrary+"."+libraryReduceName+".html"
      
      if libraryIsInDesign:
        print >> f, "<tr><td>Use <a href=\""+linkUseName+"\">"+libraryName+"</a></td></tr>"
      else:
        print >> f, "<tr><td>Use "+libraryName+"</td></tr>"            
        
   #End Table
  print >> f, "</table>"      
        
  ######################
  #Show Signals
  ######################
  print >> f, "<h2><img src=\"Style/icons/006.png\">  Ports</h2>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  
  #Get Library corresponding to Entity
  signalList = listSignal(entityName)
  
  #Start Syntax Hilighting
  print >> f, "<pre class=\"brush: vhdl;\">"
  
  for signal in signalList:
    signalName        =  signal[0]
    signalDirection   =  signal[1]
    signalType        =  signal[2]      
  
    signalNameLength = len(signalName)
    spaceFirst = ""
    for i in range(30-signalNameLength):
      spaceFirst = spaceFirst + " "

    signalDirectionLength = len(signalDirection)
    spaceSecond = "";
    for i in range(10-signalDirectionLength):
      spaceSecond = spaceSecond + " "
      
    print >> f, "%s%s%s%s%s" %(signalName,spaceFirst,signalDirection,spaceSecond,signalType)        
              
  #End SyntaxHilighting
  print >> f, "</pre>"
                
  ######################
  #Show Architecture
  ######################
  print >> f, "<h2><img src=\"Style/icons/006.png\">  Architecture ",
    
  #Get Library corresponding to Entity
  architectureList = listArchitecture(entityName)
  
  for architecture in architectureList:
        print >> f, "["+architecture+"]</h2>"           
        print >> f, "</div>"
        print >> f, "<div id=\"%s\"></div>" %architecture
        print >> f, "<div id=\"contentArchitecture\">"       
  
  
  ######################
  #Show Instances
  ######################
  findInstance = False
   
  for parseElement in parseInfo:               
    elementType = parseElement[TYPE_RK]
    if elementType == "instance":
      instanceName         =  parseElement[INSTANCE_NAME_RK]
      instanceEntityName   =  parseElement[INSTANCE_ENTITY_NAME_RK]
      instanceFilename   =  parseElement[FILENAME_RK]
      if str.upper(entityFilename) == str.upper(instanceFilename):
        if findInstance == False:
          findInstance = True
          print >> f, "<h2><img src=\"Style/icons/002.png\">  Instances</h2>"
          print >> f, "</div>"
          print >> f, "<div id=\"contentArchitecture\">"
          
        #Start Table
        print >> f, "<table border=\"0\">"       
        print >> f, "<tr>"
        print >> f, "<td>"
        print >> f,instanceName+"&nbsp;&nbsp;&nbsp;"
        print >> f,"</td>"
        print >> f, "<td>"
        print >> f,instanceEntityName
        print >> f,"</td>"
        print >> f,"</tr>"
        #End Table
        print >> f, "</table>"
        #Show Entity Tags
        tagInsertionHtml(f,entityFilename,"instance",instanceName,False)               

  
  #Find Process
  findProcess = False
  
  for parseElement in parseInfo:               
    elementType = parseElement[TYPE_RK]
    if elementType == "process":
      processName         =  parseElement[INSTANCE_NAME_RK]
      processSensitivity  =  parseElement[PROCESS_SENSITIVITY_RK]
      processFilename     =  parseElement[FILENAME_RK]
      if str.upper(entityFilename) == str.upper(processFilename):
        if findProcess == False:
          findProcess = True
          print >> f, "<h2><img src=\"Style/icons/002.png\">  Processes</h2>"
          print >> f, "</div>"
          print >> f, "<div id=\"contentArchitecture\">"
       
        #Start Table
        print >> f, "<table border=\"0\">"              
        print >> f, "<tr>"
        print >> f, "<td>"
        print >> f,processName+"&nbsp;&nbsp;&nbsp;"
        print >> f,"</td>"
        print >> f, "<td>"
        print >> f,processSensitivity
        print >> f,"</td>"
        print >> f,"</tr>"
        #End Table
        print >> f, "</table>"
        #Show Entity Tags
        tagInsertionHtml(f,entityFilename,"process",processName,False)           
        

     
  
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
     
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()

    
#======================================
# GenerateEntitiesListHtml Function
#======================================
def generateEntitiesListHtml(designFileList,libraryName,srcDir):
  
  #Message
  print " Start Entities Generation"
  print "------------------------------------------------------------------"

  #Open File
  f = open(htmlDocDir+'\\entities.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Entities",0)
  
  #Title
  print >> f, "<h1><img src=\"Style/icons/021.png\">  List of entities and architectures</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  #Start Table
  print >> f, "<table border=\"0\">"
  
  for entityParseElement in parseInfo:
  
    for checkCompiled in designFileList:
      if entityParseElement[FILENAME_RK] == checkCompiled:
  
        if entityParseElement[TYPE_RK] == "entity":
          entityName = entityParseElement[ENTITY_NAME_RK]
    
          for architectureParseElement in parseInfo:
            if architectureParseElement[TYPE_RK] == "architecture":
              if  entityName ==  architectureParseElement[ARCHITECTURE_ENTITY_NAME_RK]:
                architectureName = architectureParseElement[ARCHITECTURE_NAME_RK]
            
          print >> f, "<tr><td><a href=\"Entities/%s.%s.html\">%s.%s</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td><a href=\"Entities/%s.%s.html#%s\">[%s]</a></td></tr>" %(libraryName,entityName,libraryName,entityName,libraryName,entityName,architectureName,architectureName)
      
          generateEntitiesHtml(entityName,libraryName,srcDir)
  
  
  #End Table
  print >> f, "</table>"
  #print >> f, "</table border>"
     
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()
      
#======================================
# GeneratePackagesHtml Function
#======================================
def generatePackagesHtml(packageName,libraryName,srcDir):

  #Open File
  f = open(packagesDocDir+'\\'+libraryName+"."+packageName+'.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Packages",1)
  
  #Title                        
  print >> f, "<h1><img src=\"Style/icons/028.png\">  Package %s.%s </h1>" %(libraryName,packageName)
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  
  #Retrieve fileName 
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "package":
      packageNameElement    = parseElement[PACKAGE_NAME_RK]
      if str.upper(packageName) == str.upper(packageNameElement):
        packageFilename = parseElement[FILENAME_RK]
        
  docVhdlFileName = "../"+sourcesDir +"/" + os.path.splitext(os.path.basename(packageFilename))[0]+".html"
  showVhdlFileName = str.replace(packageFilename,srcDir,"")             
  print >> f, "File <a href=\""+docVhdlFileName+"\">"+showVhdlFileName+"</a><br>"
  
  
  #Find Library                  
  print >> f, "<h2><img src=\"Style/icons/006.png\">  Libraries</h2>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  #Start Table
  print >> f, "<table border=\"0\">"
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "library":
      libraryElementName     =  parseElement[LIBRARY_NAME_RK]
      libraryElementFilename =  parseElement[FILENAME_RK] 
      if str.upper(libraryElementFilename) == str.upper(packageFilename):
        print >> f, "<tr><td>Library "+libraryName+"</a></td></tr>"
    elif elementType == "use":
      useElementName     =  parseElement[USE_NAME_RK]
      useElementFilename =  parseElement[FILENAME_RK]
      if str.upper(useElementFilename) == str.upper(packageFilename):
        #Find if library is in design
        compiledLibrary = False
        testUseName = str.replace(useElementName,libraryName+".","")
        testUseName = str.replace(testUseName,".all","")
        linkUseName = "../packages/"+libraryName+"."+testUseName+".html"
        for testParseElement in parseInfo:
          if testParseElement[TYPE_RK] == "package":
            if testUseName == testParseElement[PACKAGE_NAME_RK]:
              compiledLibrary = True
        
        if compiledLibrary:          
          print >> f, "<tr><td>Use <a href=\""+linkUseName+"\">"+useElementName+"</a></td></tr>"
        else:
          print >> f, "<tr><td>Use "+useElementName+"</td></tr>"
            
        
   #End Table
  print >> f, "</table>"
  

  #Find Component
  print >> f, "<h2><img src=\"Style/icons/006.png\">  Components</h2>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  #Start Table
  print >> f, "<table border=\"0\">"
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "component":
      componentName     =  parseElement[COMPONENT_NAME_RK]
      componentFilename =  parseElement[FILENAME_RK] 
      if str.upper(componentFilename) == str.upper(packageFilename):
        print >> f, "<tr>"
        print >> f, "<td>"
        print >> f, componentName+"&nbsp;&nbsp;&nbsp;"
        print >> f, "</td>"
        print >> f, "<td>"
        entityLink = "../../"+entitiesDocDir +"/"+libraryName+"."+componentName+".html"
        print >> f, "<a href=\"%s\">[default binding]</a>" %entityLink
        print >> f, "</td>"
        print >> f, "</tr>"
  #End Table
  print >> f, "</table>"      
        
  #Find Function
  print >> f, "<h2><img src=\"Style/icons/006.png\">  Functions</h2>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  #Start Table
  print >> f, "<table border=\"0\">"
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "function":
      functionName     =  parseElement[COMPONENT_NAME_RK]
      functionFilename =  parseElement[FILENAME_RK] 
      if str.upper(functionFilename) == str.upper(functionFilename):
        print >> f, "<tr>"
        print >> f, "<td>"
        print >> f, functionName+"&nbsp;&nbsp;&nbsp;"
        print >> f, "</td>"
        print >> f, "</tr>"      
        
   #End Table
  print >> f, "</table>"


  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()
  

#======================================
# GeneratePackageListHtml Function
#======================================
def generatePackageListHtml(designFileList,libraryName,srcDir):

  #Message
  print " Start Packages Generation"
  print "------------------------------------------------------------------"

  #Open File
  f = open(htmlDocDir+'\\packages.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Packages",0)
  
  #Title
  print >> f, "<h1><img src=\"Style/icons/021.png\">  List of packages</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  
  #Start Table
  print >> f, "<table border=\"0\">"
   
  for packageParseElement in parseInfo:
  
   for checkCompiled in designFileList:
      if packageParseElement[FILENAME_RK] == checkCompiled:
      
        if packageParseElement[TYPE_RK] == "package":
          packageName = packageParseElement[USE_NAME_RK]
          print >> f, "<tr><td><a href=Packages/"+libraryName+"."+packageName+".html>"+packageName+"</a></td></tr>"                                              
          generatePackagesHtml(packageName,libraryName,srcDir)    
  
   #End Table
  print >> f, "</table>"
     
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()  
  
#======================================
# GenerateUtilsHtml Function
#======================================
def generateUtilsHtml(designEntity,overviewList):
  #Message
  print " Start Utils Generation"
  print "------------------------------------------------------------------"

  #Open File
  f = open(htmlDocDir+'\\utils.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Utils",0)
  
  #Summary  
  print >> f, "Some functions that can be useful:" 
  
  #Why Compilation order
  print >> f, "<h1><img src=\"Style/icons/010.png\">  Compilation Order</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "Here is the order to compile the design in your simulation or synthesis tool."
  print >> f, "( You can change the designCompileCommand variable to customize compile command)<br>"
  
  compileFileList = []
   
  #Show design Entity
  print >> f, "<h2>Compilation order for %s</h2>"%(designEntity)
  print >> f, "<pre class=\"brush: vhdl;\">"
  #Find levelMax
  levelMax = 0
  for overviewElement in overviewList:
    if overviewElement[HIERARCHY_LEVEL_RK] > levelMax:
      levelMax = overviewElement[HIERARCHY_LEVEL_RK]
       
  #Compile all files by Level order
  #Level Max --> 0
  for ilevel in range(levelMax+1):
    compileLevel = levelMax-ilevel
    for overviewElement in overviewList:
      if overviewElement[HIERARCHY_LEVEL_RK] == compileLevel:
        overviewElementType = overviewElement[HIERARCHY_TYPE_RK]
        overviewElementName = overviewElement[HIERARCHY_NAME_RK]
        
        if overviewElementType == "instance" :
         overviewElementType = "entity"
        elif overviewElementType == "package" :
          m=re.match('^.*\.([A-Za-z0-9_]+)\..*',overviewElementName,re.I) 
          overviewElementName = m.group(1)
        
        for parseElement in parseInfo:
          parseElementFilename = parseElement[FILENAME_RK]
          parseElementType     = parseElement[TYPE_RK]
          parseElementName     = parseElement[TYPE_NAME_RK]
          
          
          if parseElementType == overviewElementType:
            if parseElementName == overviewElementName:
              fileAlreadyCompiled = False
              for compileFileListElement in compileFileList:
                if compileFileListElement == parseElementFilename:
                  fileAlreadyCompiled = True
              if fileAlreadyCompiled == False:    
                print >> f, "%s%s"%(designCompileCommand,parseElementFilename)
                compileFileList.append(parseElementFilename)
  
  #Compile Top Entity
  for parseElement in parseInfo:
    parseElementFilename = parseElement[FILENAME_RK]
    parseElementType     = parseElement[TYPE_RK]
    parseElementName     = parseElement[TYPE_NAME_RK]
    
    if parseElementType == "entity":
      if parseElementName == designEntity:
        print >> f, "%s%s"%(designCompileCommand,parseElementFilename)
        compileFileList.append(parseElementFilename)
  print >> f, "</pre>"
  
  
  #Compliance Overview
  print >> f, "<h1><img src=\"Style/icons/014.png\">  Compliance Overview</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "[To be done!]"
  print >> f, "<br>"
  
  #Comments,Tags statistics
  print >> f, "<h1><img src=\"Style/icons/012.png\">  Comments, Tags Statistics</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "[To be done!]"
  print >> f, "<br>"
  
  
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()
  
  #return
  return compileFileList
  
#======================================
# GenerateDocumentationHtml Function
#======================================
def generateDocumentationHtml():
  #Message
  print " Start Documentation Generation"
  print "------------------------------------------------------------------"

  #Open File
  f = open(htmlDocDir+'\\documentation.html', 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Documentation",0)
  
  #Documenation
  print >> f, "<h1>Documentation</h1>"
  print >> f, "</div>"
  print >> f, "<div id=\"contentMini\">"
  print >> f, "Documentation Synthesis of Design [To Be Done!]"
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()  
       