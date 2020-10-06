from contextlib import closing

from django.db import connections
from Risk_project_ufps.core_risk.dto.models import *

class LeccionDao():

	def listar_lecciones(self, proyecto):
		lecciones = None
		try:
			lecciones = Leccion.objects.using('base').filter(proyecto_id = proyecto.proyecto_id)
		except Error as e:
			print(e)
		finally:      
			return lecciones

	def get_leccion_by_id(self, id):
		leccion = None
		try:
			leccion = Leccion.objects.using('base').get(leccion_id = id)
		except Error as e:
			print(e)
		finally:      
			return leccion

	def eliminar_leccion(self, leccion):
		with closing(connections['base'].cursor()) as cursor:
			sql = 'DELETE FROM `leccion`' \
				  'WHERE `leccion`.`leccion_id` = %s '
			cursor.execute(
				sql,
				[leccion.leccion_id],
			) 
		return "Se elimino la lección de forma exitosa"
	
	def editar_leccion(self, leccion, descripcion):
		with closing(connections['base'].cursor()) as cursor:
			sql = 'UPDATE `leccion`' \
				  'SET `leccion_descripcion` = %s' \
				  'WHERE `leccion`.`leccion_id` = %s '
			cursor.execute(
				sql,
				[descripcion, leccion.leccion_id],
			) 
		return "Se actualizó la lección de forma exitosa"
	

		
	def registrar_leccion(self, proyecto, descripcion):


		flag = False

		try:
			with closing(connections['base'].cursor()) as cursor:
				cursor.execute(
				'INSERT INTO `leccion`(`leccion_descripcion`, `proyecto_id`, `proyecto_linea_base` )'
				'VALUES (%s, %s, %s)',
				(descripcion, proyecto.proyecto_id , proyecto.proyecto_linea_base))
				flag = True
		except Exception as e:
			raise e
		finally:
			return flag
				
			

