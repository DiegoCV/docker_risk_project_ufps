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




});

function construir_select_tipo_recurso(tipos_recursos){
var app6 = new Vue({
  delimiters: ['[[', ']]'],
  el: '#app-6',
  data: {
    tipos_recursos: tipos_recursos
  }
});
}

//////////////////////////////////////////////////////////////////////
  //Construye los riesgos por sub_categoria
//////////////////////////////////////////////////////////////////////


function construir_recursos(tipo_recurso){
document.getElementById('content_tabla_recursos').innerHTML="";
console.log(tipo_recurso.value);
$( "#content_tabla_recursos" ).load( "/nuevorecurso/tabla_recursos/", function() {
 $.ajax({
    type: 'GET',
    url: BASE_URL_RISK + "..."+tipo_recurso.value+"/",
    crossOrigin: true,
    headers: {
        "Authorization":"Bearer " + get_token_risk()
    },
    contentType: 'application/json',
    dataType: 'json',
    success: function (data, status, xhr) {
      if(data.length > 0){
        new Vue({
              delimiters: ['[[', ']]'],
              el: '#plantilla_tabla_recursos',
              data: {
                recursos:data
              }
          });
      }else{
        new Vue({
              delimiters: ['[[', ']]'],
              el: '#plantilla_tabla_recursos',
              data: {
                recursos:[{
        "recurso_nombre": "No hay recursos asociados a este tipo de recurso",
        "recurso_costo": "",
        "tipo_recurso_nombre": ""}]
              }
          });
      }
    },
    error: function (jqXhr, textStatus, errorMessage) {
        $('#div_salvaje').append('Error' + errorMessage);
    }
  });
});
}