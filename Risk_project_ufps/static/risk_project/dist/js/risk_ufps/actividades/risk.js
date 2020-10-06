////////////////////////////////////////////////////

/*
 *	Seccion de variables globales
 */
var my_json_mpp = {};
var my_json_gex = {};
////////////////////////////////////////////////////

/*
 * Manipula la variable global
 */
function setJsonMpp(data, actionurl) {
	my_json_mpp = data;	
	adaptarJson(my_json_mpp, function(my_json_ge) {
		//console.log(my_json_ge);
		$.ajax({
	        	url: actionurl,
	        	type: 'POST',
				headers: {'X-CSRFToken': csrftoken},
	          	data: $("#form_proyecto").serialize()+"&actividades=1&actividades_data="+JSON.stringify(my_json_ge),
				success: function(data) {
					Swal.fire(
		                '¡ Registro exitoso !',
		                'el proyecto se ha registrado',
		                'success'
	              	).then(function () {
	                	location.reload();
	              	});     				
				},error: function (jqXhr, textStatus, errorMessage) {
					console.log(errorMessage);
					Swal.fire({
		                icon: 'error',
		                title: 'Oops...',
		                text: '¡ No se pudo registrar el proyecto !',             
		              }).then(function () {
		                location.reload();
		              });
				}
      		});
	});
}


/*
 * Devuelve la variable global
 */
function getJsonMpp() {
	return my_json_mpp;
}

function adaptarJson(myJson, callback) {
	var jsonGanttEditor = {
		tasks : obtenerTasks(myJson)
	};
	callback(jsonGanttEditor);
}

function obtenerTasks(myJson){
	var myTasks = myJson.Project.Tasks.Task;
	var tasks = [];
	for(let i in myTasks){
		tasks.push({
			"uid":myTasks[i].UID,
			"id":myTasks[i].ID, 
			"name":myTasks[i].Name,
			"level":myTasks[i].OutlineLevel,
			"WBS": myTasks[i].WBS,
			"start":parsear_fecha(new Date(myTasks[i].Start)),
			"duration":calcularDiferencia(myTasks[i].Start, myTasks[i].Finish),
			"end":parsear_fecha(new Date(myTasks[i].Finish)),
			"uid_predecessor":predecessor(myTasks[i].PredecessorLink)
		});
	}
	return tasks;
}

function predecessor(predecesores) {
	aux = [];
	if(predecesores != undefined){
		if(Array.isArray(predecesores)){
			for(let i in predecesores){
				aux.push(predecesores[i].PredecessorUID)
			}
		}else{
			aux.push(predecesores.PredecessorUID)
		}
	}
	return aux;
}

function parsearFecha(fecha) {
	var exampleDate = new Date(fecha);
	return exampleDate.valueOf();
}

function parsear_fecha(now){    
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
    return today;
  }

function calcularDiferencia(fechaInicio, fechaFinal){
	var fFecha1 = new Date(fechaInicio);
	var fFecha2 = new Date(fechaFinal);
	var dif = fFecha2 - fFecha1;
	var dias = Math.floor(dif / (1000 * 60 * 60 * 24));
	return dias;
}



/*
function calcularDuracion(idTask, myJson){
	var calendarUID = myJson.Project.CalendarUID;
	var calendario = obtenerCalendario(calendarUID, myJson);
	var excepciones = calendario.Exceptions.Exception;
	for(let i in excepciones){
		var today = new Date(); if(today.getDay() == 6 || today.getDay() == 0) a
	}
}

function obtenerCalendario(uid, myJson){
	var calendarios = myJson.Project.Calendars.Calendar;
	for(let i in calendarios){
		if(calendarios[i].UID == uid){
			return calendarios[i];
		}
	}
	return {};
}
*/
