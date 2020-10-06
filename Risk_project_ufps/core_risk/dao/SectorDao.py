from Risk_project_ufps.core_risk.dto.models import *

class SectorDao():

  def listar_sectores(self):
    sectores = {}
    try:
      sectores = Sector.objects.all()
    except Error as e:
      print(e)
    finally:      
      return sectores


  def obtener_sector(self, id):
  	sector = {}
  	try:
  		sector = Sector.objects.get(sector_id=id)  		
  	except Exception as e:
  		print(e)
  	finally:
  		return sector


 

 