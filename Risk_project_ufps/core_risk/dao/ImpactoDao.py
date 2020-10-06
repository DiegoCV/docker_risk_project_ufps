from Risk_project_ufps.core_risk.dto.models import Impacto
from Risk_project_ufps.core_risk.dto.models import Proyecto


class ImpactoDao:

    def listar_impactos_by_proyecto(self, proyecto):
        impactos = {}
        try:
            impactos = Impacto.objects.filter(proyecto=proyecto).order_by('impacto_valor')
        except Exception as e:
            raise e
        finally:
            return impactos

    def listar_impactos_by_proyecto_linea(self, proyecto, linea_base):
        impactos = {}
        try:
            impactos = Impacto.objects.using('base').filter(proyecto=proyecto, proyecto_linea_base=linea_base).order_by('impacto_valor')
        except Exception as e:
            raise e
        finally:
            return impactos



    def crear_impacto(self, impacto_categoria, impacto_valor, proyecto):
        impacto = None
        try:
            impacto = Impacto.objects.create(
                impacto_categoria=impacto_categoria,
                impacto_valor=impacto_valor,
                proyecto=proyecto
            )
        except Exception as e:
            raise e
        finally:
            return impacto

    def actualizar_impacto(self, impacto, impacto_categoria, impacto_valor):
        try:
            impacto.impacto_categoria = impacto_categoria
            impacto.impacto_valor = impacto_valor
            impacto.save()
        except Exception as e:
            raise e
        finally:
            return impacto

    def eliminar_impactos_by_proyecto(self, proyecto):
        result = None
        try:
            result = Impacto.objects.filter(proyecto=proyecto).delete()
        except Exception as e:
            print(e)
        finally:
            return result

    def obtener_impacto_by_id_and_proyecto(self, impacto_id, proyecto) -> Impacto:
        """

        :type impacto_id: int
        :type proyecto: Proyecto
        """
        impacto = None
        try:
            impacto = Impacto.objects.get(impacto_id=impacto_id, proyecto=proyecto)
        except Exception as e:
            raise e
        finally:
            return impacto

