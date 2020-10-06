from Risk_project_ufps.core_risk.dto.models import Propabilidad, Proyecto


class ProbabilidadDao():

    def listar_probabilidades_by_proyecto(self, proyecto):
        probabilidades = {}
        try:      
            probabilidades = Propabilidad.objects.filter(proyecto = proyecto).order_by("propabilidad_valor")
        except Exception as e:
            raise e
        finally:      
            return probabilidades

    def listar_probabilidades_by_proyecto_linea(self, proyecto, linea_base):
        probabilidades = {}
        try:      
            probabilidades = Propabilidad.objects.using('base').filter(proyecto = proyecto, proyecto_linea_base=linea_base).order_by("propabilidad_valor")
        except Exception as e:
            raise e
        finally:      
            return probabilidades




    def crear_probabilidad(self, propabilidad_categoria, propabilidad_valor, proyecto):
        probabilidad = None
        try:
            probabilidad = Propabilidad.objects.create(
                propabilidad_categoria = propabilidad_categoria,
                propabilidad_valor = propabilidad_valor,
                proyecto = proyecto
            )
        except Exception as e:
            raise e
        finally:
            return probabilidad

    def actualizar_probabilidad(self,probabilidad, propabilidad_categoria, propabilidad_valor):        
        try:
            probabilidad.propabilidad_categoria = propabilidad_categoria
            probabilidad.propabilidad_valor = propabilidad_valor                
            probabilidad.save()
        except Exception as e:
            raise e
        finally:
            return probabilidad

    def eliminar_probabilidades_by_proyecto(self, proyecto):
        result = None
        try:
            result = Propabilidad.objects.filter(proyecto=proyecto).delete()
        except Exception as e:
            print(e)
        finally:
            return result

    def obtener_probabilidad_by_id(self, probabilidad_id) -> Propabilidad:
        """
        Permite consultar una probabilidad de ocurrencia especifica a partir de su atributo proyecto_id

        :type probabilidad_id: int:
        """
        try:
            return Propabilidad.objects.get(propabilidad_id=probabilidad_id)
        except Exception as e:
            print(e)
            return None













