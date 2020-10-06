from Risk_project_ufps.core_risk.dto.models import *

class PaisDao():

  def listar_paises(self):
    paises = {}
    try:
      paises = Pais.objects.all()
    except Error as e:
      print(e)
    finally:      
      return paises 