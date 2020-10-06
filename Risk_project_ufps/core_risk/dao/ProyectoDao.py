from Risk_project_ufps.core_risk.dto.models import *
from contextlib import closing
from django.db import connections

class ProyectoDao:

	def registrar_proyecto(self, nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio, gerente, sector):
		proyecto = None
		try:
			proyecto = Proyecto.objects.create(
				proyecto_nombre=nombre,
				proyecto_objetivo=objetivo,
				proyecto_alcance=alcance,
				proyecto_descripcion=descripcion,
				proyecto_presupuesto=presupuesto,
				proyecto_fecha_inicio=fecha_inicio,
				gerente=gerente,
				sector=sector,
				proyecto_rbs_status=0,
				proyecto_linea_base=0)
		except Exception as e:
			print(e)
		finally:
			return proyecto

	def obtener_proyecto(self, id):
		proyecto = None
		try:
			proyecto = Proyecto.objects.get(proyecto_id=id)
		except Error as e:
			print(e)
		finally:
			return proyecto



	def validar_proyecto(self, nombre, gerente_id):
		proyecto = None
		try:
			proyecto = Proyecto.objects.get(proyecto_nombre=nombre, gerente_id=gerente_id)
		except Error as e:
			print(e)
		finally:
			return proyecto

	def editar_proyecto(self, proyecto, nombre, objetivo, alcance, descripcion, presupuesto, fecha_inicio, sector):
		proyecto = proyecto
		try:
			proyecto.proyecto_nombre = nombre
			proyecto.proyecto_objetivo = objetivo
			proyecto.proyecto_alcance = alcance
			proyecto.proyecto_descripcion = descripcion
			proyecto.proyecto_presupuesto = presupuesto
			proyecto.proyecto_fecha_inicio = fecha_inicio
			proyecto.sector = sector
			proyecto.save()
		except Error as e:
			print(e)
		finally:
			return "Se actualizo la información del proyecto de forma exitosamente."

	def cerrar_proyecto(self, proyecto, fecha):
		proyecto = proyecto
		try:
			proyecto.proyecto_fin_status = 1
			proyecto.proyecto_fecha_finl = fecha          
			proyecto.save()
		except Error as e:
			print(e)
		finally:
			return proyecto

	def listar_proyectos(self, id):
		proyectos = {}
		try:
			proyectos = Proyecto.objects.filter(gerente_id=id).order_by('-proyecto_fecha_inicio')
		except Error as e:
			print(e)
		finally:
			return proyectos

	def has_actividades(self, proyecto):
		flag = False
		try:
			sql = "SELECT * FROM `actividad` WHERE `proyecto_id` = %s LIMIT 1"
			actividad = Actividad.objects.raw(sql, [proyecto.proyecto_id, ])
			if (actividad):
				flag = True
		except Exception as e:
			raise e
		finally:
			return flag

	def crear_linea_base(self, gerente_id: int, proyecto):
		try:
			with closing(connections['riesgos'].cursor()) as cursor:
				cursor.callproc('crear_linea_base',
								[gerente_id, proyecto.proyecto_id, proyecto.proyecto_linea_base + 1])
			flag = True
		except Exception as e:
			print(e)
			flag = False
		return flag
