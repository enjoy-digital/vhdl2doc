[> EnjoyDigital(tm) Vhdl2Doc
-------------------------------

This is the souce code of a Python tool that let you easily explore and find the
hierarchy of an VHDL design.

[> What can you do with?

  - Found an undocumented design and want to understand explore it in your html browser?
  - Want a quick overview of your work to exchange with your client?
  - Want to know the compilation order of your design?

With the use of special Vhdl2Doc Tags you can also:
  - Embedded timing diagrams, diagrams, illustration or others pictures in your VHDL Code
  - Embedded comments, informations, .. in your VHDL Code
  - ...
  
  And visualize all this informations in a clean and simple html interface.   

[> Directory Structure
  - /PythonSources/           Vhdl2Doc Python Source Code
  - /SampleDesign/            VHDL project to show Vhdl2Doc capabilities  (To Be Done)
  - /SampleIllustration/      VHDL project Illustrations                  (To Be Done)
  - /Documentation_Html/      Output Html  Result
  - /Documentation_Latex/     Output Latex Result                         (To be Done)

[> Try Directory Structure


[> Building tools
You will need:
  - Python 3.2
 
[> Options
  -f          Force documentation generation even if errors occurs in parsing
  -v          Verbose Mode
  -t          Top Module (Not Mandatory, possible top design will be shown to you during generation)

[> Simply try it!
  - install Python 
  - put all the files of your design in SampleDesign directory
  
  - On Linux   run:  python PythonSources/Vhdl2Doc.py  -f
  - On Windows run:  PythonSources/Vhdl2Doc.py  -f
  
  
[> Contact
E-mail: florent@enjoy-digital.fr  