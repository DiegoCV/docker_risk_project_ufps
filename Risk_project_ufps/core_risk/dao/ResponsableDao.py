from Risk_project_ufps.core_risk.dao.ProyectoHasRiesgoDao import *

from Risk_project_ufps.core_risk.dto.models import *


class ResponsableDao:

    def registrar_responsable(self, nombre, descripcion, proyecto, rol):
        responsable = Responsble(
            responsble_nombre=nombre,
            responsble_descripcion=descripcion,
            proyecto_id=proyecto,
            rol_id=rol.rol_id)
        try:
            responsable.save()
        except Exception as e:
            print(e)
        finally:
            return "Se registro un miembro de equipo exitosamente."

    def listar_responsables(self, id):
        responsables = {}
        try:
            responsables = Responsble.objects.filter(proyecto_id=id)
        except Exception as e:
            print(e)
        finally:
            return responsables

    def obtener_responsable(self, id):

        try:
            responsable = Responsble.objects.get(responsable_id=id)
        except Exception as e:
            print(e)
        finally:
            return responsable

    def editar_responsable(self, responsable, nombre, descripcion, rol):
        responsable = responsable
        try:
            responsable.responsble_nombre = nombre
            responsable.responsble_descripcion = descripcion
            responsable.rol_id = rol.rol_id
            responsable.save()
        except Exception as e:
            print(e)
        finally:
            return "Se actualizo la información del miembro del equipo exitosamente."

    def eliminar_responsable(self, responsable):
        responsable = responsable
        try:
            responsable.delete()
        except Exception as e:
            print(e)
        finally:
            return "Se eliminó un miembro del equipo exitosamente."

    def eliminar_responsable_riesgo(self, responsable_id, riesgo_id, proyecto_id):
        proyecto_has_riesgo_dao = ProyectoHasRiesgoDao()
        return proyecto_has_riesgo_dao.set_responsable_null(responsable_id, riesgo_id, proyecto_id)










