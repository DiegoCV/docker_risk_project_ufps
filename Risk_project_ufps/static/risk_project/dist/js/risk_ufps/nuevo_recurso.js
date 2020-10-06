$(function() {

  //////////////////////////////////////////////////////////////////////
    //Construye el combo de tipos de recursos
  //////////////////////////////////////////////////////////////////////
  $.ajax({
    type: 'GET',
    url: BASE_URL_RISK + "tipo_recurso/listar/",
    crossOrigin: true,
    headers: {
        "Authorization":"Bearer " + get_token_risk()
    },
    contentType: 'application/json',
    dataType: 'json',
    success: function (data, status, xhr) {
      construir_select_tipo_recurso(data);
    },
    error: function (jqXhr, textStatus, errorMessage) {
        $('#div_salvaje').append('Error' + errorMessage);
    }
  });

  //////////////////////////////////////////////////////////////////////
    //Registra un tipo de recurso para un gerente
  //////////////////////////////////////////////////////////////////////

     $('#form_registrar_tipo_recurso').on('submit', function(e) {
        e.preventDefault();

        let form_tipo_recurso = parsear_formulario($("#form_registrar_tipo_recurso :input").serializeArray());
        console.log(form_tipo_recurso)
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "tipo_recurso/",
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer " + get_token_risk()
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_tipo_recurso),
          success: function (data, status, xhr) {
            window.location ="../nuevorecurso/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });
  });


  //////////////////////////////////////////////////////////////////////
    //Registra un recurso asociado a un tipo de recurso para un gerente
  //////////////////////////////////////////////////////////////////////

      $('#form_registrar_recurso').on('submit', function(e) {
        e.preventDefault();
        let form_recurso = parsear_formulario($("#form_registrar_recurso :input").serializeArray());
        console.log(form_recurso)
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "recurso/",
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer " + get_token_risk()
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_recurso),
          success: function (data, status, xhr) {
            window.location ="../nuevorecurso/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });
      });


});




//////////////////////////////////////////////////////////////////////
  //Construye el select de tipos de recursos
//////////////////////////////////////////////////////////////////////

function construir_select_tipo_recurso(tipos_recursos){
var app6 = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app-6',
  data: {
    tipos_recursos: tipos_recursos
  }
});
}



  