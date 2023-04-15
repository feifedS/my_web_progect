$(document).ready( function () {
   

    $("#id_category").append(`
    <option value="" disabled selected >Выберите категорию</option>    `)
    var selected_barber_id = 0;
    $("#id_service").html('');
    
    $("#id_service").append(`
        <option value="">Выберите услугу</option>
    `)
    $("#id_category").change(function (event) {
        var cat_from_form = event.target.value;
        $.ajax({
            url: `/main/api/models?category=${cat_from_form}`,
            type: 'get',
            success: function (data){
                $("#id_service").html('');
                $("#id_barber").html('');
                $("#id_barber").append(`
                        <option value="" disabled selected >Выберите мастера</option>
                    `)
                $("#id_service").append(`
                        <option value="" id="XAXAXA" disabled selected>Выберите услугу</option>
                        
                    `)
                data.forEach(element => {
                    $("#id_service").append(`
                        <option value="${element.id}">${element.name}</option>
                    `);
                    });
                
                }
            });
    });

    $("#id_barber").html('');
    
    $("#id_barber").append(`
        <option value="">Выберите мастера</option>
    `);
    $("#id_service").change(function (event) {
        var ser_from_form = event.target.value;
        
        $.ajax({
            url: `/main/api/barbers?service=${ser_from_form}`,
            type: 'get',
            success: function (data){
                $("#id_barber").html('');
                $("#XAXAXA").replaceWith(`<option value="" disabled>Выберите мастера</option>`);
                $("#id_barber").append(`<option value="" disabled selected>Выберите услугу</option>`);
                $("#XAXAXA").replaceWith('<option value="" disabled>Выберите услугу</option>');
                data.forEach(element => {
                    $("#id_barber").append(`
                        <option value="${element.user}">${element.name}</option>
                    `);
                    })
                }
            }
        );
    });
    $("#id_date").change(function (event) {
        var date = event.target.value;
        $.ajax({
            url: `/main/api/aviable_times?barber=${date}`,
            success: function (data){
                $('available_times').show();
                var currentTime = new Date();
                $("#available_times").html("");
                data.forEach(function(time){
                    var timeValue = new Date(time.time);
                    if (timeValue > currentTime) {
                        $("#available_times").append(`
                            <option value="${time.time}">${time.time}</option>
                        `);
                    }
                });
            },
            error: function(error){
                $("#available_times").html("");
                $("#available_times").append(`
                    <option value="" disabled selected>Извините,у этоге мастера на эту дату свободного времени записи не найдено.</option>
                `);
            }
        });
    });
    // функция возвращающая список всех доступных времен по дате
    // $("#id_barber").change(function (event) {
    //     var $option = $(this).find('option:selected');
    //     // selected_barber_id = $option.val();
    //     var ser_from_form = event.target.value;
       
    //     $.ajax({
    //         url: `/main/api/aviable_times?barber=${date}`,
    //         // type:'get',
            
    //         success: function (data){
    //             $('available_times').show();
    //     }});
    //     // debugger
    // });

    // $("#id_date").change(function (event) {
    //     var date = event.target.value;
    //     $.ajax({
    //         url: `/main/api/aviable_times?barber=${date}`,
    //         // type:'get',
            
    //         success: function (data){
    //             $('available_times').show();
    //     }});
        
    // });
});

function validateForm() {
    const service = document.getElementById("id_service").value;
    const barber = document.getElementById("id_barber").value;
    const date = document.getElementById("id_date").value;

    if (service === "" || barber === "" || date === "") {
        const errorMessage = "Пожалуйста, заполните все поля.";
    const errorElement = document.getElementById("error-message");
    errorElement.innerHTML = `<div class="alert alert-danger" role="alert">${errorMessage}</div>`;
    return false;
    }
    return true;
  }
