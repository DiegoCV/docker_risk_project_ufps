from Risk_project_ufps.core_risk.dto.models import *


class ActividadDao:

    def listar_actividades_proyecto(self, proyecto_id):
        actividades = {}
        try:
            sql = "SELECT * FROM `actividad` WHERE `proyecto_id` = %s ORDER BY `actividad_orden`"
            actividades = Actividad.objects.raw(sql, [proyecto_id, ])
        except Exception as e:
            print(e)
        finally:
            return actividades

    def obtener_actividad(self, actividad_id):
        actividad = None
        try:
            actividad = Actividad.objects.get(actividad_id=actividad_id)
        except Exception as e:
            print(e)
        finally:
            return actividad
