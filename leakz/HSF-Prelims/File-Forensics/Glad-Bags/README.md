#Solution
​
## Directory Tree
      GLAD.docx
         |
        pptx
         |     
      .secret --- stuff.rar --- _ppt contents_
         |            | 
         |      _ppt contents_
         |
     narnia.cab ----- chicken.pdf ----- nin.ja 
         |
   skinking.wmz ----- trump.log ----- HelloWorld.depend ----- HelloWorld.layout ----- main.o
         |
       Doom ----- dat.ass ----- flush.7z -----flush ----- glad.7z ----- glad ----- lqm files----- _bitmaps_
        |                          |            |
        |                          |           42.zip ----- cat pix
        |                         42.zip ----- cat pix
CAN'T FRUMP THE TRUMP.DOCX ----- flag.zip
        |                              |
*flag.png* ----- _docx contents_   1-4321.txt ----- Mountain Dew.ppt ----- deeper.zip
                         
_If you follow the leftmost side, you will reach the real flag._


The GLAD.docx file cannot be opened in Microsoft Word. However, upon using `file`, the docx file is marked as a ZIP archive file. Using `unzip`, the extracted folder reveals that the .docx file was actually a Powerpoint file. The extracted folder, pptx, contains stuff.rar, normal contents of a powerpoint, and a hidden directory named .secret. Within .secret is narnia.cab, chicken.pdf, and nin.ja. `unzip`ping a cabinet file will not work, but using `7z x` will. Within narnia.cab is skinking.wmz, trump.log, HelloWorld.depend, HellowWorld.layout, and main.o. skinking.wmz can be `unzip`ped. Using `file, Doom is a LHa archive file. Extracted properly with `jlha`, a .docx and .zip file should appear. However, `unzip` can be used as well and picks up only on the contents of the .docx file, revealing the flag in a screenshot of a .docx.


42.zip, glad.7z, glad, and deeper.zip are zip bombs.
