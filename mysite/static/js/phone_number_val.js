
window.onload = function(){ 


var phoneField = document.getElementById('phoneNumber');
    phoneField.addEventListener('keyup', function(){
    var phoneValue = phoneField.value || "";
    var output;
    phoneValue = phoneValue.replace(/[^0-9]/g, '');
    var areas = phoneValue.substr(0,1);
    var area = phoneValue.substr(1, 3);
    var pre = phoneValue.substr(4, 3);
    var tel = phoneValue.substr(7, 2);
    var tele = phoneValue.substr(9, 2);
    var anyString = '87075822613';
    if(!phoneValue) {
        output = "";
    }
    if (areas.length == 1 && area.length == 0) {
      console.log(anyString.substring(1, 4));
      console.log(anyString.substring(4, 7));
      console.log(anyString.substring(8, 11));
      console.log(anyString.substring(0, 11));
      output = areas +"(";   
    }
    else if (areas.length == 1 && area.length > 0 && area.length <3  ) {
      output =  areas +"(" + area;
    
  }
    else if (phoneValue.length >= 4 && phoneValue.length < 7) {
        output = areas + "(" + area + ")" + " " + pre;
    } else if (phoneValue.length >= 7 && phoneValue.length < 9) {
        output =areas + "(" + area + ")" + " " + pre + "-"+tel;
    }
    else if (phoneValue.length >= 9  ) {
      output =areas + "(" + area + ")" + " " + pre + "-"+tel +"-"+tele;
  }
  phoneField.value = output;

});

var phone = document.getElementById('phoneNumber'),
cleanPhoneNumber;

cleanPhoneNumber= function(e) {
e.preventDefault();
var pastedText = '';
if (window.clipboardData && window.clipboardData.getData) {
pastedText = window.clipboardData.getData('Text');
} else if (e.clipboardData && e.clipboardData.getData) {
pastedText = e.clipboardData.getData('text/plain');
}
this.value = pastedText.replace(/\D/g, '');
};
window.onload = function(){
phone.onpaste = cleanPhoneNumber;
}
}



