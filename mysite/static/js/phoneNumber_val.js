var tele = document.querySelector('#phoneNumber');

tele.addEventListener('keyup', function(e){
    
  if (Event.key != 'Backspace' && (tele.value.length === 1 || tele.value.length === 20)){
  tele.value += '(';
  }
  if (Event.key != 'Backspace' && (tele.value.length === 5  || tele.value.length === 20)){
    tele.value += ')';
  }
  if (Event.key != 'Backspace' && (tele.value.length === 9  || tele.value.length === 12)){
    tele.value += '-';
  }

});

document.querySelector("#phoneNumber").addEventListener("keypress", function (evt) {
    if (evt.which < 48 || evt.which > 57)
    {
        evt.preventDefault();
    }
});
var phone = document.getElementById('numberonly'),
cleanPhoneNumber;

cleanPhoneNumber= function(e) {
e.preventDefault();
var pastedText = '';
if (window.clipboardData && window.clipboardData.getData) { // IE
pastedText = window.clipboardData.getData('Text');
} else if (e.clipboardData && e.clipboardData.getData) {
pastedText = e.clipboardData.getData('text/plain');
}
this.value = pastedText.replace(/\D/g, '');
};

phone.onpaste = cleanPhoneNumber;

