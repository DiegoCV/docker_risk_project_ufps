from contextlib import closing

from django.db import connections

from Risk_project_ufps.core_risk.dto.models import *


class ProyectoHasRiesgo_ActividadDao():

    def registrar_actividad_riesgo(self, proyecto_riesgo, actividad):
        with closing(connections['riesgos'].cursor()) as cursor:
            cursor.execute(
                'INSERT INTO `proyecto_has_riesgo_actividad`(`proyecto_has_riesgo_id`, `actividad_id`)'
                'VALUES (%s, %s)',
                (proyecto_riesgo.proyecto_has_riesgo_id, actividad.actividad_id),
            )

            return "Se agrego respuesta al riesgo exitosamente."

    def listar_actividades_riesgo(self, proyecto_id):
        actividades = {}
        try:
            actividades = Actividad.objects.raw(
                "SELECT * FROM actividad act "
                "INNER JOIN proyecto_has_riesgo_actividad pr "
                "ON act.actividad_id=pr.actividad_id "
                "INNER JOIN proyecto_has_riesgo tr "
                "ON pr.proyecto_has_riesgo_id=tr.proyecto_has_riesgo_id "
                "WHERE tr.proyecto_id = %s",
                [proyecto_id])

        except Exception as e:
            print(e)

        finally:
            return actividades

    def validar_actividad(self, proyecto_riesgo_id, actividad_id):
        actividad = None
        try:
            actividad = ProyectoHasRiesgoActividad.objects.get(proyecto_has_riesgo_id=proyecto_riesgo_id,
                                                               actividad_id=actividad_id)
        except Exception as e:
            print(e)

        finally:
            return actividad

    def desasociar_actividad_riesgo(self, proyecto_has_riesgo, actividad):
        actividad_riesgo = None
        try:
            actividad_riesgo = ProyectoHasRiesgoActividad.objects.get(proyecto_has_riesgo=proyecto_has_riesgo,
                                                                      actividad=actividad)
            actividad_riesgo.delete()
        except Exception as e:
            raise e
        finally:
            return actividad_riesgo
