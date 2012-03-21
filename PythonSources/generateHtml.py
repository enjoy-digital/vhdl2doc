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
    styleRefDir    = os.path.join(os.curdir,pythonSources,styleDir)
    styleLocalDir = os.path.join(dirElement,styleDir)
    
    if os.path.exists(styleLocalDir):
      rmtree(styleLocalDir)
    copytree(styleRefDir,styleLocalDir) 
   
  #Creat Illustation Directory
  #Create directory
  if os.path.exists(illustationDocDir):
    rmtree(illustationDocDir)
     
  #Copy Illustation Files
  illustationsRefDir = os.path.join(os.curdir,localPathIllustration)    
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
  print("<html>", file=p_file)
  print(" <head>", file=p_file)
  print("  <title>VHDL Documentation %s</title>" %(docTitle), file=p_file)
  
  print("  <link rel=\"stylesheet\" media=\"screen\" type=\"text/css\" title=\"style\" href=\"%s/style.css\" />" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/shCore.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/shBrushVhdl.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/jquery.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/jquery_002.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/footer.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/ga.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/aboutSlider.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/protovis-d3.js\"></script>" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\" src=\"hierarchy.js\"></script>", file=p_file)
  print("  <script type=\"text/javascript\" src=\"%s/javascript/plot_hierarchy.js\"></script>" %(styleDir), file=p_file) 
  print("  <script type=\"text/javascript\" src=\"%s/javascript/back_to_top.js\"></script>" %(styleDir), file=p_file)
   
  print("  <link rel=\"stylesheet\" type=\"text/css\" href=\"%s/javascript/shCore.css\" />" %(styleDir), file=p_file)
  print("  <link rel=\"stylesheet\" type=\"text/css\" href=\"%s/javascript/shThemeDefault.css\" />" %(styleDir), file=p_file)
  print("  <script type=\"text/javascript\">SyntaxHighlighter.all();</script>", file=p_file)
  print(" </head>", file=p_file)
  print("<body>", file=p_file)
          
  print("<div id=\"wrapper\">", file=p_file)
  print(" <div id=\"headwrap\">", file=p_file)	
  print("	  <div class=\"logo\">", file=p_file)
  print(" 	   <a href=\"http://www.enjoy-digital.fr/\" title=\"enjoydigital\" rel=\"home\"><img src=\"%s/images/Vhdl2Doc.png\" alt=\"EnjoyDigital\"></a>" %(styleDir), file=p_file)
  print("   </div>", file=p_file)
  print("   <div id=\"bigTitleCenter\">%s</div>" %(docTitle), file=p_file)
  print("	</div>", file=p_file)
  
  print("<div id=\"content\">", file=p_file)
	
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
  print("<div id=\"worksFilter\" style=\"display: yes;\">", file=p_file)
  print("<ul id=\"filter\" >", file=p_file)
  
  for htmlFilterElement in htmlFilter:
    if active == htmlFilterElement:
      print("<li class=\"active\" id=\"%s\"><a href=\"%s%s.html\" >%s</a></li>" %(htmlFilterElement,rel,str.lower(htmlFilterElement),htmlFilterElement), file=p_file)
    else:
      print("<li id=\"%s\"><a href=\"%s%s.html\" >%s</a></li>" %(htmlFilterElement,rel,str.lower(htmlFilterElement),htmlFilterElement), file=p_file)
         	
  print("</ul>", file=p_file) 
  print("</div>", file=p_file)
  
     
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
  print("<br>", file=p_file)
  print("<br>", file=p_file)
  print("<br>", file=p_file)
  
  #Insert Date / Link / Version
  print("Generated on  %s with <a" %(now.ctime()), file=p_file)
  print("href=\"http://www.enjoy-digital.fr/\">EnjoyDigital VHDL2Doc</a>", file=p_file)
  print(vhdl2DocVersion, file=p_file)
  
  #Presentation
  print("<br>", file=p_file)
  print("<br>", file=p_file)
  
  #Close Content
  print("</div>", file=p_file)
  
  #Start Footer
  print("<div id=\"footer\">", file=p_file)
  print("<div id=\"backToTop\"><a href=\"#\"><img src=\"%s/images/footerBtn.jpg\" alt=\"EnjoyDigital\" /></a></div>" %(styleDir), file=p_file)
  
  print("<script language=\"javascript\">", file=p_file)
  print("back_to_top();", file=p_file)
  print("</script>", file=p_file)
	
  print("<div id=\"footerLeftColumn\">", file=p_file)
  print("<a href=\"http://www.enjoy-digital.fr/\" title=\"enjoydigital\" rel=\"home\"><img src=\"%s/images/EnjoyDigitalGray.png\" alt=\"EnjoyDigital\"></a>" %(styleDir), file=p_file)
  print("</div>", file=p_file)
    
  print("<div id=\"footerRightColumn\">", file=p_file)
  print("<div id=\"footer_contact\"><a href=\"mailto:florent@enjoy-digital.fr\">florent@enjoy-digital.fr</a></div>", file=p_file) 	 
  print("</div>", file=p_file)
  print("</div>", file=p_file)
  
  #Close Footer
  print("</div>", file=p_file)
  
  #Close Body
  print("</body>", file=p_file)
  
  #Close Html
  print("</html>", file=p_file)

#=================================
# insertVhdlCodeHtml Function
#=================================
def insertVhdlCodeHtml(p_file,vhdlFile):

  #Call of SyntaxHilighter
  print("<pre class=\"brush: vhdl;\">", file=p_file)
  
  #Open Vhdl File
  with open(vhdlFile) as p_vhdlFile:
    
    #Read each line
    for line in p_vhdlFile:
      print("%s" %(line), end=' ', file=p_file)
  
  print("</pre>", file=p_file)


#=================================
# listSourcesHtml Function
#=================================
def listSourcesHtml(p_file,fileList,designFileList,srcDir):

  #===============
  # Presentation
  #===============
  print("<h1><img src=\"Style/icons/021.png\">  Source file overview</h1>", file=p_file)
  print("<p>The file paths link to HTML pages showing the sources; the links in brackets point to the actual source files.</p>", file=p_file)
  print("</div>", file=p_file)
  print("<div id=\"contentMini\">", file=p_file)


  #Generate Ordered File List
  designFileListOrdered = listDesignFilesOrdered(fileList,designFileList)
  
  
  #==================
  # Table Generation
  #==================
  
  #Open Table
  print("<table border=\"0\">", file=p_file)
  
  #Start Loop
  for designFile in designFileListOrdered:
    
    #Doc Filename : Add .html to filename
    docFilename  = os.path.join(sourcesDir,os.path.basename(designFile)+".html")
    
    #Show Filename : Remove Sources Base Directory from filename
    showFilename = str.replace(designFile,srcDir,"")
  
    #Presentation
    print("<tr>", file=p_file)
    print("<td>", file=p_file)
    print("<a href=\"%s\">%s</a>&nbsp;&nbsp;&nbsp;</td>" %(docFilename,showFilename), file=p_file)
    print("</tr>", file=p_file)                                                                                                                             
        
  #Close Table
  print("</table>", file=p_file)
  
  
#=================================
# generateSourcesListHtml Function
#=================================
def generateSourcesListHtml(fileList,designFileList,srcDir):

  #Message
  print(" Start Sources Generation")
  print("------------------------------------------------------------------")

  #Open File
  f = open(os.path.join(htmlDocDir,'sources.html'), 'w+')
  
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
    docVhdlFileName = os.path.join(sourcesDocDir,os.path.basename(designFile)+".html") 

    #Open File
    f = open(docVhdlFileName, 'w+')  
  
    #Generate Html Header
    generateHtmlHeader(f)

    #Generate Html Filter
    generateHtmlFilter(f,"Sources",1)
    
    #Show FileName
    print("<h1><img src=\"Style/icons/028.png\">  Source file %s</h1>" %(os.path.basename(designFile)), file=f)
    print("</div>", file=f)
    print("<div id=\"contentMini\">", file=f)

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
  print(" Start Home Generation")
  print("------------------------------------------------------------------")

   #Open File
  f = open(os.path.join(htmlDocDir,'home.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Home",0)
  
  #Show Project Description
  print("<h1><img src=\"Style/icons/019.png\">  Design brief</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
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
  print("<h1><img src=\"Style/icons/024.png\">  Hierarchy Quick Overview</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("<div id=\"contentHierarchy\">", file=f)
  
  
  print("<b>[<a href=\"%s\" target=\"_blank\" >%s</a>]</b>:" %("Entities/work."+designEntity+".html",designEntity), file=f)
  print("<br>", file=f) 
  #Loop on designHierarchyFileList
  for designHierarchyElement in designHierarchyFileList:
    designLevel = designHierarchyElement[HIERARCHY_LEVEL_RK]
    designType  = designHierarchyElement[HIERARCHY_TYPE_RK]
    designName  = designHierarchyElement[HIERARCHY_NAME_RK]
  
    
    #for i in range(designLevel):
    #  print >> f, "&nbsp&nbsp<img src=\"Grey Ball.png\">"
      
    #print >> f, "&nbsp&nbsp<img src=\"Add Green Button.png\">"  
    
    
    for i in range(designLevel):
      print("&nbsp&nbsp|", file=f)
      
    print("&nbsp&nbsp+", file=f)  
    
    if designType == "instance":
      if isEntityLinkTo(designName):          
        print("<b>[<a href=\"%s\" target=\"_blank\">%s</a>]</b>:" %("Entities/work."+designName+".html",designName), file=f)
      else:
        print("<b>[%s]</b>:" %designName, file=f)
      
    else:
      m=re.match('^([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)',designName,re.I)
      if compareString(m.group(1),"ieee"):
        print("<i>%s.%s.%s</i>:" %(m.group(1),m.group(2),m.group(3)), file=f)
      else:
        print("<i>%s.[<a href=\"%s\" target=\"_blank\">%s</a>].%s</i>:" %(m.group(1),"Packages/"+m.group(1)+"."+m.group(2)+".html",m.group(2),m.group(3)), file=f)
        
    print("<br>", file=f)   
  
  print("</div>", file=f)
  
  #Show Design Stats
  print("<h1><img src=\"Style/icons/012.png\">  Design statistics</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("Statistics based on parsed files<br><br>", file=f)
  for parseStatElement in parseStat: 
    print("Nb %s : %s<br>" %(parseStatElement[1],parseStatElement[0]), file=f)
  
  print("<br>", file=f)
  
  
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()
  
  
#======================================
# GenerateAboutHtml Function
#======================================
def generateAboutHtml():
  #Message
  print(" Start About Generation")
  print("------------------------------------------------------------------")

  #Open File
  f = open(os.path.join(htmlDocDir,'about.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"About",0)
  
  #Why Vhdl2Doc
  print("<h1><img src=\"Style/icons/023.png\">  Why Vhdl2Doc?</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("I'm sometimes a bit lazy and have search last year on the net for an automatic documentation for VHDL code without success.", file=f)
  print("That's why I decided to develop my own tool, I hope it will be useful for someone else ;-)", file=f)
  
  #What can be done with Vhdl2Doc
  print("<h1><img src=\"Style/icons/023.png\"> How can Vhdl2Doc be useful?</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("Vhdl2Doc is useful for automatic VHDL documentation.", file=f)
  print("It can be used for a new project where specifics Tags will be used", end=' ', file=f)
  print("to enhance documentation (Comments, Descriptions, Schematics, Synoptics,etc... See Below)", file=f)
  print("It can also be used to understand old projects where documentation is lost or very brief, it will allow to recover easily", end=' ', file=f)
  print("design hierarchy, to navigates in entities, packages, etc...", file=f)
  
  #How it Works
  print("<h1><img src=\"Style/icons/023.png\"> How it works?</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("<img src=\"%s/images/Vhdl2DocSynoptic.png\" alt=\"EnjoyDigital\">" %(styleDir), file=f)
  print("Vhdl2Doc is developped in Python.", file=f)
  print("You put all your VHDL files in a folder, Vhdl2Doc search the Vhdl files in this folder, analyse the files,", file=f)
  print("find the optional documentation Tags you put in the code, etc...", file=f)
  print("Once it's done, it propose you the possible design Top found in the repertory, you choose it and it will do the rest.", file=f)
  
  #Documentation Tags examples
  #Comments
  print("<h1><img src=\"Style/icons/022.png\"> Documentation Tags examples:</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("<h2>Insertion of Comments in the documentation:</h2>", file=f)
  print("<pre class=\"brush: vhdl;\">", file=f)
  print("  --* This process defines a counter.  This is just to demonstrate", file=f)
  print("  --* how Vhdl2Doc documentation comments can extend over several ", file=f)
  print("  --* comment lines.", file=f)
  print("  --*""", file=f)
  print("  --* Here is a second paragraph, again designed to show", file=f)
  print("  --* how to write documentation for Vhdl2Doc.", file=f)
  print("  Counter_p : process( rst_n, clk ) is", file=f)
  print("  begin", file=f)
  print("    if rst_n = '0' then ", file=f)
  print("      counter <= (others => '0');", file=f)
  print("    elsif rising_edge(clk) then ", file=f)
  print("      counter <= counter + 1;", file=f)
  print("    end if;  ", file=f)
  print("  end process Counter_p; ", file=f)
  print("</pre>", file=f)
  print("<br>", file=f)
  
  #Description
  print("<h2>Insertion of detailed information:</h2>", file=f)
  print("<pre class=\"brush: vhdl;\">", file=f)
  
  print("--------------------------------------------------------------------------------", file=f)
  print("--                            Entite                                            ", file=f)
  print("--------------------------------------------------------------------------------", file=f)
  print("--* @link     [entity] [PwmDeadTime]                                             ", file=f)
  print("--* @brief    Ce module gere la protection sur la commuation des Mos de pont en H", file=f)
  print("--* @details  Il realise:                                                         ", file=f)
  print("--* @details  - l'inversion des signaux de commandes des Mos High et Low          ", file=f)
  print("--* @fig      [Inversion Mos High et Low] [Inversion_Mos_High_Low.png]            ", file=f)
  print("--* @details  - l'application d'un retard a la commutation pour compenser le delai", file=f)
  print("--*           de desactivation du Mos et eviter les bref courts circuits.         ", file=f)
  print("--* @fig      [Retard a la commutation] [Retard_A_La_Commutation.png]             ", file=f)
  print("--------------------------------------------------------------------------------  ", file=f)
  print("entity PwmDeadTime is                                                             ", file=f)
  print("generic (                                                                         ", file=f)
  print("  PWM_NB     : natural := 3;          -- Nombre de voies PWM                      ", file=f)
  print("  CLK_PERIOD : real    := 33.0;       -- Periode de l'horloge (ns)                ", file=f)
  print("  DEAD_TIME  : real    := 0.6);       -- Dead Time Commutation Mos (us)           ", file=f)
  print("port (                                                                            ", file=f)
  print("   clk             : in std_logic;                                                ", file=f)
  print("  rst_n           : in std_logic;                                                 ", file=f)
  print("  switch_n        : in std_logic;                                                 ", file=f)
  print("  pwmNoDeadTime   : in unsigned(PWM_NB-1 downto 0);                               ", file=f)
  print("  pwmWithDeadTime : in unsigned(2*PWM_NB-1 downto 0)                              ", file=f)
  print("  );                                                                              ", file=f)
  print("end PwmDeadTime;                                                                  ", file=f)
  print("</pre>", file=f)
  print("<br>", file=f)
  print("Here are some examples of Tags use:<br>", file=f)
  print("- Use @link    Tag to link the next Tags to specific Element<br>", file=f)
  print("- Use @brief   Tag to insert brief of the Elemetn(entity,package,process,instance,etc...)<br>", file=f)
  print("- Use @details Tag to insert more information about the element.<br>", file=f)
  print("- Use @req     Tag to specify to which requirement the element belongs.<br>", file=f)
  print("- Use @version Tag to specify to which version of the requirement the element belongs.<br>", file=f)
  print("- Use @fig     Tag to insert a figure of a schematic, synoptic, chronogram...<br>", file=f)
  print("Each Tags can be used more than one time for each element<br>", file=f)
  print("<br>", file=f)
  print("link is valid until a non-comment line is found<br>", file=f)
  
  #Todo List and limitations
  print("<h1><img src=\"Style/icons/016.png\">  Todo List and Limitations: (Vhdl2Doc %s , %s)</h1>" %(vhdl2DocVersion,vhdl2DocDate), file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("<h2>Todo</h2><br>", file=f)
  print(" - Code Latex engine to generate PostScript,Pdf documentation<br>", file=f)
  print(" - Move parts of hierarchy search done in Html Generation to Hierarchy engine(For Reuse in Latex)<br>", file=f)
  print(" - Test & Improve parse engine on more designs and files<br>", file=f)
  print(" - Improve hierarchy engine<br>", file=f)
  print(" - Improve documentation presentation<br>", file=f)
  print(" - Add more Documentation Tags<br>", file=f)
  print(" - Etc...<br>", file=f)
  print("<br>", file=f)
  print("You have ideas to improve Vhdl2Doc or want a specific function, feel free to contact me!<br>", file=f)
  
  print("<h2>Limitations</h2><br>", file=f)
  print(" - More tests needs to be done one each engine(Parse,Hierarchy)<br>", file=f)
  print(" - I'have test those engines on several designs. Still, it is possible that your", file=f)
  print("design may be incorrectly parsed. If so, you can help me greatly by sending me a copy of", file=f)
  print("the VHDL files witch failed to be parsed", file=f)

  
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
            print("<h2>"+dataString+"</h2>", file=f)
          else:
            print("<br>", file=f)
            print("<h2>"+dataString+"</h2>", file=f)
      #Or something else
      else: 
          if not dataIsValid:
            if firstBrief == False:
              print("<br>", file=f)
              print("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+dataString, file=f)
            else:
              print("&nbsp;&nbsp;&nbsp;&nbsp;"+dataString, file=f)
            firstBrief = False
          else:
            print(dataString, file=f) 
            
            
    # Tag Details        
    elif dataType == "details":
      if dataIsValid:
        print(dataString, file=f)
      else:
        print("<br>", file=f)
        print(dataString, file=f)
         
    # Tag Fig                
    elif dataType == "fig":
      if isHome:
        print("<br><div id=\"centerImg\"><img src=\"./%s/%s\" alt=\"EnjoyDigital\"><br>%s</div>" %(illustationsDir,dataFigFilename,dataFigName), file=f)
      else:       
        print("<br><div id=\"centerImg\"><img src=\"../%s/%s\" alt=\"EnjoyDigital\"><br>%s</div>" %(illustationsDir,dataFigFilename,dataFigName), file=f)
  
  
  
#======================================
# GenerateEntitiesHtml Function
#======================================
def generateEntitiesHtml(entityName,libraryName,srcDir):

  #Open File
  f = open(os.path.join(entitiesDocDir,libraryName+"."+entityName+'.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Entities",1)
  
  #Title
  print("<h1><img src=\"Style/icons/028.png\">  Entity %s.%s </h1>" %(libraryName,entityName), file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  
  #Retrieve fileName
  entityFilename = retrieveFilenameElement(parseInfo,"entity",entityName)             
  docVhdlFileName = "../"+sourcesDir +"/" + os.path.basename(entityFilename)+".html"
  showVhdlFileName = str.replace(entityFilename,srcDir,"")
  
  ######################
  #Show Entity & Tags
  ######################
           
  print("File <a href=\""+docVhdlFileName+"\">"+showVhdlFileName+"</a><br>", file=f)
  tagInsertionHtml(f,entityFilename,"entity",entityName,False)
  
  
  ######################
  #Show Libraries
  ######################
  print("<h2><img src=\"Style/icons/006.png\">  Libraries</h2>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  
  #Get Library corresponding to File
  libraryList = listLibrary(entityFilename)
  
  #Start Table
  print("<table border=\"0\">", file=f)
  
  currentLibrary = ""
  
  for library in libraryList:
  
    libraryType       = library[0]
    libraryName       = library[1]
    libraryReduceName = library[2]
    libraryIsInDesign = library[3]
  
    if libraryType == "library":
      print("<tr><td>Library "+libraryName+"</a></td></tr>", file=f)
      currentLibrary = libraryName
    elif libraryType == "use":
      linkUseName = "../packages/"+currentLibrary+"."+libraryReduceName+".html"
      
      if libraryIsInDesign:
        print("<tr><td>Use <a href=\""+linkUseName+"\">"+libraryName+"</a></td></tr>", file=f)
      else:
        print("<tr><td>Use "+libraryName+"</td></tr>", file=f)            
        
   #End Table
  print("</table>", file=f)      
        
  ######################
  #Show Signals
  ######################
  print("<h2><img src=\"Style/icons/006.png\">  Ports</h2>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  
  #Get Library corresponding to Entity
  signalList = listSignal(entityName)
  
  #Start Syntax Hilighting
  print("<pre class=\"brush: vhdl;\">", file=f)
  
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
      
    print("%s%s%s%s%s" %(signalName,spaceFirst,signalDirection,spaceSecond,signalType), file=f)        
              
  #End SyntaxHilighting
  print("</pre>", file=f)
                
  ######################
  #Show Architecture
  ######################
  print("<h2><img src=\"Style/icons/006.png\">  Architecture ", end=' ', file=f)
    
  #Get Library corresponding to Entity
  architectureList = listArchitecture(entityName)
  
  for architecture in architectureList:
        print("["+architecture+"]</h2>", file=f)           
        print("</div>", file=f)
        print("<div id=\"%s\"></div>" %architecture, file=f)
        print("<div id=\"contentArchitecture\">", file=f)       
  
  
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
          print("<h2><img src=\"Style/icons/002.png\">  Instances</h2>", file=f)
          print("</div>", file=f)
          print("<div id=\"contentArchitecture\">", file=f)
          
        #Start Table
        print("<table border=\"0\">", file=f)       
        print("<tr>", file=f)
        print("<td>", file=f)
        print(instanceName+"&nbsp;&nbsp;&nbsp;", file=f)
        print("</td>", file=f)
        print("<td>", file=f)
        print(instanceEntityName, file=f)
        print("</td>", file=f)
        print("</tr>", file=f)
        #End Table
        print("</table>", file=f)
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
          print("<h2><img src=\"Style/icons/002.png\">  Processes</h2>", file=f)
          print("</div>", file=f)
          print("<div id=\"contentArchitecture\">", file=f)
       
        #Start Table
        print("<table border=\"0\">", file=f)              
        print("<tr>", file=f)
        print("<td>", file=f)
        print(processName+"&nbsp;&nbsp;&nbsp;", file=f)
        print("</td>", file=f)
        print("<td>", file=f)
        print(processSensitivity, file=f)
        print("</td>", file=f)
        print("</tr>", file=f)
        #End Table
        print("</table>", file=f)
        #Show Entity Tags
        tagInsertionHtml(f,entityFilename,"process",processName,False)           
        

     
  
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
     
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()

    
#======================================
# GenerateEntitiesListHtml Function
#======================================
def generateEntitiesListHtml(designFileList,libraryName,srcDir):
  
  #Message
  print(" Start Entities Generation")
  print("------------------------------------------------------------------")

  #Open File
  f = open(os.path.join(htmlDocDir,'entities.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Entities",0)
  
  #Title
  print("<h1><img src=\"Style/icons/021.png\">  List of entities and architectures</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  #Start Table
  print("<table border=\"0\">", file=f)
  
  for entityParseElement in parseInfo:
  
    for checkCompiled in designFileList:
      if entityParseElement[FILENAME_RK] == checkCompiled:
  
        if entityParseElement[TYPE_RK] == "entity":
          entityName = entityParseElement[ENTITY_NAME_RK]
    
          for architectureParseElement in parseInfo:
            if architectureParseElement[TYPE_RK] == "architecture":
              if  entityName ==  architectureParseElement[ARCHITECTURE_ENTITY_NAME_RK]:
                architectureName = architectureParseElement[ARCHITECTURE_NAME_RK]
            
          print("<tr><td><a href=\"Entities/%s.%s.html\">%s.%s</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td><a href=\"Entities/%s.%s.html#%s\">[%s]</a></td></tr>" %(libraryName,entityName,libraryName,entityName,libraryName,entityName,architectureName,architectureName), file=f)
      
          generateEntitiesHtml(entityName,libraryName,srcDir)
  
  
  #End Table
  print("</table>", file=f)
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
  f = open(os.path.join(packagesDocDir,libraryName+"."+packageName+'.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Packages",1)
  
  #Title                        
  print("<h1><img src=\"Style/icons/028.png\">  Package %s.%s </h1>" %(libraryName,packageName), file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  
  #Retrieve fileName 
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "package":
      packageNameElement    = parseElement[PACKAGE_NAME_RK]
      if str.upper(packageName) == str.upper(packageNameElement):
        packageFilename = parseElement[FILENAME_RK]
        
  docVhdlFileName = "../"+sourcesDir +"/" + os.path.splitext(os.path.basename(packageFilename))[0]+".vhd.html"
  showVhdlFileName = str.replace(packageFilename,srcDir,"")
  print("File <a href=\""+docVhdlFileName+"\">"+showVhdlFileName+"</a><br>", file=f)
  
  
  #Find Library                  
  print("<h2><img src=\"Style/icons/006.png\">  Libraries</h2>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  #Start Table
  print("<table border=\"0\">", file=f)
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "library":
      libraryElementName     =  parseElement[LIBRARY_NAME_RK]
      libraryElementFilename =  parseElement[FILENAME_RK] 
      if str.upper(libraryElementFilename) == str.upper(packageFilename):
        print("<tr><td>Library "+libraryName+"</a></td></tr>", file=f)
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
          print("<tr><td>Use <a href=\""+linkUseName+"\">"+useElementName+"</a></td></tr>", file=f)
        else:
          print("<tr><td>Use "+useElementName+"</td></tr>", file=f)
            
        
   #End Table
  print("</table>", file=f)
  

  #Find Component
  print("<h2><img src=\"Style/icons/006.png\">  Components</h2>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  #Start Table
  print("<table border=\"0\">", file=f)
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "component":
      componentName     =  parseElement[COMPONENT_NAME_RK]
      componentFilename =  parseElement[FILENAME_RK] 
      if str.upper(componentFilename) == str.upper(packageFilename):
        print("<tr>", file=f)
        print("<td>", file=f)
        print(componentName+"&nbsp;&nbsp;&nbsp;", file=f)
        print("</td>", file=f)
        print("<td>", file=f)
        entityLink = "../../"+entitiesDocDir +"/"+libraryName+"."+componentName+".html"
        print("<a href=\"%s\">[default binding]</a>" %entityLink, file=f)
        print("</td>", file=f)
        print("</tr>", file=f)
  #End Table
  print("</table>", file=f)      
        
  #Find Function
  print("<h2><img src=\"Style/icons/006.png\">  Functions</h2>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  #Start Table
  print("<table border=\"0\">", file=f)
  for parseElement in parseInfo:
    elementType = parseElement[TYPE_RK]
    if elementType == "function":
      functionName     =  parseElement[COMPONENT_NAME_RK]
      functionFilename =  parseElement[FILENAME_RK] 
      if str.upper(functionFilename) == str.upper(functionFilename):
        print("<tr>", file=f)
        print("<td>", file=f)
        print(functionName+"&nbsp;&nbsp;&nbsp;", file=f)
        print("</td>", file=f)
        print("</tr>", file=f)      
        
   #End Table
  print("</table>", file=f)


  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()
  

#======================================
# GeneratePackageListHtml Function
#======================================
def generatePackageListHtml(designFileList,libraryName,srcDir):

  #Message
  print(" Start Packages Generation")
  print("------------------------------------------------------------------")

  #Open File
  f = open(os.path.join(htmlDocDir,'packages.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Packages",0)
  
  #Title
  print("<h1><img src=\"Style/icons/021.png\">  List of packages</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  
  #Start Table
  print("<table border=\"0\">", file=f)
   
  for packageParseElement in parseInfo:
  
   for checkCompiled in designFileList:
      if packageParseElement[FILENAME_RK] == checkCompiled:
      
        if packageParseElement[TYPE_RK] == "package":
          packageName = packageParseElement[USE_NAME_RK]
          print("<tr><td><a href=Packages/"+libraryName+"."+packageName+".html>"+packageName+"</a></td></tr>", file=f)                                              
          generatePackagesHtml(packageName,libraryName,srcDir)    
  
   #End Table
  print("</table>", file=f)
     
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()  
  
#======================================
# GenerateUtilsHtml Function
#======================================
def generateUtilsHtml(designEntity,overviewList):
  #Message
  print(" Start Utils Generation")
  print("------------------------------------------------------------------")

  #Open File
  f = open(os.path.join(htmlDocDir,'utils.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Utils",0)
  
  #Summary  
  print("Some functions that can be useful:", file=f) 
  
  #Why Compilation order
  print("<h1><img src=\"Style/icons/010.png\">  Compilation Order</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("Here is the order to compile the design in your simulation or synthesis tool.", file=f)
  
  compileFileList = []
   
  #Show design Entity
  print("<h2>Compilation order for %s</h2>"%(designEntity), file=f)
  print("<pre class=\"brush: vhdl;\">", file=f)
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
                print("%s"%(parseElementFilename), file=f)
                compileFileList.append(parseElementFilename)
  
  #Compile Top Entity
  for parseElement in parseInfo:
    parseElementFilename = parseElement[FILENAME_RK]
    parseElementType     = parseElement[TYPE_RK]
    parseElementName     = parseElement[TYPE_NAME_RK]
    
    if parseElementType == "entity":
      if parseElementName == designEntity:
        print("%s"%(parseElementFilename), file=f)
        compileFileList.append(parseElementFilename)
  print("</pre>", file=f)
  
  #Comments,Tags statistics
  print("<h1><img src=\"Style/icons/012.png\">  Comments, Tags Statistics</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("[To be done!]", file=f)
  print("<br>", file=f)
  
  
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
  print(" Start Documentation Generation")
  print("------------------------------------------------------------------")

  #Open File
  f = open(os.path.join(htmlDocDir,'documentation.html'), 'w+')
  
  #Generate Html Header
  generateHtmlHeader(f)

  #Generate Html Filter
  generateHtmlFilter(f,"Documentation",0)
  
  #Documenation
  print("<h1>Documentation</h1>", file=f)
  print("</div>", file=f)
  print("<div id=\"contentMini\">", file=f)
  print("Documentation Synthesis of Design [To Be Done!]", file=f)
  #Generate Html Footer
  generateHtmlFooter(f)

  #Close File
  f.close()  
       
