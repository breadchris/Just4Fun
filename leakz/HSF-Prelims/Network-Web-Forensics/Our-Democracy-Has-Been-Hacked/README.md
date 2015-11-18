HSF 2015: EXIF Metadata Challenge

Challenge Name: Our Democracy Has Been Hacked
Points: 200-250

SETUP:
- Copy all files (including hidden) but not this README into the webroot (/var/www/html/)
- If you want to be nice, enable directory listings

RUNNING INSTRUCTIONS:
- sudo service apache2 start

SOLUTION:
- An old commit message contains the flag. Once teams realize there is a .git folder, they can pull the logs and grep for it.
$ grep -ir flag .
./.git/logs/HEAD:06c6437ce09aa480a5a0cf92af29cecd9c78b5a4 8c71f479d8fb14ea538daa83e26530e0ac43c498 Elliot <elliot@fsociety.com> 1441893495 -0400	commit: flag{nothing_says_holidays_like_a_git_log}
./.git/logs/HEAD:d6309a252dfbdbc3b227144428d183053018006a 7aedf785d86ed92ad6433db55d4018f2100ee7fd Elliot <elliot@fsociety.com> 1441894426 -0400	commit: I think it's pretty obvious. There's really only one thing you can do for a brother in a fish bowl. Give him a false flag.
./.git/logs/HEAD:d2dd3c69459668dff5478ba7c62c6bd044263ec4 54efde9bf7be36eb213d16ba56c61c19c8bc9901 Elliot <elliot@fsociety.com> 1441895038 -0400	commit: We are finally free of all flags!
./.git/logs/HEAD:54efde9bf7be36eb213d16ba56c61c19c8bc9901 6a935bdf537b23cd2d2074fd68494c6b81aa6e87 Elliot <elliot@fsociety.com> 1441895267 -0400	revert: Revert "We are finally free of all flags!"
./.git/logs/refs/heads/master:06c6437ce09aa480a5a0cf92af29cecd9c78b5a4 8c71f479d8fb14ea538daa83e26530e0ac43c498 Elliot <elliot@fsociety.com> 1441893495 -0400	commit: flag{nothing_says_holidays_like_a_git_log}
./.git/logs/refs/heads/master:d6309a252dfbdbc3b227144428d183053018006a 7aedf785d86ed92ad6433db55d4018f2100ee7fd Elliot <elliot@fsociety.com> 1441894426 -0400	commit: I think it's pretty obvious. There's really only one thing you can do for a brother in a fish bowl. Give him a false flag.
./.git/logs/refs/heads/master:d2dd3c69459668dff5478ba7c62c6bd044263ec4 54efde9bf7be36eb213d16ba56c61c19c8bc9901 Elliot <elliot@fsociety.com> 1441895038 -0400	commit: We are finally free of all flags!
./.git/logs/refs/heads/master:54efde9bf7be36eb213d16ba56c61c19c8bc9901 6a935bdf537b23cd2d2074fd68494c6b81aa6e87 Elliot <elliot@fsociety.com> 1441895267 -0400	revert: Revert "We are finally free of all flags!"
Binary file ./.index.html.swp matches
./index.html:       <!-- This is not the flag :) -->
./index.html:       <td id="flag">
./index.html:    document.getElementById("flag").appendChild(pic);
./index.html~:       <td><img src="flag.txt" alt="" /></td>