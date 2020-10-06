$(document).ready(function(){
  //////////////////////////////////////////////////////////////////////
    //Construye el combo de categorias
  //////////////////////////////////////////////////////////////////////
  $.ajax({
    type: 'GET',
    url: BASE_URL_RISK + "categoria/listar/",
    crossOrigin: true,
    headers: {
        "Authorization":"Bearer " + get_token_risk()
    },
    contentType: 'application/json',
    dataType: 'json',
    success: function (data, status, xhr) {
      construir_select_categoria(data);
    },
    error: function (jqXhr, textStatus, errorMessage) {
        $('#div_salvaje').append('Error' + errorMessage);
    }
  });
});


  //////////////////////////////////////////////////////////////////////
    //Construye el select de categorias
  //////////////////////////////////////////////////////////////////////

function construir_select_categoria(categorias){
  var app4 = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app-4',
    data: {
      categorias: categorias
    }
  });
}
