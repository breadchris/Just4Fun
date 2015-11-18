//key defaults
var keyString = "";
var keyNumber = 0;
var keyBool = false;

//global counter
var counter = 0;

//page elements
var cp = document.getElementById('controlPanel');
var us = document.getElementById('userString');
var un = document.getElementById('userNumber');
var ub = document.getElementById('userBool');

//buttons
document.getElementById('b1').onclick = function(){counter+=true;};
document.getElementById('b2').onclick = function(){updateKey(0,keyString+"thank mr. skeletal");};
document.getElementById('b3').onclick = function(){updateKey(0, String.fromCharCode(77)+String.fromCharCode(69)+String.fromCharCode(79)+String.fromCharCode(87))};
document.getElementById('b4').onclick = function(){updateKey(1, keyNumber<<counter);};
document.getElementById('b5').onclick = function(){updateKey(1, ((new Date().getTime())%(([]+{}).split("c")[2]).length==(true-true))?(new Date().getTime()):Math.floor(Math.random()*10*(true+true+true)));};
document.getElementById('b6').onclick = function(){updateKey(0,keyString+(typeof(NaN))[counter]);};
document.getElementById('b7').onclick = function(){updateKey(1, parseInt(keyNumber)+~[]);};
document.getElementById('b8').onclick = function(){updateKey(0, keyString+String.fromCharCode(counter));};
document.getElementById('b9').onclick = function(){counter=false-false;};
document.getElementById('b10').onclick = function(){updateKey(2,keyBool||((Math.floor(Math.random()*100)%2==0)||!keyBool));};
document.getElementById('b11').onclick = function(){updateKey(0, keyString+([]+{})[counter]);};
document.getElementById('b12').onclick = function(){updateKey(1, parseInt(keyNumber)/(Array(16).join("divr").length%29));};

function wrong(){	
}
function right(){
	document.getElementById('helper').style.color="blue";
	document.getElementById('helper').innerHTML="Correct!";
	//Credz 2 kiwiz https://github.com/kiwiz
	document.getElementById('cancan').style.zIndex="723";
	Nyan.initialize(); Nyan.run(); Nyan.addCat();
}
function updateKey(keyType, keyValue){
	switch(keyType){
		case(0):
			keyString = keyValue;
			us.innerHTML = keyValue;
			break;
		case(1):
			keyNumber = Math.floor(parseInt(keyValue));
			un.innerHTML = ([]+[]) + Math.floor(parseInt(keyValue));
			break;
		case(2):
			keyBool = keyValue;
			ub.innerHTML = ([]+[]) + keyValue;
			break;
	}
	(keyString ==(([]+[])+(([]+{})[1]&&true)+typeof({}+{})).slice(-12,-4)+(++[[]][+[]]+[+[]])+([]+{}[1])[4]+(typeof(NaN))[5]+(Array(2<<3).join("wat").length-11)+~ [] * ((((+((([]+{}).replace("[","4").replace("ct","gh").replace(" ","").split("j").sort()[0][0])+5) - 13) << 6) + ~ []) >> 2)) ? ((keyNumber%(['10','10','10','10'].map(parseInt)[2])==0)&&(keyNumber%(Array(9).join("wat").length)==parseInt(1 / 0, 19))&&(keyNumber>parseInt("0xf", 10))&&(~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~keyNumber & 69 | ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~69 & keyNumber)&&(keyNumber< Array(20).join([]+{}).length)) ? (keyBool==(([0]==![0]&&NaN===NaN&&(null instanceof Object))||(("string" instanceof String)==(true+false==1))&&(!!("0")))) ? right() : wrong()  : wrong() : wrong();
}
