from Risk_project_ufps.core_risk.dto.models import *


class RespuestaDao:

    def registrar_respuesta(self, nombre, descripcion, tipo):
        return Respuesta.objects.create(
            respuesta_nombre=nombre,
            respuesta_descripcion=descripcion,
            respuesta_tipo=tipo
        )

    def obtener_respuesta(self, id):
        """
		Permite consultar una respuesta por su id
		
		:rtype: Respuesta
		:type id: int
		"""
        try:
            return Respuesta.objects.get(respuesta_id=id)
        except Exception as e:
            print(e)
            return None

    def validar_respuesta(self, nombre, proyecto_id):

        respuesta = None       
        try:
            sql = 'SELECT * FROM respuesta re ' \
                  'INNER JOIN riesgo_has_respuesta ri ' \
                  'ON re.respuesta_id=ri.respuesta_id ' \
                  'INNER JOIN proyecto_has_riesgo_respuesta tr ' \
                  'ON ri.riesgo_has_respuesta_id=tr.respuesta_has_id ' \
                  'INNER JOIN proyecto_has_riesgo qr ' \
                  'ON tr.proyecto_has_id=qr.proyecto_has_riesgo_id ' \
                  'WHERE qr.proyecto_id = %s AND re.respuesta_nombre = %s'
            respuesta = Respuesta.objects.raw(sql, [proyecto_id, nombre])

        except Exception as e:
            print(e)

        finally:
            return respuesta



    def editar_respuesta(self, respuesta, nombre, descripcion):
        respuesta = respuesta
        try:
            respuesta.respuesta_descripcion = descripcion
            respuesta.respuesta_nombre = nombre
            respuesta.save()
        except Exception as e:
            print(e)

        finally:
            return "Se actualizo la información de la respuesta."

    def eliminar_respuesta(self, respuesta):
        respuesta = respuesta
        try:
            respuesta.delete()
        except Exception as e:
            print(e)

        finally:
            return "Se elimino respuesta exitosamente."

    def obtener_respuestas_sugeridas_from_riesgo_by_proyecto(self, riesgo, proyecto):
        """
        Consulta todas las respuestas que se hayan asosiado a este riesgo en todos los proyectos
        en que se utilizo execto al que entro
        :param proyecto:Proyecto"""
        #try:
        sql = "SELECT r.respuesta_id, r.respuesta_nombre, r.respuesta_descripcion, r.respuesta_costo, rhr.riesgo_id  FROM respuesta r  INNER JOIN riesgo_has_respuesta rhr  ON r.respuesta_id = rhr.respuesta_id  INNER JOIN proyecto_has_riesgo_respuesta phrr  ON rhr.riesgo_has_respuesta_id = phrr.respuesta_has_id  INNER JOIN proyecto_has_riesgo phr  ON phrr.proyecto_has_id = phr.proyecto_has_riesgo_id INNER JOIN riesgo ri ON phr.riesgo_id = ri.riesgo_id WHERE ri.riesgo_nombre='"+riesgo.riesgo_nombre+"' AND phr.proyecto_id <> %s"
        return Respuesta.objects.raw(sql, [proyecto.proyecto_id,])
        #except Exception as e:
        #    print(e)
        #    return []

