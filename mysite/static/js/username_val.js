
// function validateForm(){
//     var nameRegex = /^[a-zA-Z\-]+$/;
//     var validUsername = document.form.username.value.match(nameRegex);
//     if(validUsername == null){
//         alert("Your first name is not valid. Only characters A-Z, a-z and '-' are  acceptable.");
//         document.form.username.focus();
//         return false;
//     }
// }
//   var a = document.querySelector('#username');
//   function validation()
//   {
//   var a = document.form.name.value;
//   if(a=="")
//   {
//   alert("Please Enter Your Name");
//   document.form.name.focus();
//   return false;
//   }
//   }
// function validate() {
//     var name = /^[a-zA-Z\-]+$/;
//     var name = document.getElementById("username").value.match(nameRegex);
//     //do checking here however you like (regex, iteration, etc.)
//     if(validUsername == null){
//         alert("Your first name is not valid. Only characters A-Z, a-z and '-' are  acceptable.");
//         document.frm.firstName.focus();
//         return false;
//     }
// }
// const username = document.querySelector('#username');
// const form = document.querySelector('#signup');
// const checkUsername = () => {
//     let valid = false;
//     const min = 3,
//         max = 25;
//     const username = username.value.trim();
//     if (!isRequired(username)) {
//         showError(username, 'Please Enter the username.');
//     } else if (!isBetween(username.length, min, max)) {
//         showError(username, `Username must lie between ${min} and ${max} characters.`)
//     } else {
//         showSuccess(username);
//         valid = true;
//     }
//     return valid;
// }
function formValidation()
{
var uid = document.registration.username;

if(userid_validation(uid,5,12))
{
function userid_validation(uid,mx,my)
{
}
return false;
}

function userid_validation(uid,mx,my)
{
var uid_len = uid.value.length;
if (uid_len == 0 || uid_len>= my || uid_len<mx)
{
alert("User Id should not be empty / length be between "+mx+" to "+my);
uid.focus();
return false;
}
return true;
}
}