from Risk_project_ufps.core_risk.dto.models import *

class SubcategoriaDao():

    def listar_subcategorias(self, id):
        subcategorias = {}
        try:
            subcategorias = SubCategoria.objects.raw("SELECT s.sub_categoria_id, s.sub_categoria_nombre FROM sub_categoria s INNER JOIN categoria c ON s.categoria_id=c.categoria_id INNER JOIN rbs r ON c.rbs_id = r.rbs_id WHERE r.gerente_id = %s", [id])
        except Error as e:
            print(e)

        finally:
            return subcategorias

    def obtener_subcategoria(self, id):
        subcategoria = {}
        try:
            subcategoria = SubCategoria.objects.get(sub_categoria_id=id)
        except Error as e:
            print(e)

        finally:
            return subcategoria


    def get_sub_categorias_by_categoria(self, categoria):
        subcategoria = None
        try:
            subcategoria = SubCategoria.objects.filter(categoria = categoria)
        except Error as e:
            print(e)
        finally:
            return subcategoria


    def get_sub_categorias_by_categoria_and_proyecto(self, categoria, proyecto):
        sub_categorias = None
        try:  
            sql = "SELECT DISTINCT sc.sub_categoria_id, sc.sub_categoria_nombre, sc.sub_categoria_descripcion,  sc.sub_categoria_uid FROM sub_categoria sc INNER JOIN riesgo r ON sc.sub_categoria_id = r.sub_categoria_id INNER JOIN proyecto_has_riesgo p_h_r ON r.riesgo_id = p_h_r.riesgo_id INNER JOIN proyecto p ON p_h_r.proyecto_id = p.proyecto_id WHERE sc.categoria_id = %s AND p.proyecto_id = %s"
            sub_categorias = SubCategoria.objects.raw(sql, [categoria.categoria_id, proyecto.proyecto_id])
        except Error as e:
            print(e)
        finally:      
            return sub_categorias

    def get_sub_categorias_by_categoria_and_sector(self, categoria, sector):
        sub_categorias = None
        try:  
            sql = "SELECT DISTINCT sc.sub_categoria_id, sc.sub_categoria_nombre, sc.sub_categoria_descripcion,  sc.sub_categoria_uid FROM sub_categoria sc INNER JOIN riesgo r ON sc.sub_categoria_id = r.sub_categoria_id INNER JOIN proyecto_has_riesgo p_h_r ON r.riesgo_id = p_h_r.riesgo_id INNER JOIN proyecto p ON p_h_r.proyecto_id = p.proyecto_id WHERE sc.categoria_id = %s AND p.sector_id = %s"
            sub_categorias = SubCategoria.objects.raw(sql, [categoria.categoria_id, sector.sector_id])
        except Error as e:
            print(e)
        finally:      
            return sub_categorias       

    def duplicar_sub_categoria(self, categoria, subcategoria):
        """En el primer metodo por alguna razon la subcategoria llega una lista y no un modelo"""
        sub_categoria = None        
        #try:
        sub_categoria = SubCategoria(
            sub_categoria_nombre = subcategoria["sub_categoria_nombre"],
            sub_categoria_descripcion = subcategoria["sub_categoria_descripcion"],
            sub_categoria_default = 2,
            sub_categoria_uid = subcategoria["sub_categoria_uid"],
            categoria = categoria
        )
        sub_categoria.save()
        #except Exception as e:
            #print(e)        
        #finally:
        return sub_categoria

    def duplicar_sub_categoria_2(self, categoria, subcategoria):
        """Aqui la subcategoria es un Models"""
        sub_categoria = None        
        try:
            sub_categoria = SubCategoria.objects.get(
                sub_categoria_nombre=subcategoria.sub_categoria_nombre,
                categoria=categoria
            )
        except SubCategoria.DoesNotExist:
            sub_categoria = SubCategoria.objects.create(
                sub_categoria_nombre=subcategoria.sub_categoria_nombre,
                sub_categoria_descripcion=subcategoria.sub_categoria_descripcion,
                sub_categoria_default=2,
                sub_categoria_uid=subcategoria.sub_categoria_uid,
                categoria=categoria
            )
        finally:
            return sub_categoria












