$(function() {
  //////////////////////////////////////////////////////////////////////
    //Lista todos los proyectos de un gerente
  //////////////////////////////////////////////////////////////////////
  $.ajax({
    type: 'GET',
    url: BASE_URL_RISK + "proyecto/listar/",
    crossOrigin: true,
    headers: {
        "Authorization":"Bearer " + get_token_risk()
    },
    contentType: 'application/json',
    dataType: 'json',
    success: function (data, status, xhr) {
      console.log(data);
      construir_proyectos(data);
    },
    error: function (jqXhr, textStatus, errorMessage) {
        $('#div_salvaje').append('Error' + errorMessage);
    }
  });
});



  //////////////////////////////////////////////////////////////////////
    //Crear el json de proyectos de un gerente
  //////////////////////////////////////////////////////////////////////
function construir_proyectos(proyectos){
  var app1 = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app-1',
    data: {
      proyectos: proyectos
    }
  });
}

