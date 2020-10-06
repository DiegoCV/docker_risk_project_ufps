 var form_aux = 0;
$(function() {

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
    //Edita una subcategoria para un gerente
  //////////////////////////////////////////////////////////////////////

     $('#form_editar_subcategoria').on('submit', function(e) {
        e.preventDefault();

        let form_subcategoria = parsear_formulario($("#form_editar_subcategoria :input").serializeArray());
        var aux = $("#sub_categoria_id").val();
        $.ajax({
          type: 'PUT',
          url: BASE_URL_RISK + "sub_categoria/actualizar/"+aux+"/",
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer " + get_token_risk()
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_subcategoria),
          success: function (data, status, xhr) {
            window.location ="../subcategorias/";
            console.log(form_subcategoria)
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });
  });

});

  //////////////////////////////////////////////////////////////////////
    //Construye el select de subcategorias
  //////////////////////////////////////////////////////////////////////

  function construir_select_subcategoria(subcategorias){
    var app5 = new Vue({
      delimiters: ['[[', ']]'],
      el: '#app-5',
      data: {
        subcategorias: subcategorias
      },
      methods:{
          abrir_modal_editar:function(argument) {
              abrir_modal_editar(argument);
          },
          abrir_modal_eliminar:function(subcategoria) {
              abrir_modal_eliminar(subcategoria)
          }
        }
    });
  }

  function eliminar_subcategoria(subcategoria_id){

    $.ajax({
      type: 'DELETE',
      url: BASE_URL_RISK + "sub_categoria/eliminar/"+subcategoria_id+"/",
      crossOrigin: true,
      headers: {
        "Authorization":"Bearer " + get_token_risk()
      },
      contentType: 'application/json',
      dataType: 'json',
      success: function (data, status, xhr) {
        window.location ="../subcategorias/";
      },
      error: function (jqXhr, textStatus, errorMessage) {
        $('#div_salvaje').append('Error' + errorMessage);
      }
    });


  }
