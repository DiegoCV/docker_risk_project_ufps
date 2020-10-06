from Risk_project_ufps.core_risk.dto.models import ClasificacionRiesgo


class ClasificacionRiesgoDao:

    def listar_clasificaciones_by_proyecto(self, proyecto):
        clasificaciones = {}
        try:
            clasificaciones = ClasificacionRiesgo.objects.filter(proyecto=proyecto).order_by('clasificacion_riesgo_min')
        except Exception as e:
            print(e)
        finally:
            return clasificaciones

    def listar_clasificaciones_by_proyecto_linea(self, proyecto, linea_base):
        clasificaciones = {}
        try:
            clasificaciones = ClasificacionRiesgo.objects.using('base').filter(proyecto=proyecto, proyecto_linea_base=linea_base).order_by('clasificacion_riesgo_min')
        except Exception as e:
            print(e)
        finally:
            return clasificaciones

    def eliminar_clasificaciones_by_proyecto(self, proyecto):
        result = None
        try:
            result = ClasificacionRiesgo.objects.filter(proyecto=proyecto).delete()
        except Exception as e:
            print(e)
        finally:
            return result

    def crear_clasificacion(self, clasificacion_riesgo_nombre, clasificacion_color, clasificacion_riesgo_min,
                            clasificacion_riesgo_max, proyecto):
        result = None
        try:
            result = ClasificacionRiesgo.objects.create(
              clasificacion_riesgo_nombre=clasificacion_riesgo_nombre,
              clasificacion_color=clasificacion_color,
              clasificacion_riesgo_min=clasificacion_riesgo_min,
              clasificacion_riesgo_max=clasificacion_riesgo_max,
              proyecto=proyecto
            )
        except Exception as e:
            print(e)
        finally:
            return result
