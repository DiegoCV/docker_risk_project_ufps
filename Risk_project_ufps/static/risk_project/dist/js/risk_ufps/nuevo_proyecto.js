$(function() {
  //////////////////////////////////////////////////////////////////////
    //Registrar un proyecto para un gerente
  //////////////////////////////////////////////////////////////////////
      $('#form_registrar_proyecto').on('submit', function(e) {
        e.preventDefault();

        let form_proyecto = parsear_formulario($("#form_registrar_proyecto :input").serializeArray());
        console.log(form_proyecto)
        $.ajax({
          type: 'POST',
          url: BASE_URL_RISK + "proyecto/",
          crossOrigin: true,
          headers: {
              "Authorization":"Bearer " + get_token_risk()
          },
          contentType: 'application/json',
          dataType: 'json',
          data: JSON.stringify(form_proyecto),
          success: function (data, status, xhr) {
            window.location ="../nuevoproyecto/";
          },
          error: function (jqXhr, textStatus, errorMessage) {
              console.log('Error' + errorMessage);
              alert("Ha ocurrido un error");
          }
        });
  });

 
});