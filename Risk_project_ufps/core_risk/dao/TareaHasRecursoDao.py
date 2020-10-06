from Risk_project_ufps.core_risk.dto.models import *
from contextlib import closing
from django.db import connections


class TareaHasRecursoDao():

    def agregar_recurso_tarea(self, tarea, recurso, cantidad):
        with closing(connections['riesgos'].cursor()) as cursor:
            cursor.execute(
                'INSERT INTO `tarea_has_recurso`(`tarea_id`, `recurso_id`, `cantidad` )'
                'VALUES (%s, %s, %s)',
                (tarea.tarea_id, recurso.recurso_id, cantidad),
            )

            return "Se asigno recurso exitosamente."

    def get_recurso_tarea_by_id(self, tarea, recurso):
        tarea_recurso = None
        try:
            tarea_recurso = TareaHasRecurso.objects.get(tarea_id=tarea.tarea_id, recurso_id=recurso.recurso_id)
        except Exception as e:
            print(e)
        finally:
            return tarea_recurso

    def eliminar_recurso_tarea(self, tarea_recurso):
        tarea_recurso = tarea_recurso
        try:
            tarea_recurso.delete()
        except Exception as e:
            print(e)
        finally:
            return "Recurso desvinculado exitosamente"

    def eliminar_recurso_tarea_2(self, recurso_id, tarea_id):
        try:
            with closing(connections['riesgos'].cursor()) as cursor:
                sql = 'DELETE FROM tarea_has_recurso ' \
                      'WHERE recurso_id = %s ' \
                      'AND tarea_id = %s'
                cursor.execute(
                    sql,
                    [recurso_id,
                     tarea_id]
                )
                return "Eliminado correctamente"
        except Exception:
            return "No se pudo eliminar"








