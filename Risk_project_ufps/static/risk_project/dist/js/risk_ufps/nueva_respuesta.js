var SUBCATEGORIAS_RISK = [];

$(document).ready(function(){
  //////////////////////////////////////////////////////////////////////
    //Construye el combo de categorias
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
      SUBCATEGORIAS_RISK = data;
      let sub_categorias = data.reduce(( sub_categoria_list, aux ) => {
        sub_categoria_list.push(aux["sub_categoria"]);

        return sub_categoria_list;

      }, []);
      console.log(sub_categorias)
      let aux_sub_categoria = { "sub_categorias":SUBCATEGORIAS_RISK };
      construir_select(aux_sub_categoria, "bloq_subcategorias");

    },
    error: function (jqXhr, textStatus, errorMessage) {
        console.log('Error' + errorMessage);
    }
  });
});

//////////////////////////////////////////////////////////////////////
  //Captura la accion del combo categoria para pintar las subcategorias
//////////////////////////////////////////////////////////////////////

function cargar_riesgos(categoria){
  let riesgos = SUBCATEGORIAS_RISK.filter((aux) => +aux["sub_categoria"]["sub_categoria_id"] == +sub_categoria.value)[0]["sub_categorias"];
  construir_select_riesgos(sub_categorias);
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
   e = document.getElementById('sub_categorias_id');
   let sub_categorias = SUBCATEGORIAS_RISK.filter((aux) => +aux["sub_categoria"]["sub_categoria_id"] == +e.options[e.selectedIndex].value)[0]["sub_categorias"];
   construir_select_riesgos(sub_categorias);
}

function construir_select_riesgos(datos){
  let select_aux = document.getElementById('riesgo_id');
  select_aux.innerHTML = '';
  datos.forEach((item, i) => {
    var x = document.createElement("OPTION");
    x.setAttribute("value", item.riesgo_id);
    var t = document.createTextNode(item.riesgo_nombre);
    x.appendChild(t);
    select_aux.appendChild(x);
  });

}

