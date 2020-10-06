from Risk_project_ufps.core_risk.dao.SubcategoriaDao import *


class SubcategoriaController:


	def listar_subcategorias(self, id):
		"""
		Lista las subcategorias de un gerente
		:param id:
		:return:
		"""
		subcategoria_dao = SubcategoriaDao()
		return subcategoria_dao.listar_subcategorias(id)

	def obtener_subcategoria(self, id):
		"""
		Retorna una subcategoria a partir de un id
		:param id:
		:return:
		"""
		subcategoria_dao = SubcategoriaDao()
		return subcategoria_dao.obtener_subcategoria(id)



