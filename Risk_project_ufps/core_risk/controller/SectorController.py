from Risk_project_ufps.core_risk.dao.SectorDao import *


class SectorController:

	def listar_sectores(self):
		sector_dao = SectorDao()
		return sector_dao.listar_sectores()
		
	def obtener_sector(self, id):
		sector_dao = SectorDao()
		return sector_dao.obtener_sector(id)