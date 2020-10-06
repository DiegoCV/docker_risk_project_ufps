from Risk_project_ufps.core_risk.dao.RbsDao import *
from Risk_project_ufps.core_risk.dao.CategoriaDao import *
from Risk_project_ufps.core_risk.dao.SubcategoriaDao import *
from Risk_project_ufps.core_risk.dao.GerenteDao import *
from Risk_project_ufps.core_risk.dao.RiesgoDao import *
from Risk_project_ufps.core_risk.dao.ProyectoDao import *
from Risk_project_ufps.core_risk.dao.SectorDao import *
from Risk_project_ufps.core_risk.dto.models import *

from django.forms.models import model_to_dict

class RbsController():  

    rbs_dao = RbsDao()

    def get_rbs_gerente_id(self, gerente_id):
        gerente = Gerente(gerente_id = gerente_id) 
        return self.rbs_dao.get_rbs_gerente_id(gerente)

    def crear_rbs_pmbok(self, gerente_id):      
        gerente = Gerente(gerente_id = gerente_id) 
        return self.rbs_dao.crear_rbs(gerente)      

    def crear_rbs_sugerida(self, gerente_id):
        gerente_dao = GerenteDao()  
        gerente = gerente_dao.get_by_id(gerente_id)
        
        rbs = self.rbs_dao.crear_rbs(gerente, 2) 

        categoria_dao = CategoriaDao()
        categorias = categoria_dao.get_categorias_by_sector(gerente.sector)
        
        sub_categoria_dao = SubcategoriaDao()

        rbs_sugerida = self.obtener_rbs_sugerida(gerente.sector.sector_id)

        for aux in rbs_sugerida:   
            categoria = categoria_dao.duplicar_categoria(aux["categoria"], rbs) 
            if (aux["subcategorias"]):                        
                for subcategoria in aux["subcategorias"]:
                    sub_categoria_dao.duplicar_sub_categoria(categoria, subcategoria)
        return rbs                                
              

    def crear_rbs_blanco(self, gerente_id):
        gerente = Gerente(gerente_id = gerente_id) 
        return self.rbs_dao.crear_rbs(gerente, 1)       

    def obtener_rbs_general(self, gerente_id):
        """Construye la rbs general del gerente.

        Devuelve en un diccionario la informacion de las categorias
        junto con las subcategorias asociadas.

        Se encarga de consultar la rbs del gerente y a partir de su id
        consultar todas las categorias y subcategorias asociados.
        Parámetros:
        gerente_id -- corresponde al id del gerente en la base de datos     
        Excepciones:
        ValueError -- Si gerente no existe      
        """
        gerente_dao = GerenteDao()
        gerente = gerente_dao.get_by_id(gerente_id)
        categoria_dao = CategoriaDao()
        categorias = categoria_dao.get_categorias_by_gerente(gerente)
        rbs = []
        sub_categoria_dao = SubcategoriaDao()
        for categoria in categorias:
            subcategorias = sub_categoria_dao.get_sub_categorias_by_categoria(categoria)
            rbs.append({
                "categoria" : model_to_dict(categoria),
                "subcategorias": list(subcategorias.values())
            })
        return rbs

    def obtener_rbs_completa(self, gerente_id):
        """Construye la rbs con los riesgos por subcategoria del gerente.

        Devuelve en un diccionario la informacion de las categorias
        junto con las subcategorias asociadas y sus riesgos.

        Se encarga de consultar la rbs del gerente y a partir de su id
        consultar todas las categorias y subcategorias asociados.
        Parámetros:
        gerente_id -- corresponde al id del gerente en la base de datos     
        Excepciones:
        ValueError -- Si gerente no existe      
        """
        gerente_dao = GerenteDao()
        gerente = gerente_dao.get_by_id(gerente_id)
        categoria_dao = CategoriaDao()
        categorias = categoria_dao.get_categorias_by_gerente(gerente)
        rbs = []
        sub_categoria_dao = SubcategoriaDao()
        riesgo_dao = RiesgoDao()
        for categoria in categorias:
            subcategorias = sub_categoria_dao.get_sub_categorias_by_categoria(categoria)    
            aux = []        
            for subcategoria in subcategorias:
                riesgos = riesgo_dao.get_riesgo_by_subcategoria(subcategoria)   
                if riesgos == None:
                    aux.append({
                        "subcategoria" : model_to_dict(subcategoria),
                        "riesgos" : []
                    })
                else: 
                    aux.append({
                        "subcategoria" : model_to_dict(subcategoria),
                        "riesgos" : list(riesgos.values())
                    })               
            rbs.append({
                "categoria" : model_to_dict(categoria),
                "subcategorias": aux
            })
        return rbs

    def obtener_rbs_completa_by_proyecto(self, gerente_id, proyecto_id):
        """Construye la rbs con los riesgos por subcategoria del gerente.

        Devuelve en un diccionario la informacion de las categorias
        junto con las subcategorias asociadas y sus riesgos.

        Se encarga de consultar la rbs del gerente y a partir de su id
        consultar todas las categorias y subcategorias asociados.
        Parámetros:
        gerente_id -- corresponde al id del gerente en la base de datos     
        Excepciones:
        ValueError -- Si gerente no existe      
        """
        gerente_dao = GerenteDao()
        gerente = gerente_dao.get_by_id(gerente_id)
        categoria_dao = CategoriaDao()
        categorias = categoria_dao.get_categorias_by_gerente(gerente)
        proyecto_dao = ProyectoDao()
        proyecto = proyecto_dao.obtener_proyecto(proyecto_id)
        rbs = []
        sub_categoria_dao = SubcategoriaDao()
        riesgo_dao = RiesgoDao()
        for categoria in categorias:
            subcategorias = sub_categoria_dao.get_sub_categorias_by_categoria(categoria)    
            aux = []        
            for subcategoria in subcategorias:
                riesgos = riesgo_dao.get_riesgo_by_subcategoria(subcategoria)                  
                if riesgos == None:                  
                    aux.append({
                        "subcategoria" : model_to_dict(subcategoria),
                        "riesgos" : []
                    })
                else: 
                    riesgos = list(riesgos.values()) 
                    if(len(riesgos) > 0):                                                
                        for riesgo in riesgos:
                            e = riesgo_dao.riesgo_is_proyecto(Riesgo(riesgo_id=riesgo["riesgo_id"]), proyecto)                            
                            if(e != None):
                                riesgo['is_assigned'] = True
                                riesgo['fecha_manifestacion'] = e.fecha_manifestacion.strftime("%Y-%m-%d")
                            else:
                                riesgo['is_assigned'] = False                              
                    aux.append({
                        "subcategoria" : model_to_dict(subcategoria),
                        "riesgos" : riesgos
                    })               
            rbs.append({
                "categoria" : model_to_dict(categoria),
                "subcategorias": aux
            })
        return rbs

    def obtener_rbs_sugerida(self, sector_id):
        """Construye una rbs de acuerdo al sector.

        Devuelve en un diccionario la informacion de las categorias
        junto con las subcategorias asociadas.

        Se encarga de consultar la rbs del gerente y a partir de su id
        consultar todas las categorias y subcategorias asociados.
        Parámetros:
        gerente_id -- corresponde al id del gerente en la base de datos     
        Excepciones:
        ValueError -- Si gerente no existe      
        """        
        categoria_dao = CategoriaDao() 
        sector_dao = SectorDao()
        sector = sector_dao.obtener_sector(sector_id)
        categorias = categoria_dao.get_categorias_by_sector(sector)
        rbs = []
        indice = {}
        cont = 0
        sub_categoria_dao = SubcategoriaDao()        
        for categoria_aux in categorias:
            categoria_nombre = indice.get(categoria_aux.categoria_nombre)                
            subcategorias = sub_categoria_dao.get_sub_categorias_by_categoria_and_sector(categoria_aux, sector)          
            if subcategorias == None:
                if(categoria_nombre == None):
                    rbs.append({"categoria" : model_to_dict(categoria_aux)})
                    indice[categoria_aux.categoria_nombre] = cont
                    cont = cont + 1
            else:
                if(categoria_nombre == None):
                    rbs.append({
                        "categoria" : model_to_dict(categoria_aux),
                        "subcategorias": self.raw_queryset_as_values_list(subcategorias)
                    })
                    indice[categoria_aux.categoria_nombre] = cont
                    cont = cont + 1
                else:
                    subcategoria_aux = rbs[indice[categoria_aux.categoria_nombre]].get("subcategorias")
                    if(subcategoria_aux == None):
                        rbs[indice]["subcategorias"] = self.raw_queryset_as_values_list(subcategorias)
                    else:
                        subcategoria_aux = subcategoria_aux + self.raw_queryset_as_values_list(subcategorias)
        return rbs        

    def obtener_rbs_proyecto(self, proyecto_id):
        """Construye una rbs de acuerdo al sector.

        Devuelve en un diccionario la informacion de las categorias
        junto con las subcategorias asociadas.

        Se encarga de consultar la rbs del gerente y a partir de su id
        consultar todas las categorias y subcategorias asociados.
        Parámetros:
        gerente_id -- corresponde al id del gerente en la base de datos     
        Excepciones:
        ValueError -- Si gerente no existe      
        """        
        proyecto_dao = ProyectoDao()
        proyecto = proyecto_dao.obtener_proyecto(proyecto_id)

        categoria_dao = CategoriaDao()
        categorias = categoria_dao.get_categorias_by_proyecto(proyecto)    

        sub_categoria_dao = SubcategoriaDao()

        rbs = []

        for categoria in categorias:
            subcategorias = sub_categoria_dao.get_sub_categorias_by_categoria_and_proyecto(categoria, proyecto)
            if subcategorias == None:
                rbs.append({
                    "categoria" : model_to_dict(categoria)                
                })
            else:
                rbs.append({
                    "categoria" : model_to_dict(categoria),
                    "subcategorias": self.raw_queryset_as_values_list(subcategorias)
                })
        return rbs        

    def raw_queryset_as_values_list(self, raw_qs):
        aux = []
        for row in raw_qs:
            aux.append(model_to_dict(row))
        return aux




