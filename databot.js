// Global definitions.

 /* global include */

/** TODO Parse input from chat.
 * Involves:
 * $("#message-* div")[0].innerHTML;
 * https://github.com/DennisMitchell/tryitonline/blob/master/html/frontend.js#L67
 * 
 */
 
 var btoa = require('btoa');
 var atob = require('atob');
 
 // From Dennis's TIO repo
 function decode(string) {
	return decodeURIComponent(escape(atob(unescape(string).replace(/-/g, "+").replace(/_/g, "/"))));
}

function encode(string) {
	return btoa(unescape(encodeURIComponent(string))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
}

var uuid = '';
var running = false;

// get TIO output
function run(code, input, language) {
    var XMLHttpRequest = require('./XMLHttpRequest.js').XMLHttpRequest;

    var http = new XMLHttpRequest();
    http.open("POST", "http://"+language+".tryitonline.net/cgi-bin/backend", true);
    
    running = true;
    
    http.onreadystatechange = function() {
        if(running && http.responseText.length > 32) {
            uuid = http.responseText.substr(0,32);
        }
        
        if(http.status == 200 && http.responseText.length < 100033) {
            //console.log(language+": "+http.responseText.substr(33));
        }
        
        if(http.readyState == 4) {
            running = false;
            console.log(language+": "+http.responseText.substr(33));
            process.exit();
        }
    }
    
    http.send("code="+encodeURIComponent(code)+"&input="+encodeURIComponent(input));
}

//run('H', '', 'seriously');
run('+'.repeat(65)+'.', '', 'brainfuck');


/** TODO Output to chat.
 * Involves:
 * document.getElementById("input").value = <output>; 
 * document.getElementById("sayit-button").click();
 * 
 */