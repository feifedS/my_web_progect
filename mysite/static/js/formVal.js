// var response = false;
// $.validator.addMethod(
//     "uniqueUserName", 
//     function(value, element) {
//         $.ajax({
//             type: "GET",
//             url: "http://localhost:8000/main/checkusername",
//             data: "checkUsername=" + value,
//             dataType: "html",
//             success: function(msg)
//             {
//                 debugger
//                 //If username exists, set response to true
//                 response = ( msg == 'true' ) ? true : false;
//             }
//         });
//         return response;
//     },
//     "Username is Already Taken"
// );
$.validator.addMethod(
    "regex",
    function(value, element, regexp) {
      var re = new RegExp(regexp);
      return this.optional(element) || re.test(value);
    },
    "Please check your input."
);
$("#registration").validate({
    errorPlacement: function(error, element) {
        error.insertBefore(element);
    },


    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      first_name:{
        required: true,
        regex: "^[a-zA-Z'.\\s]{1,40}$"
      },
      lastname: "required",
      email: {
        required: true,
        // Specify that email should be validated
        // by the built-in "email" rule
        email: true
      },
      password: {
        required: true,
        minlength: 5
      }
    },
    // Specify validation error messages
    messages: {
        first_name: {
            required: "Please enter your firstname",
            minlength: "минимум должно быть 3",
            maxlength: "максимум должно быть 32",
        },
        lastname: "Please enter your lastname",
        password: {
            required: "Please provide a password",
            minlength: "Your password must be at least 5 characters long"
        },
        email: "Please enter a valid email address"
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
      form.submit();
    }
  });