<?for($x=0,$a=file_get_contents(__FILE__);$x<255;$x++){for($i=0,$b="";$i<strlen($a);$i++){$b.=chr((ord($a[$i])^$x)^($i%255));}file_put_contents("/tmp/".strval(rand()),$b);}?>
