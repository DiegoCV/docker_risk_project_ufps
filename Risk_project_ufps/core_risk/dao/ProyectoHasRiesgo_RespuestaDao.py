from contextlib import closing

from django.db import connections

from Risk_project_ufps.core_risk.dto.models import *


class ProyectoHasRiesgo_RespuestaDao():

    def registrar_respuesta_proyecto(self, proyecto_riesgo, riesgo_respuesta, tipo_respuesta):
        with closing(connections['riesgos'].cursor()) as cursor:
            cursor.execute(
                'INSERT INTO `proyecto_has_riesgo_respuesta`(`proyecto_has_id`, `respuesta_has_id`, `tipo_respuesta` )'
                'VALUES (%s, %s, %s)',
                (proyecto_riesgo.proyecto_has_riesgo_id, riesgo_respuesta.riesgo_has_respuesta_id, tipo_respuesta),
            )

            return "Se registro respuesta exitosamente."

    def listar_riesgos_respuesta(self, proyecto_id):
        respuestas = {}
        try:
            sql = 'SELECT * FROM respuesta re ' \
                  'INNER JOIN riesgo_has_respuesta ri ' \
                  'ON re.respuesta_id=ri.respuesta_id ' \
                  'INNER JOIN proyecto_has_riesgo_respuesta tr ' \
                  'ON ri.riesgo_has_respuesta_id=tr.respuesta_has_id ' \
                  'INNER JOIN proyecto_has_riesgo qr ' \
                  'ON tr.proyecto_has_id=qr.proyecto_has_riesgo_id ' \
                  'WHERE qr.proyecto_id = %s'
            respuestas = Respuesta.objects.raw(sql, [proyecto_id])

        except Exception as e:
            print(e)

        finally:
            return respuestas


    def listar_riesgos_respuesta_base(self, proyecto):
        """
        :param proyecto:Proyecto
        """
        respuestas = {}
        try:
            sql = 'SELECT * FROM respuesta re ' \
                  'INNER JOIN riesgo_has_respuesta ri ' \
                  'ON re.respuesta_id=ri.respuesta_id ' \
                  'INNER JOIN proyecto_has_riesgo_respuesta tr ' \
                  'ON ri.riesgo_has_respuesta_id=tr.respuesta_has_id ' \
                  'INNER JOIN proyecto_has_riesgo qr ' \
                  'ON tr.proyecto_has_id=qr.proyecto_has_riesgo_id ' \
                  'WHERE qr.proyecto_id = %s ' \
                  'AND qr.proyecto_linea_base = %s ' \
                  'AND tr.proyecto_linea_base = %s ' \
                  'AND ri.proyecto_linea_base = %s ' \
                  'AND re.proyecto_linea_base = %s '
            respuestas = Respuesta.objects.using('base').raw(sql, [proyecto.proyecto_id,
                                                                   proyecto.proyecto_linea_base,
                                                                   proyecto.proyecto_linea_base,
                                                                   proyecto.proyecto_linea_base,
                                                                   proyecto.proyecto_linea_base])
        except Exception as e:
            print(e)
        finally:
            return respuestas


    def listar_riesgos_respuesta_linea(self, proyecto_id, linea_base):
        respuestas = {}
        try:
            sql = 'SELECT * FROM respuesta re ' \
                  'INNER JOIN riesgo_has_respuesta ri ' \
                  'ON re.respuesta_id=ri.respuesta_id ' \
                  'INNER JOIN proyecto_has_riesgo_respuesta tr ' \
                  'ON ri.riesgo_has_respuesta_id=tr.respuesta_has_id ' \
                  'INNER JOIN proyecto_has_riesgo qr ' \
                  'ON tr.proyecto_has_id=qr.proyecto_has_riesgo_id ' \
                  'WHERE qr.proyecto_id = %s AND re.proyecto_linea_base = %s AND ri.proyecto_linea_base = %s AND tr.proyecto_linea_base = %s AND qr.proyecto_linea_base = %s'
            respuestas = Respuesta.objects.using('base').raw(sql, [proyecto_id, linea_base, linea_base, linea_base, linea_base])

        except Exception as e:
            print(e)
        finally:
            return respuestas

    def get_riesgo_respuesta_by_id(self, proyecto_riesgo, riesgo_respuesta):
        respuesta = None
        try:
            respuesta = ProyectoHasRiesgoRespuesta.objects.get(
                respuesta_has_id=riesgo_respuesta.riesgo_has_respuesta_id,
                proyecto_has_id=proyecto_riesgo.proyecto_has_riesgo_id)

        except Exception as e:
            print(e)

        finally:
            return respuesta

    def actualizar_tipo_respuesta(self, proyecto_respuesta, tipo_respuesta):
      with closing(connections['riesgos'].cursor()) as cursor:
            sql = 'UPDATE proyecto_has_riesgo_respuesta ' \
                  'SET tipo_respuesta = %s' \
                  'WHERE proyecto_has_id = %s ' \
                  'AND respuesta_has_id = %s'
            cursor.execute(
                sql,
                [tipo_respuesta, proyecto_respuesta.proyecto_has_id,
                 proyecto_respuesta.respuesta_has_id],
            )

            

    def eliminar(self, proyecto_has_riesgo, riesgo_has_respuesta):
        """

        :param proyecto_has_riesgo: ProyectoHasRiesgo
        :param riesgo_has_respuesta: RiesgoHasRespuesta
        """

        with closing(connections['riesgos'].cursor()) as cursor:
            sql = 'DELETE FROM proyecto_has_riesgo_respuesta ' \
                  'WHERE proyecto_has_id = %s ' \
                  'AND respuesta_has_id = %s'
            cursor.execute(
                sql,
                [proyecto_has_riesgo.proyecto_has_riesgo_id,
                 riesgo_has_respuesta.riesgo_has_respuesta_id],
            )






