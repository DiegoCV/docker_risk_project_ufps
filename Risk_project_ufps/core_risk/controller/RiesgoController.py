from Risk_project_ufps.core_risk.dao.RiesgoDao import *
from Risk_project_ufps.core_risk.dao.CategoriaDao import *
from Risk_project_ufps.core_risk.dao.SubcategoriaDao import *
from Risk_project_ufps.core_risk.dao.ProyectoDao import *
from Risk_project_ufps.core_risk.dao.ProyectoHasRiesgoDao import *
from Risk_project_ufps.core_risk.dao.RbsDao import *
from Risk_project_ufps.core_risk.controller.RbsController import *

from Risk_project_ufps.core_risk.dto.models import *

from django.forms.models import model_to_dict


class RiesgoController():

	def registrar_riesgo(self, nombre, causa, evento, efecto, tipo, subcategoria):
		riesgo_dao = RiesgoDao()
		return riesgo_dao.registrar_riesgo(nombre, causa, evento, efecto, tipo, subcategoria)

	def listar_riesgos(self, id):
		riesgo_dao = RiesgoDao()
		return riesgo_dao.listar_riesgos(id)

	def editar_riesgo(self, riesgo, nombre, causa, evento, efecto, tipo, subcategoria):
		riesgo_dao = RiesgoDao()
		return riesgo_dao.editar_riesgo(riesgo, nombre, causa, evento, efecto, tipo, subcategoria)

	def obtener_riesgo(self, id):
		riesgo_dao = RiesgoDao()
		return riesgo_dao.obtener_riesgo(id)

	def eliminar_riesgo(self, riesgo):
		riesgo_dao = RiesgoDao()
		return riesgo_dao.eliminar_riesgo(riesgo)

	def registrar_riesgo_proyecto(self, nombre, causa, evento, efecto, tipo, subcategoria_id, proyecto_id):
		riesgo_dao = RiesgoDao()
		subcategoria_dao = SubcategoriaDao()
		proyecto_dao = ProyectoDao()
		return riesgo_dao.registrar_riesgo_proyecto(
			nombre,
			causa,
			evento,
			efecto,
			tipo,
			subcategoria_dao.obtener_subcategoria(subcategoria_id),
			proyecto_dao.obtener_proyecto(proyecto_id),
		)

	def asosiar_riesgos_proyecto(self, riesgos, proyecto):
		p_h_r = ProyectoHasRiesgoDao()
		for riesgo in riesgos:
			p_h_r.registrar_proyecto_riesgo(proyecto, Riesgo(riesgo_id=riesgo))
		return True

	def asosiar_riesgos_sugeridos_proyecto(self, riesgos, proyecto):
		p_h_r = ProyectoHasRiesgoDao()

		riesgo_dao = RiesgoDao()

		subcategoria_dao = SubcategoriaDao()

		categoria_dao = CategoriaDao()

		rbs_dao = RbsDao()
		rbs_controller = RbsController()
		rbs = rbs_controller.obtener_rbs_general(proyecto.gerente.gerente_id)
		rbs_model = rbs_dao.get_rbs_gerente_id(proyecto.gerente)

		for riesgo in riesgos:
			aux = riesgo_dao.obtener_riesgo(riesgo)
			sub_categoria_aux = aux.sub_categoria
			try:
				sub_aux = self.buscar_sub_categoria_by_uid(rbs, sub_categoria_aux)
				if sub_aux:
					riesgo_nuevo = riesgo_dao.registrar_riesgo(
						aux.riesgo_nombre,
						"Sin Causa definida",
						"Sin Evento definido",
						"Sin efecto definido", 0, 0, sub_aux)
				else:
					print("EEEEEEEEEEEE", sub_categoria_aux.categoria, rbs_model)
					print("CATENOMBRE", sub_categoria_aux.categoria.categoria_nombre)
					categoria_aux = categoria_dao.duplicar_categoria_2(sub_categoria_aux.categoria, rbs_model)
					print("CCCC", categoria_aux)
					sub_categoria_aux = subcategoria_dao.duplicar_sub_categoria_2(categoria_aux, sub_categoria_aux)
					print("SSSSSSS", sub_categoria_aux)
					rbs = rbs_controller.obtener_rbs_general(proyecto.gerente.gerente_id)
					print("RBSSSSS", rbs)
					riesgo_nuevo = riesgo_dao.clonar_riesgo(aux.riesgo_nombre, aux.riesgo_uid, sub_categoria_aux)
					print("RRRRRRRR", riesgo_nuevo)
				p_h_r.registrar_proyecto_riesgo_editado(proyecto, riesgo_nuevo)
			except Exception as e:
				raise e
			finally:
				pass

		return True

	def buscar_sub_categoria_by_uid(self, rbs, sub_categoria):
		for fila in rbs:
			subcategorias = fila['subcategorias']
			for aux in subcategorias:
				if aux['sub_categoria_uid'] == sub_categoria.sub_categoria_uid:
					return aux['sub_categoria_uid']
		return None

	def get_riesgo_by_proyecto(self, proyecto, riesgo):
		p_h_r = ProyectoHasRiesgoDao()
		return p_h_r.get_by_riesgo_and_proyecto(proyecto, riesgo)



	def get_riesgos_by_proyecto(self, proyecto):
		"""Devuelve todos los riesgos que esten asociados a un riesgo,
		devuleve como un objeto raw query
		"""
		riesgo_dao = RiesgoDao()
		riesgos = riesgo_dao.get_riesgos_by_proyecto(proyecto)
		aa = []
		for riesgo in riesgos:
			riesgo_aux = model_to_dict(riesgo)
			#print("RRRRR", riesgo_aux)
			#riesgo_aux['fecha_manifestacion'] = riesgo.fecha_manifestacion.strftime("%Y-%m-%d")
			aa.append(riesgo_aux)
			#riesgo['fecha_manifestacion'] = riesgo['fecha_manifestacion'].strftime("%Y-%m-%d")
		return aa


	def get_riesgos_by_proyecto_linea(self, proyecto, linea_base):        
		riesgo_dao = RiesgoDao()
		return riesgo_dao.get_riesgos_by_proyecto_linea(proyecto, linea_base)


	def get_riesgos_by_proyecto_2(self, proyecto):
		"""Devuelve todos los riesgos que esten asociados a un proyecto,
		como un array de diccionarios
		"""
		riesgo_dao = RiesgoDao()
		riesgos = riesgo_dao.get_riesgos_by_proyecto(proyecto)
		return self.raw_queryset_of_riesgos_as_values_list(riesgos)

	def eliminar_riesgo_by_proyecto(self, riesgo_proyecto):
		p_h_r = ProyectoHasRiesgoDao()
		return p_h_r.eliminar_by_riesgo_and_proyecto(riesgo_proyecto)

	def agregar_responsable_riesgo(self, riesgo_proyecto, responsable):
		p_h_r = ProyectoHasRiesgoDao()
		return p_h_r.agregar_responsable_riesgo(riesgo_proyecto, responsable)

	def listar_responsables_riesgo(self, proyecto_id):
		p_h_r = ProyectoHasRiesgoDao()
		responsables = p_h_r.listar_responsables_riesgo(proyecto_id)
		aux = []
		for responsable in responsables:
			aa = model_to_dict(responsable)
			aa['riesgo_id'] = responsable.riesgo_id
			aux.append(aa)
		return aux


	def get_riesgos_sugeridos(self, sector, gerente_id):
		""" Busca todos los riesgos dentro de todos los proyectos
		de un sector especifico, excluyendo a los riesgos propios del gerente"""

		riesgo_dao = RiesgoDao()
		gerente = Gerente(gerente_id=gerente_id)

		r = riesgo_dao.listar_riesgos(gerente_id)

		riesgos_propios = self.raw_queryset_as_dictionary(r)

		riesgos_sugeridos = riesgo_dao.get_riesgos_by_sector_distinct_gerente(sector, gerente)

		riesgos_sugeridos_aux = []

		for aux in riesgos_sugeridos:
			key = riesgos_propios.get(aux.riesgo_nombre)
			if (key == None):
				riesgos_sugeridos_aux.append(aux)

		return riesgos_sugeridos_aux

	def raw_queryset_as_dictionary(self, raw_qs):
		aux = {}
		for row in raw_qs:
			aux[row.riesgo_nombre] = row
		return aux

	def editar_riesgo_proyecto(self, proyecto_id, riesgo_id, nombre, causa, evento, efecto, tipo ):

		riesgo_dao = RiesgoDao()
		proyecto_dao = ProyectoDao()
		proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()

		riesgo = riesgo_dao.obtener_riesgo(riesgo_id)
		proyecto = proyecto_dao.obtener_proyecto(proyecto_id)
		#print("VARIABLES", riesgo, proyecto)
		proyecto_has_riesgo = proyecto_has_riesgo_dao.get_by_riesgo_and_proyecto_2(riesgo, proyecto)
		#print("MI OBJETO", proyecto_has_riesgo)
		if proyecto_has_riesgo.is_editado == 1:
			#proyecto_has_riesgo_dao.actualizar_fecha(proyecto_has_riesgo, fecha)
			return riesgo_dao.editar_riesgo(riesgo, nombre, causa, evento, efecto, tipo, riesgo.sub_categoria)
		else:
			proyecto_has_riesgo.delete()
			riesgo_nuevo = riesgo_dao.registrar_riesgo_2(nombre, causa, evento, efecto, tipo, riesgo.sub_categoria)
			proyecto_has_riesgo_dao.registrar_proyecto_riesgo_editado(proyecto, riesgo_nuevo)
			return riesgo_nuevo

	def raw_queryset_of_riesgos_as_values_list(self, raw_qs):
		aux = []
		for row in raw_qs:
			aa = model_to_dict(row)
			aa["impacto_id"] = row.impacto_id
			aa["propabilidad_id"] = row.propabilidad_id
			aux.append(aa)
		return aux

	def evaluar_riesgos_by_proyecto_id(self, riesgos, proyecto_id):
		"""
		Este metodo asume que llegan los riesgos del proyecto_id y el objetivo es buscar los
		valores de impacto y probabilidad y evaluarlos.
		:param riesgos:
		:param proyecto_id:
		:return:
		"""
		proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()
		proyecto = Proyecto(proyecto_id=proyecto_id)
		aux = {}
		for riesgo in riesgos:
			#print("SUPER IMPRESIONS", riesgo)
			aa = Riesgo(riesgo_id=riesgo.get('riesgo_id'))
			proyecto_has_riesgo = proyecto_has_riesgo_dao.get_by_riesgo_and_proyecto_2(aa, proyecto)
			aux['riesgo_' + str(aa.riesgo_id)] = dict(
				impacto_id=proyecto_has_riesgo.impacto_id,
				propabilidad_id=proyecto_has_riesgo.propabilidad_id,
				#fecha_manifestacion=riesgo['fecha_manifestacion']
			)
		return aux


	def evaluar_riesgos_by_proyecto_id_linea(self, riesgos, proyecto_id, linea_base):
		"""
		Este metodo asume que llegan los riesgos del proyecto_id y el objetivo es buscar los
		valores de impacto y probabilidad y evaluarlos.
		:param riesgos:
		:param proyecto_id:
		:return:
		"""
		proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()
		proyecto = Proyecto.objects.using('base').get(proyecto_id=proyecto_id, proyecto_linea_base=linea_base)
		aux = {}
		for riesgo in riesgos:
			proyecto_has_riesgo = proyecto_has_riesgo_dao.get_by_riesgo_and_proyecto_2_linea(riesgo, proyecto, linea_base)
			aux['riesgo_' + str(riesgo.riesgo_id)] = dict(
				impacto_id=proyecto_has_riesgo.impacto_id,
				propabilidad_id=proyecto_has_riesgo.propabilidad_id
			)
		return aux
