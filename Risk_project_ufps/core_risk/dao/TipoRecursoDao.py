from Risk_project_ufps.core_risk.dto.models import *

class TipoRecursoDao():

	def registrar_tipo_recurso(self, nombre, descripcion, gerente):
		tipo_recurso = TipoRecurso(
				tipo_recurso_nombre = nombre,
    			tipo_recurso_descripcion = descripcion,
    			gerente = gerente)
		try:
			tipo_recurso.save()
		except Error as e:
			print(e)
		finally:
			return "Se registró un tipo de recurso exitosamente."

	def eliminar_tipo_recurso(self, tipo_recurso):
  		tipo_recurso = tipo_recurso
  		try:
  			tipo_recurso.delete()
  		except Error as e:
  			print(e)
  		finally:
  			return "Se elimino un tipo de recurso de forma exitosa."


	def editar_tipo_recurso(self, tipo_recurso, nombre, descripcion):
  		tipo_recurso = tipo_recurso
  		try:
  			tipo_recurso.tipo_recurso_nombre = nombre
  			tipo_recurso.tipo_recurso_descripcion = descripcion
  			tipo_recurso.save()
  		except Error as e:
  			print(e)
  		finally:
  			return "Se actualizo la información de tipo de recurso de forma exitosa."


  		

	def obtener_tipo_recurso(self, id):
  		try:
  			tipo_recurso = TipoRecurso.objects.get( tipo_recurso_id=id)
  		except Error as e:
  			print(e)
  		finally:
  			return tipo_recurso



  		

	def listar_tipos_recursos(self, id):
  		tipo_recurso = {}
  		try:
  			tipo_recurso = TipoRecurso.objects.filter(gerente_id=id)
  		except Error as e:
  			print(e)
  		finally:
  			return tipo_recurso

  	

  	

  		
  	