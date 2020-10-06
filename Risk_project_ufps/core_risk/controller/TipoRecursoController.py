from Risk_project_ufps.core_risk.dao.TipoRecursoDao import *


class TipoRecursoController():


	def registrar_tipo_recurso(self, nombre, descripcion, gerente):
		tipo_recurso_dao = TipoRecursoDao()
		return tipo_recurso_dao.registrar_tipo_recurso(nombre, descripcion, gerente)

	def listar_tipos_recursos(self, id):
		tipo_recurso_dao = TipoRecursoDao()
		return tipo_recurso_dao.listar_tipos_recursos(id)

	def obtener_tipo_recurso(self, id):
		tipo_recurso_dao = TipoRecursoDao()
		return tipo_recurso_dao.obtener_tipo_recurso(id)

	def eliminar_tipo_recurso(self, tipo_recurso):
		tipo_recurso_dao = TipoRecursoDao()
		return tipo_recurso_dao.eliminar_tipo_recurso(tipo_recurso)

	def editar_tipo_recurso(self, tipo_recurso, nombre, descripcion):
		tipo_recurso_dao = TipoRecursoDao()
		return tipo_recurso_dao.editar_tipo_recurso(tipo_recurso, nombre, descripcion)

