from Risk_project_ufps.core_risk.dao.PaisDao import *


class PaisController:

    def listar_paises(self):
        pais_dao = PaisDao()
        return pais_dao.listar_paises()
