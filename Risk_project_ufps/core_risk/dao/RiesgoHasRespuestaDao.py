from contextlib import closing

from django.db import connections
from Risk_project_ufps.core_risk.dto.models import *


class RiesgoHasRespuestaDao():

    def registrar_respuesta_riesgo(self, respuesta, riesgo):
        with closing(connections['riesgos'].cursor()) as cursor:
            cursor.execute(
                'INSERT INTO `riesgo_has_respuesta`(`riesgo_id`, `respuesta_id`)'
                'VALUES (%s, %s)',
                (riesgo.riesgo_id, respuesta.respuesta_id), )
            return "Se registro respuesta exitosamente."

    def obtener_respuesta_riesgo(self, riesgo: int, respuesta: int):
        """

        :type riesgo: int
        :type respuesta: int
        """
        riesgo_respuesta = None
        try:
            riesgo_respuesta = RiesgoHasRespuesta.objects.get(riesgo_id=riesgo, respuesta_id=respuesta)
        except Exception as e:
            print(e)

        finally:
            return riesgo_respuesta

    def listar_respuesta_riesgo(self, id):
        riesgos = {}
        try:
            sql = "SELECT * FROM riesgo_has_respuesta re INNER JOIN riesgo ri ON re.riesgo_id=ri.riesgo_id INNER JOIN sub_categoria s ON ri.sub_categoria_id=s.sub_categoria_id INNER JOIN categoria c ON s.categoria_id=c.categoria_id INNER JOIN rbs r ON c.rbs_id = r.rbs_id WHERE r.gerente_id = %s"
            riesgos = RiesgoHasRespuesta.objects.raw(sql,[id])
        except Exception as e:
            print(e)
        finally:
            return riesgos