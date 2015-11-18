# HSF-Prelims
Preliminary Challenges for HSF


## Categories
* Cryptography
    * Where is My Key
        * Tested - Chris
        * Writeup
        * Solution script
    * Caesar (Julius)
        * Tested - Chris, Marc
        * Writeup
        * Solution script
        * MB - Solution: rot13
    * Counting Semaphores
        * Tested - Chris, Momo, Marc
        * Writeup
        * MB - Solution: compile program (gcc anderson.c) and execute to generate mapping for alphabet
    * Down the Rabbit Hole
        * Writeup
        * MB - This challenge seems doable, but even with the previous commit that shows the word taken from each paragraph I cant get my script to run for more than 3 letters.
    * Back to Bas6
        * Tested - Chris, Marc
        * Writeup
        * Solution script
    * More Than One
        * Tested - Chris
        * Writeup
        * Solution script
    * Only One
        * Tested - Chris
        * Writeup
        * Solution script
    * Mr. Skeletal (What do you Say)
        * Tested - Chris, Marc
        * MB - Solution Script Added
* Disk Forensics
    * Cats
        * Note - We need to have something on the site to tell students this is a 7+GB file. Can we up the compression or something to reduce file size? 7z?
    * GG Filesystem
        * Tested - Marc
        * MB - Solution: strings filesystem | grep 'flag{'
    * JustDoIt
* File Forensics
    * Abracadabra
        * Tested (Locally) - Marc
        * Solution Script provided with Challenge
    * Glad Bags
        * Tested - Momo, Marc
        * Writeup
        * MB - Solution Steps added
    * True Cryptography
    * Match the Hash
        * Tested - Chris, Marc
        * Writeup
        * MB - Solution Script added
    * Club Going Europe on a Tuesday
        * Tested - Kyle, Marc
        * MB - Solution: zip2john hungry.zip > zip.hash; john zip.hash
    * Git it Got it Good
        * Tested - Chris, Marc
        * MB - Solution: Check out previous commits and cat s3cr3t
    * What are Th000000se
        * Tested - Chris, Marc
        * Solution script
        * MB - sol.py added
* Photo-rensics 
    * All of Them
        * Tested - Chris, Nick, Marc
    * Secret Meeting
        * Tested - Chris, Marc
        * Writeup
        * MB - Solution: exiftool sceneOfTheCrime.jpg
    * Ides of March
        * Tested
    * Meta Meta Meta
        * Tested (Locally) - Marc
        * Solution Script Provided with Challenge
    * Movie Night
        * Tested - Chris, Momo
* Network / Web Forensics
    * Burritos
    * Instapwn
        * Tested - Nick, Chris, Marc
    * OMG DOGS
        * Issues - Marc
        * MB - Attempted solution added. File that is generated does not open.
    * OTP-Fun
    * You Got Mail
        * ~~Is this the nitroba capture? If so, do we have permission to redistribute/utilize for the competition?~~ Looking at the capture in wireshark, it is. Second question still remains: can we redistribute?
        * Added Nitroba Slidedeck. The answers posted look wrong - Lily Tuckridge is the recipient. Also, I'm pretty sure the OS from the UA string is Windows - I dont have the answers in front of me right now, but from what I remember, the MAC address ties back to Apple, but the UA string is Firefox on Windows.
    * Do Not Support
        * Tested - Chris, Marc
        * Writeup
        * MB - Solution: dig -t txt cyber-ninja.xyz
    * Obfuscript
    * Our Democracy Has Been Hacked
        * Tested (Locally) - Marc
        * MB - Solution: clone git repo, grep logs
    * Styx
        * Tested - Chris, Nick, Marc
    * So Board
        * Tested - Chris
        * MB - Flag wasn't being accepted on site
* Reversing
    * Droid
    * Zipped Up Jacket
        * Tested - Chris, Marc
        * MB - Solution: strings have_some_fun.apk | grep flag
    * Malrio Ware
        * Tested - Chris
        * Writeup
    * PHP 4 Lyfe
        * Tested
    * Somewhere In There
        * Tested - Marc
        * MB - Solution: strings somewhere
    * Varrick
        * Tested - Marc
        * MB - sol.py added. Based off of c code, possible to reconstruct from IDA disassembly
    * Graphic
        * MB - too lazy to write it, but seems doable with Z3 pretty easily
* Steganography
    * What's the Difference
        * Writeup
    * Andromeda
        * Tested - Chris
        * Writeup
    * Cheaptrix
        * Tested - Chris
        * Writeup
    * Skeuomorphic
