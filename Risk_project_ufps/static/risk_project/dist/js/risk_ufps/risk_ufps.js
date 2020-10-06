//////////////////////////////////////////////////////////////////////
  //Variables globales risk_ufps
//////////////////////////////////////////////////////////////////////
var BASE_URL_RISK = "http://localhost:8000/api_v1/";

$(function() {
  //////////////////////////////////////////////////////////////////////
    //Capturar el evento del formulario para iniciar la sesion
  //////////////////////////////////////////////////////////////////////

    $('#form_login').on('submit', function(e) {
        e.preventDefault();
        let form_login = parsear_formulario($("#form_login :input").serializeArray());
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "gerente/login/",
          crossOrigin: true,
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_login),
          success: function (data, status, xhr) {
            set_token_risk(data.access);
            
            window.location ="../inicio/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });

    });

  //////////////////////////////////////////////////////////////////////
     //Registra un nuevo gerente
  //////////////////////////////////////////////////////////////////////

        $('#form_registrar_gerente').on('submit', function(e) {
        e.preventDefault();
        let form_gerente = parsear_formulario($("#form_registrar_gerente :input").serializeArray());
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "gerente/",
          crossOrigin: true,
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_gerente),
          success: function (data, status, xhr) {
            set_token_risk(data.access);
            
            window.location ="../index/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });

    });
});

//////////////////////////////////////////////////////////////////////
  //Parsea un formulario al formato del Json
//////////////////////////////////////////////////////////////////////

function parsear_formulario(form){
  let form_parse = {};
  for(let i in form){
    form_parse[form[i].name] = form[i].value;
  }
  return form_parse;
}


//////////////////////////////////////////////////////////////////////
  //Funciones para almacenar y recuperar informacion del local storage
//////////////////////////////////////////////////////////////////////

function set_token_risk(token_risk) {
  localStorage.setItem("token_risk", token_risk);
}

function get_token_risk() {
  if(localStorage.getItem("token_risk")){
    return localStorage.getItem("token_risk");
  }else{
    console.log("token no encontrado");
  }
}
