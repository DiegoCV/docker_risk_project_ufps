from Risk_project_ufps.core_risk.dao.ResponsableDao import *
from Risk_project_ufps.core_risk.dao.ProyectoHasRiesgoDao import *

from Risk_project_ufps.core_risk.dto.models import *

from django.forms.models import model_to_dict


class ResponsableController():

	def registrar_responsable(self, nombre, descripcion, proyecto, rol):
		responsable_dao = ResponsableDao()
		return responsable_dao.registrar_responsable(nombre, descripcion, proyecto, rol)

	def listar_responsables(self, id):
		responsable_dao = ResponsableDao()
		return responsable_dao.listar_responsables(id)

	def obtener_responsable(self, id):
		responsable_dao = ResponsableDao()
		return responsable_dao.obtener_responsable(id)

	def obtener_responsables_by_proyecto_group_for_riesgos(self, proyecto_id):
		responsable_dao = ResponsableDao()
		proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()
		proyecto = Proyecto(proyecto_id=proyecto_id)
		proyectos_has_riesgos = proyecto_has_riesgo_dao.listar_proyecto_has_riesgo_by_proyecto(proyecto)
		return proyectos_has_riesgos

	def raw_queryset_as_dictionary(self, raw_qs):
		aux = []
		for row in raw_qs:
			aux.append(model_to_dict(row))
		return aux

	def editar_responsable(self, responsable, nombre, descripcion, rol):
		responsable_dao = ResponsableDao()
		return responsable_dao.editar_responsable(responsable, nombre, descripcion, rol)

	def eliminar_responsable(self, responsable):
		responsable_dao = ResponsableDao()
		return responsable_dao.eliminar_responsable(responsable)

	def eliminar_responsable_riesgo(self, responsable_id, riesgo_id, proyecto_id):
		responsable_dao = ResponsableDao()
		responsable_dao.eliminar_responsable_riesgo(responsable_id, riesgo_id, proyecto_id)

	
