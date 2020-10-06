//////////////////////////////////////////////////////////////////////
  //Variables globales para la vista mis_riesgos.html
//////////////////////////////////////////////////////////////////////
var CATEGORIAS_RISK = [];

$(document).ready(function(){
  //////////////////////////////////////////////////////////////////////
    //Construye el combo de categorias
  //////////////////////////////////////////////////////////////////////
  $.ajax({
    type: 'GET',
    url: BASE_URL_RISK + "categoria/listar/all/",
    crossOrigin: true,
    headers: {
        "Authorization":"Bearer " + get_token_risk()
    },
    contentType: 'application/json',
    dataType: 'json',
    success: function (data, status, xhr) {
      CATEGORIAS_RISK = data;
      let categorias = data.reduce(( categoria_list, aux ) => {
        categoria_list.push(aux["categoria"]);
        return categoria_list;
      }, []);
      let aux_categoria = { categorias:categorias };
      construir_select(aux_categoria, "riesgos_bloq_categorias");

    },
    error: function (jqXhr, textStatus, errorMessage) {
        $('#div_salvaje').append('Error' + errorMessage);
    }
  });
});

//////////////////////////////////////////////////////////////////////
  //Captura la accion del combo categoria para pintar las subcategorias
//////////////////////////////////////////////////////////////////////

function cargar_subCategorias(categoria){
  let sub_categorias = CATEGORIAS_RISK.filter((aux) => +aux["categoria"]["categoria_id"] == +categoria.value)[0]["sub_categorias"];
  construir_select_subcategorias(sub_categorias);
}

//////////////////////////////////////////////////////////////////////
  //Construye la estructura de los selects
//////////////////////////////////////////////////////////////////////

function construir_select(datos, id_bloq){
  new Vue({
      delimiters: ['[[', ']]'],
      el: '#'+id_bloq,
      data: datos
  });
   e = document.getElementById('riesgos_categoria_id');
   let categorias = CATEGORIAS_RISK.filter((aux) => +aux["categoria"]["categoria_id"] == +e.options[e.selectedIndex].value)[0]["sub_categorias"];
   construir_select_subcategorias(categorias);
}

function construir_select_subcategorias(datos){
  let select_aux = document.getElementById('riegos_sub_categoria_id');
  select_aux.innerHTML = '';
  datos.forEach((item, i) => {
    var x = document.createElement("OPTION");
    x.setAttribute("value", item.sub_categoria_id);
    var t = document.createTextNode(item.sub_categoria_nombre);
    x.appendChild(t);
    select_aux.appendChild(x);
  });

}

//////////////////////////////////////////////////////////////////////
  //Construye los riesgos por sub_categoria
//////////////////////////////////////////////////////////////////////


function construir_riesgos(sub_categoria){
document.getElementById('content_tabla_riesgos').innerHTML="";
console.log(sub_categoria.value);
$( "#content_tabla_riesgos" ).load( "/riesgos/plantilla_tabla_riesgo/", function() {
 $.ajax({
    type: 'GET',
    url: BASE_URL_RISK + "riesgo/listar/sub_categoria/"+sub_categoria.value+"/",
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
              el: '#plantilla_tabla_riesgos',
              data: {
                riesgos:data
              }
          });
      }else{
        new Vue({
              delimiters: ['[[', ']]'],
              el: '#plantilla_tabla_riesgos',
              data: {
                riesgos:[{
        "riesgo_nombre": "No hay riesgos asociados a esta subcategoria",
        "riesgo_causa": "",
        "riesgo_evento": "",
        "riesgo_efecto": "",
        "riesgo_prom_evaluacion": ""}]
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
















