$(function() { //shorthand document.ready function
    /*$('#form_registrar_categoria').on('submit', function(e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var categoria = parsear_formulario();
        $.ajax({
          type: 'POST',
          url: '/registrarcategoria/',
          headers: {
              "csrfmiddlewaretoken":"s1CeXA4H139tsM6cfAc3gQi0VJDfKt729hjrs1LCCJAIVNKJrW0NJmN8UULQWIJd"
          },
          contentType: 'application/json',
          dataType: 'html',
          data: JSON.stringify(categoria),  // data to submit
          success: function (data, status, xhr) {
              $('#div_salvaje').append('status: ' + status + ', data: ' + data);
          },
          error: function (jqXhr, textStatus, errorMessage) {
              $('#div_salvaje').append('Error' + errorMessage);
          }
        });
    });*/
    $('#form_registrar_categoria').on('submit', function(e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var categoria = parsear_formulario();
        $.ajax({
          type: 'POST',
          url: 'http://localhost:8000/api_v1/categoria/',
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk2MDM5NjM3LCJqdGkiOiIyZGMyNjYwM2NlYWQ0YjI3YTAzZDM3ZGJhMzVkNzQ3NSIsInVzZXJfaWQiOjc5LCJ1c2VybmFtZSI6ImRpZWdvY3ZfMzYiLCJnZXJlbnRlX2lkIjo3OX0.xlbBKOdBZ9fVb7zKFU2lX_HauBLTpv0h2KC_VifcwqQ"
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(categoria),  // data to submit
          success: function (data, status, xhr) {
            //  $('#div_salvaje').append('status: ' + status + ', data: ' + data);
              //$("#form_registrar_categoria")[0].reset();
            location.reload();
          },
          error: function (jqXhr, textStatus, errorMessage) {
              $('#div_salvaje').append('Error' + errorMessage);
          }
        });

    });
});

function parsear_formulario(){
  var form_categoria = $("#form_registrar_categoria :input").serializeArray();
  console.log(form_categoria);
  return{
    categoria_nombre : form_categoria[1].value,
    categoria_descripcion : form_categoria[2].value
  }
}

//////////////////////////////////////////////////////////////////////
  //Funciones para almacenar y recuperar informacion del local storage
//////////////////////////////////////////////////////////////////////

function set_token_risk(token_risk) {
  localStorage.setItem("token_risk":token_risk);
}

function get_token_risk() {
  if(localStorage.getItem("token_risk")){
    return localStorage.getItem("token_risk");
  }else{
    console.log("token no encontrado");
  }
}