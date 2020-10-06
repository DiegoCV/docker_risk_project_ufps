from Risk_project_ufps.core_risk.dao.RecursoDao import *


class RecursoController:

	def registrar_recurso(self, proyecto, nombre, costo, tipo_recurso):
		recurso_dao = RecursoDao()
		return recurso_dao.registrar_recurso(proyecto, nombre, costo, tipo_recurso)
	
	def listar_recursos(self, id):
		recurso_dao = RecursoDao()
		return recurso_dao.listar_recursos(id)

	def listar_recursos_linea(self, id, linea_base):
		recurso_dao = RecursoDao()
		return recurso_dao.listar_recursos_linea(id, linea_base)

	def obtener_recurso(self, id):
		recurso_dao = RecursoDao()
		return recurso_dao.obtener_recurso(id)

	def eliminar_recurso(self, recurso):
		recurso_dao = RecursoDao()
		return recurso_dao.eliminar_recurso(recurso)

	def editar_recurso(self, recurso, nombre, costo):
		recurso_dao = RecursoDao()
		return recurso_dao.editar_recurso(recurso, nombre, costo)


















	