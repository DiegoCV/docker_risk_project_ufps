from Risk_project_ufps.core_risk.dao.LeccionDao import *


class LeccionController:

    def registrar_leccion(self, proyecto, descripcion):
        leccion_dao = LeccionDao()
        return leccion_dao.registrar_leccion( proyecto, descripcion)

    def listar_lecciones(self, proyecto):
        leccion_dao = LeccionDao()
        return leccion_dao.listar_lecciones(proyecto)

    def get_leccion_by_id(self, id):
        leccion_dao = LeccionDao()
        return leccion_dao.get_leccion_by_id(id)

    def eliminar_leccion(self, leccion):
        leccion_dao = LeccionDao()
        return leccion_dao.eliminar_leccion(leccion)

    def editar_leccion(self, leccion, descripcion):
        leccion_dao = LeccionDao()
        return leccion_dao.editar_leccion(leccion, descripcion)