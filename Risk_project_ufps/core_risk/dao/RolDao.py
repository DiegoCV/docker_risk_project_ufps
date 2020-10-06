from Risk_project_ufps.core_risk.dto.models import *

class RolDao():


	def registrar_rol(self, nombre, descripcion, gerente):
		rol = Rol(
		    	rol_nombre = nombre,
		    	rol_descripcion = descripcion,
		    	gerente = gerente)
		try:
			rol.save()      
		except Error as e:
			print(e)
		finally:
			return rol

	def listar_roles(self, gerente):
		lista_roles = None
		try:
			lista_roles = Rol.objects.filter(gerente_id=gerente.gerente_id)     
		except Error as e:
			print(e)
		finally:
			return lista_roles

	def editar_rol(self, rol, nombre, descripcion):
		rol = rol
		try:
			rol.rol_nombre = nombre
			rol.rol_descripcion = descripcion
			rol.save()      
		except Error as e:
			print(e)
		finally:
			return rol

	def get_rol_by_id(self, rol_id):
		rol = None
		try:
			rol = Rol.objects.get(rol_id=rol_id)     
		except Error as e:
			print(e)
		finally:
			return rol

	def eliminar_rol(self, rol):
		rol = rol
		try:
			rol.delete()     
		except Error as e:
			return False
		finally:
			return True