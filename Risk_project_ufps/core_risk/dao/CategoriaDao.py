from Risk_project_ufps.core_risk.dto.models import *


class CategoriaDao():

    def duplicar_categoria(self, categoria, rbs):
        """Aqui llega es una lista categoria"""
        categ = None
        try:
            categ = Categoria.objects.create(
                categoria_nombre=categoria["categoria_nombre"],
                categoria_descripcion=categoria["categoria_descripcion"],
                categoria_default=2,
                categoria_uid=categoria["categoria_uid"],
                rbs=rbs
            )
        except Exception as e:
            raise e
        finally:
            return categ

    def duplicar_categoria_2(self, categoria, rbs):
        """ Aqui llega un model"""
        aux_categoria = None
        try:
            aux_categoria = Categoria.objects.get(categoria_nombre=categoria.categoria_nombre, rbs=rbs)
        except Categoria.DoesNotExist:
            aux_categoria = Categoria.objects.create(
                categoria_nombre=categoria.categoria_nombre,
                categoria_descripcion=categoria.categoria_descripcion,
                categoria_default=2,
                categoria_uid=categoria.categoria_uid,
                rbs=rbs
            )
        finally:
            return aux_categoria

    def get_categorias_by_gerente(self, gerente):
        categorias = None
        try:
            categorias = Categoria.objects.raw(
                "SELECT c.categoria_id, c.categoria_nombre FROM categoria c INNER JOIN rbs r ON c.rbs_id = r.rbs_id WHERE r.gerente_id = %s",
                [gerente.gerente_id])
        except Error as e:
            print(e)
        finally:
            return categorias

    def get_categorias_by_sector(self, sector):
        categorias = []
        try:
            sql = "SELECT DISTINCT c.categoria_id, c.categoria_nombre, c.categoria_descripcion, c.categoria_uid FROM categoria c INNER JOIN sub_categoria sc ON c.categoria_id = sc.categoria_id INNER JOIN riesgo r ON sc.sub_categoria_id = r.sub_categoria_id INNER JOIN proyecto_has_riesgo p_h_r ON r.riesgo_id = p_h_r.riesgo_id INNER JOIN proyecto p ON p_h_r.proyecto_id = p.proyecto_id WHERE p.sector_id = %s"
            categorias = Categoria.objects.raw(sql, [sector.sector_id, ])
        except Error as e:
            print(e)
        finally:
            return categorias

    def get_categorias_by_proyecto(self, proyecto):
        categorias = []
        try:
            sql = "SELECT DISTINCT c.categoria_id, c.categoria_nombre, c.categoria_descripcion, c.categoria_uid FROM categoria c INNER JOIN sub_categoria sc ON c.categoria_id = sc.categoria_id INNER JOIN riesgo r ON sc.sub_categoria_id = r.sub_categoria_id INNER JOIN proyecto_has_riesgo p_h_r ON r.riesgo_id = p_h_r.riesgo_id INNER JOIN proyecto p ON p_h_r.proyecto_id = p.proyecto_id WHERE p.proyecto_id = %s"
            categorias = Categoria.objects.raw(sql, [proyecto.proyecto_id])
        except Error as e:
            print(e)
        finally:
            return categorias
