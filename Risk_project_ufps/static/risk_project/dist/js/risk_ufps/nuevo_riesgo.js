$(function() {

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

//////////////////////////////////////////////////////////////////////
    //Construye el combo de subcategorias
//////////////////////////////////////////////////////////////////////

  $.ajax({
  type: 'GET',
  url: BASE_URL_RISK + "sub_categoria/listar/",
  crossOrigin: true,
  headers: {
      "Authorization":"Bearer " + get_token_risk()
  },
  contentType: 'application/json',
  dataType: 'json',
  success: function (data, status, xhr) {
    construir_select_subcategoria(data);
  },
  error: function (jqXhr, textStatus, errorMessage) {
      $('#div_salvaje').append('Error' + errorMessage);
    }
  });

  //////////////////////////////////////////////////////////////////////
    //Registra una categoria para un gerente
  //////////////////////////////////////////////////////////////////////

    $('#form_registrar_categoria').on('submit', function(e) {
        e.preventDefault();
        let form_categoria = parsear_formulario($("#form_registrar_categoria :input").serializeArray());
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "categoria/",
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer " + get_token_risk()
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_categoria),
          success: function (data, status, xhr) {
            window.location ="../nuevoriesgo/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });
  });

  //////////////////////////////////////////////////////////////////////
    //Registra una subcategoria para un gerente
  //////////////////////////////////////////////////////////////////////

     $('#form_registrar_subcategoria').on('submit', function(e) {
        e.preventDefault();

        let form_subcategoria = parsear_formulario($("#form_registrar_subcategoria :input").serializeArray());
        console.log(form_subcategoria)
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "sub_categoria/",
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer " + get_token_risk()
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_subcategoria),
          success: function (data, status, xhr) {
            window.location ="../nuevoriesgo/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });
  });


  //////////////////////////////////////////////////////////////////////
    //Registra una riesgo para una categoria de un gerente
  //////////////////////////////////////////////////////////////////////

      $('#form_registrar_riesgo').on('submit', function(e) {
        e.preventDefault();
        let form_riesgo = parsear_formulario($("#form_registrar_riesgo :input").serializeArray());
        console.log(form_riesgo)
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "riesgo/",
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer " + get_token_risk()
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_riesgo),
          success: function (data, status, xhr) {
            window.location ="../nuevoriesgo/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });
      });


});


function caturarDatos_form_subcategoria() {
  return {
    "sub_categoria_nombre":$("#sub_categoria_nombre").val(),
    "sub_categoria_descripcion":$("#sub_categoria_descripcion").val(),
    "categoria_id":document.getElementById("categoria_id_form_sub_catg").value
  }
}

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



  //////////////////////////////////////////////////////////////////////
    //Construye el select de subcategorias
  //////////////////////////////////////////////////////////////////////

  function construir_select_subcategoria(subcategorias){
    var app5 = new Vue({
      delimiters: ['[[', ']]'],
      el: '#app-5',
      data: {
        subcategorias: subcategorias
      }
    });
  }

  
























//sdf
