from contextlib import closing

from django.db import connection
from django.db import connections

from Risk_project_ufps.core_risk.dto.models import *

class ProyectoHasRiesgoDao():

    """def registrar_proyecto_riesgo(self, proyecto, riesgo):
        proyecto_riesgo = None
        try:
            proyecto_riesgo = ProyectoHasRiesgo(
                proyecto = proyecto,
                riesgo = riesgo             
            )
            proyecto_riesgo.save()      
        except Error as e:
            print(e)
        finally:
            return proyecto_riesgo"""

    def registrar_proyecto_riesgo(self, proyecto, riesgo):
        with closing(connections['riesgos'].cursor()) as cursor:
            cursor.execute(
                'INSERT INTO `proyecto_has_riesgo`(`proyecto_id`, `riesgo_id`)'
                'VALUES (%s, %s)',
                (proyecto.proyecto_id, riesgo.riesgo_id),
            )


    def registrar_proyecto_riesgo_editado(self, proyecto, riesgo):
        with closing(connections['riesgos'].cursor()) as cursor:
            cursor.execute(
                'INSERT INTO `proyecto_has_riesgo`(`proyecto_id`, `riesgo_id`, `is_editado`)'
                'VALUES (%s, %s, 1)',
                (proyecto.proyecto_id, riesgo.riesgo_id),
            )

    def actualizar_fecha(self, proyecto_riesgo, fecha):
        with closing(connections['riesgos'].cursor()) as cursor:
            sql = 'UPDATE proyecto_has_riesgo ' \
                  'SET fecha_manifestacion = %s' \
                  'WHERE proyecto_has_riesgo_id = %s '
            cursor.execute(
                sql,
                [fecha, proyecto_riesgo.proyecto_has_riesgo_id],
            )

    def agregar_responsable_riesgo(self, proyecto_riesgo, responsable):         

        proyecto_riesgo = proyecto_riesgo
        try:
            proyecto_riesgo.responsable = responsable
            proyecto_riesgo.save()
        except ProyectoHasRiesgo.DoesNotExist:
            proyecto_riesgo = None
        finally:
            return "Se actualizo responsable al riesgo exitosamente."

    def listar_responsables_riesgo(self, proyecto_id):
        responsables_riesgo = {}
        try:
            #Revisar esta consulta
            responsables_riesgo = Responsble.objects.raw("SELECT * FROM responsble re INNER JOIN proyecto_has_riesgo pr ON re.responsable_id=pr.responsable_id WHERE pr.proyecto_id = %s", [proyecto_id])

        except Exception as e:
            print(e)

        finally:
            return responsables_riesgo

    def listar_proyecto_has_riesgo_by_proyecto(self, proyecto):
        """
        Permite consultar todos los registros de la tabla proyecto_has_riesgo filtrados por el proyecto_id

        Este metodo retorna un rawqueryset porque hago un innerjoin con responsable para sacarme el nombre
        del responsable, despues en el controlador formateo para que se vea bonito

        :param proyecto:Proyecto
        :return:
        """
        try:
            sql = "SELECT * FROM proyecto_has_riesgo phr " \
                  "INNER JOIN responsble res " \
                  "ON phr.responsable_id = res.responsable_id " \
                  "INNER JOIN impacto i " \
                  "ON phr.impacto_id = i.impacto_id " \
                  "INNER JOIN propabilidad p " \
                  "ON phr.propabilidad_id = p.propabilidad_id " \
                  "INNER JOIN riesgo r " \
                  "ON phr.riesgo_id = r.riesgo_id " \
                  "WHERE phr.proyecto_id = %s " \
                  "ORDER BY phr.riesgo_id ASC"
            return ProyectoHasRiesgo.objects.raw(sql, [proyecto.proyecto_id])

        except Exception as e:
            return None


    def get_by_riesgo_and_proyecto(self, proyecto, riesgo) -> ProyectoHasRiesgo:
        proyecto_riesgo = None
        try:
            proyecto_riesgo = ProyectoHasRiesgo.objects.get(proyecto_id=proyecto, riesgo_id=riesgo)
        except ProyectoHasRiesgo.DoesNotExist:
            proyecto_riesgo = None
        finally:
            return proyecto_riesgo

    def get_by_riesgo_and_proyecto_2(self, riesgo, proyecto):
        proyecto_riesgo = None
        try:
            proyecto_riesgo = ProyectoHasRiesgo.objects.get(riesgo=riesgo, proyecto=proyecto )
        except Exception as e:
            print(e)
        finally:
            return proyecto_riesgo

    def get_by_riesgo_and_proyecto_2_linea(self, riesgo, proyecto, linea_base):
        
        proyecto_riesgo = None
        try:
            proyecto_riesgo = ProyectoHasRiesgo.objects.using('base').get(riesgo=riesgo, proyecto=proyecto, proyecto_linea_base=linea_base)
        except Exception as e:
            print(e)
        finally:
            return proyecto_riesgo

    def eliminar_by_riesgo_and_proyecto(self, proyecto_riesgo):
        proyecto_riesgo = proyecto_riesgo
        try:
            proyecto_riesgo.delete()
        except ProyectoHasRiesgo.DoesNotExist:
            proyecto_riesgo = None
        finally:
            return "Se eliminó riesgo del proyecto de forma exitosa."


    def set_responsable_null(self, responsable_id, riesgo_id, proyecto_id):
        with closing(connections['riesgos'].cursor()) as cursor:
            try:
                sql = 'UPDATE `proyecto_has_riesgo` ' \
                      'SET `responsable_id` = NULL  ' \
                      'WHERE `proyecto_id` = %s ' \
                      'AND `riesgo_id` = %s ' \
                      'AND `responsable_id` = %s;'
                cursor.execute(
                    sql,
                    [proyecto_id, riesgo_id, responsable_id],
                )
            except Exception as e:
                print(e)














