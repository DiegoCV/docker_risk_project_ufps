from Risk_project_ufps.core_risk.dto.models import *
import datetime

class GerenteDao():

	def get_by_id(self, gerente_id):
		gerente = None
		try:
			gerente = Gerente.objects.get(gerente_id = gerente_id)
		except Exception as e:
			print(e)
		finally:      
			return gerente

	def validar_gerente(self, usuario):
		gerente = None
		try:
			gerente = Gerente.objects.get(gerente_usuario = usuario)
		except Exception as e:
			print(e)
		finally:      
			return gerente

		
	def registrar_gerente(self, id, usuario, correo, nombre, sector, profesion, empresa, pais, metodologia, certificacion, fecha_creacion):

		gerente = Gerente(
			gerente_id=id,
			gerente_usuario=usuario,
			gerente_correo=correo,
			gerente_nombre=nombre,
			sector=sector,
			gerente_profesion=profesion,
			gerente_empresa=empresa,
			pais_id=pais,
			gerente_metodologias=metodologia,
			gerente_certificaciones=certificacion,
			gerente_fecha_creacion=fecha_creacion
		)	
		try:
			gerente.save()      
		except Exception as e:
			print(e)
		finally:      
			return "Se registro el gerente exitosamente."



	def obtener_gerente(self, id):
		gerente = {}

		try:
			gerente = Gerente.objects.get(gerente_id=id)
		except Exception as e:
			print(e)
		finally:
			return gerente

	def actualizar_gerente(self, gerente, nombre, correo, profesion, empresa, sector, certificacion, metodologia):
		gerente = gerente
		gerente.gerente_nombre = nombre
		gerente.gerente_correo = correo
		gerente.gerente_profesion = profesion
		gerente.gerente_empresa = empresa
		gerente.sector = sector
		gerente.gerente_certificaciones = certificacion
		gerente.gerente_metodologias = metodologia
		try:
			gerente.save()
		except Exception as e:
			print(e)
		finally:
			
				return "Se actualizó la información del gerente exitosamente."