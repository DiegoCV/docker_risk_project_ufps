from Risk_project_ufps.core_risk.dao.RespuestaDao import *
from Risk_project_ufps.core_risk.dao.RiesgoHasRespuestaDao import *
from Risk_project_ufps.core_risk.dao.ProyectoHasRiesgo_RespuestaDao import *
from Risk_project_ufps.core_risk.dao.RiesgoDao import *
from Risk_project_ufps.core_risk.dao.ProyectoDao import *

from Risk_project_ufps.core_risk.dto.models import *
from datetime import datetime

class RespuestaController:

    def registrar_respuesta(self, nombre, descripcion,tipo):
        respuesta_dao = RespuestaDao()
        return respuesta_dao.registrar_respuesta(nombre, descripcion, tipo)

    def validar_respuesta(self, nombre, proyecto_id):
        respuesta_dao = RespuestaDao()
        return respuesta_dao.validar_respuesta(nombre, proyecto_id)

    def obtener_respuesta(self, id):
        respuesta_dao = RespuestaDao()
        return respuesta_dao.obtener_respuesta(id)

    def eliminar_respuesta(self, respuesta):
        respuesta_dao = RespuestaDao()
        return respuesta_dao.eliminar_respuesta(respuesta)

    def editar_respuesta(self, respuesta, nombre, descripcion):
        respuesta_dao = RespuestaDao()
        return respuesta_dao.editar_respuesta(respuesta, nombre, descripcion)


    def registrar_respuesta_riesgo(self, respuesta, riesgo):
        respuesta_riesgo_dao = RiesgoHasRespuestaDao()
        return respuesta_riesgo_dao.registrar_respuesta_riesgo(respuesta, riesgo)

    def listar_respuesta_riesgo(self, id):
        respuesta_riesgo_dao = RiesgoHasRespuestaDao()
        return respuesta_riesgo_dao.listar_respuesta_riesgo(id)

    
    def obtener_respuesta_riesgo(self, riesgo, respuesta):
        respuesta_riesgo_dao = RiesgoHasRespuestaDao()
        return respuesta_riesgo_dao.obtener_respuesta_riesgo(riesgo, respuesta)

    def registrar_respuesta_proyecto(self, proyecto_riesgo, riesgo_respuesta, tipo_respuesta):
        p_r_r= ProyectoHasRiesgo_RespuestaDao()
        return p_r_r.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta, tipo_respuesta)

    def get_riesgo_respuesta_by_id(self, proyecto_riesgo, riesgo_respuesta):
        p_r_r= ProyectoHasRiesgo_RespuestaDao()
        return p_r_r.get_riesgo_respuesta_by_id(proyecto_riesgo, riesgo_respuesta)

    def actualizar_tipo_respuesta(self, proyecto_respuesta, tipo_respuesta):
        p_r_r= ProyectoHasRiesgo_RespuestaDao()
        return p_r_r.actualizar_tipo_respuesta(proyecto_respuesta, tipo_respuesta)

    def desasociar_respuesta_riesgo_by_proyecto(self, respuesta_id, riesgo_id, proyecto_id):

        proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()
        riesgo_has_respuesta_dao = RiesgoHasRespuestaDao()
        proyecto_has_riesgo_respuesta_dao = ProyectoHasRiesgo_RespuestaDao()

        proyecto_has_riesgo = proyecto_has_riesgo_dao.get_by_riesgo_and_proyecto(proyecto_id, riesgo_id)
        riesgo_has_respuesta = riesgo_has_respuesta_dao.obtener_respuesta_riesgo(riesgo_id, respuesta_id)

        proyecto_has_riesgo_respuesta_dao.eliminar(proyecto_has_riesgo, riesgo_has_respuesta)


    def listar_riesgos_respuesta(self, proyecto_id):
        p_r_r= ProyectoHasRiesgo_RespuestaDao()
        respuestas = p_r_r.listar_riesgos_respuesta(proyecto_id)
        aux = {}
        for respuesta in respuestas:
            key = "riesgo_"+str(respuesta.riesgo_id)
            riesgo_aux = aux.get(key)
            if(riesgo_aux):
                riesgo_aux.append(
                    dict(
                        respuesta_id=respuesta.respuesta_id,
                        respuesta_nombre=respuesta.respuesta_nombre,
                        respuesta_descripcion=respuesta.respuesta_descripcion,
                        tipo_respuesta= respuesta.tipo_respuesta,
                        riesgo_has_respuesta=respuesta.riesgo_has_respuesta_id
                    )
                )
            else:
                aux[key] = []
                aux[key].append(
                    dict(
                        respuesta_id=respuesta.respuesta_id,
                        respuesta_nombre=respuesta.respuesta_nombre,
                        respuesta_descripcion=respuesta.respuesta_descripcion,
                        tipo_respuesta= respuesta.tipo_respuesta,
                        riesgo_has_respuesta=respuesta.riesgo_has_respuesta_id
                    )
                )
        return aux


    def listar_riesgos_respuesta_base(self, proyecto_id):

        proyecto_dao = ProyectoDao()
        p_r_r = ProyectoHasRiesgo_RespuestaDao()

        proyecto = proyecto_dao.obtener_proyecto(proyecto_id)
        respuestas = p_r_r.listar_riesgos_respuesta_base(proyecto)

        aux = {}
        for respuesta in respuestas:
            key = "riesgo_"+str(respuesta.riesgo_id)
            riesgo_aux = aux.get(key)
            if(riesgo_aux):
                riesgo_aux.append(
                    dict(
                        respuesta_id=respuesta.respuesta_id,
                        respuesta_nombre=respuesta.respuesta_nombre,
                        respuesta_descripcion=respuesta.respuesta_descripcion,
                        tipo_respuesta= respuesta.tipo_respuesta,
                        riesgo_has_respuesta=respuesta.riesgo_has_respuesta_id
                    )
                )
            else:
                aux[key] = []
                aux[key].append(
                    dict(
                        respuesta_id=respuesta.respuesta_id,
                        respuesta_nombre=respuesta.respuesta_nombre,
                        respuesta_descripcion=respuesta.respuesta_descripcion,
                        tipo_respuesta= respuesta.tipo_respuesta,
                        riesgo_has_respuesta=respuesta.riesgo_has_respuesta_id
                    )
                )
        return aux


    def listar_riesgos_respuesta_linea(self, proyecto_id, linea_base):
        p_r_r= ProyectoHasRiesgo_RespuestaDao()
        respuestas = p_r_r.listar_riesgos_respuesta_linea(proyecto_id, linea_base)
        aux = {}
        for respuesta in respuestas:
            key = "riesgo_"+str(respuesta.riesgo_id)
            riesgo_aux = aux.get(key)
            if(riesgo_aux):
                riesgo_aux.append(
                    dict(
                        respuesta_id=respuesta.respuesta_id,
                        respuesta_nombre=respuesta.respuesta_nombre,
                        respuesta_descripcion=respuesta.respuesta_descripcion,
                        tipo_respuesta= respuesta.tipo_respuesta,
                        riesgo_has_respuesta=respuesta.riesgo_has_respuesta_id
                    )
                )
            else:
                aux[key] = []
                aux[key].append(
                    dict(
                        respuesta_id=respuesta.respuesta_id,
                        respuesta_nombre=respuesta.respuesta_nombre,
                        respuesta_descripcion=respuesta.respuesta_descripcion,
                        tipo_respuesta= respuesta.tipo_respuesta,
                        riesgo_has_respuesta=respuesta.riesgo_has_respuesta_id
                    )
                )
        return aux


    def get_datetime(self, now):
        try:

            date_time = now.strftime("%d/%m/%Y")
            
        except Exception as e:
            return None
        
        return date_time



    def obtener_respuestas_sugeridas(self, proyecto_id: int):
        """
        Consulta todas las respuestas asociadas a los riesgos
        del proyecto que no se hayan utilizado dentro del mismo proyecto
        :param proyecto_id:
        :return: dict
        """
        respuesta_dao = RespuestaDao()
        riesgo_dao = RiesgoDao()
        proyecto = Proyecto(proyecto_id=proyecto_id)
        riesgos = riesgo_dao.get_riesgos_by_proyecto(proyecto)
        aux = {}
        for riesgo in riesgos:
            key = "riesgo_" + str(riesgo.riesgo_id)
            aux[key] = []
            respuestas = respuesta_dao.obtener_respuestas_sugeridas_from_riesgo_by_proyecto(riesgo, proyecto)
            for respuesta in respuestas:
                aux[key].append(
                    dict(
                        respuesta_id=respuesta.respuesta_id,
                        respuesta_nombre=respuesta.respuesta_nombre,
                        respuesta_descripcion=respuesta.respuesta_descripcion,
                    )
                )

        return aux

    def registrar_respuesta_sugeridas_riesgo(self, respuestas_id, riesgo_id, proyecto_id):
        """
        Permite registrar las respuestas sugeridas de un riesgo
        :param respuestas_id:
        :param riesgo_id:
        :param proyecto_id:
        :return:
        """
        respuesta_dao = RespuestaDao()
        p_h_r = ProyectoHasRiesgoDao()
        respuesta_riesgo_dao = RiesgoHasRespuestaDao()

        riesgo = Riesgo(riesgo_id=riesgo_id)
        proyecto = Proyecto(proyecto_id=proyecto_id)
        for respuesta_id in respuestas_id:
            # Consulto la respuesta
            respuesta_aux = respuesta_dao.obtener_respuesta(respuesta_id)
            # Duplico la respuesta
            respuesta = respuesta_dao.registrar_respuesta(respuesta_aux.respuesta_nombre, respuesta_aux.respuesta_descripcion)
            # Inserto el muchos a muchos entre respuesta y riesgos
            self.registrar_respuesta_riesgo(respuesta, riesgo) #LineaA
            # Consulto el muchos a muchos entre riesgo y proyecto
            proyecto_riesgo = p_h_r.get_by_riesgo_and_proyecto(proyecto, riesgo) #LineaB
            # Consulto el muchos a muchos entre riesgo y respuesta, el que se acabo de agregar en la linea A
            riesgo_respuesta = respuesta_riesgo_dao.obtener_respuesta_riesgo(riesgo, respuesta) #LineaC
            # Insertar el muchos a muchos entre linea B y linea C
            self.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta, None)







