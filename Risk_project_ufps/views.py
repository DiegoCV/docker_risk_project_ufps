from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth import logout as do_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import JsonResponse, HttpResponseRedirect

from django.urls import reverse

from django.core import serializers

from django.forms.models import model_to_dict

from Risk_project_ufps.core_risk.dto.models import *

from json import dumps

from datetime import date
from datetime import datetime

import json
import os

from Risk_project_ufps.core_risk.controller.SectorController import *
from Risk_project_ufps.core_risk.controller.PaisController import *
from Risk_project_ufps.core_risk.controller.RbsController import *
from Risk_project_ufps.core_risk.controller.ProyectoController import *
from Risk_project_ufps.core_risk.controller.GerenteController import *
from Risk_project_ufps.core_risk.controller.SubcategoriaController import *
from Risk_project_ufps.core_risk.controller.RiesgoController import *
from Risk_project_ufps.core_risk.controller.RespuestaController import *
from Risk_project_ufps.core_risk.controller.TipoRecursoController import *
from Risk_project_ufps.core_risk.controller.RecursoController import *
from Risk_project_ufps.core_risk.controller.ResponsableController import *
from Risk_project_ufps.core_risk.controller.ActividadController import *
from Risk_project_ufps.core_risk.controller.ReporteController import *
from Risk_project_ufps.core_risk.controller.RolController import *
from Risk_project_ufps.core_risk.controller.TareaController import *
from Risk_project_ufps.core_risk.controller.LeccionController import *

"""
////////////////////////////////////////////////////////////////////////////
    Metodos generales de usuario
/////////////////////////////////////////////////////////////////////////////
"""


# Autentica usuario y carga la vista de inicio
def autenticar(request):
    if request.user.is_authenticated:
        proyecto_controller = ProyectoController()
        lista_proyectos = proyecto_controller.listar_proyectos(request.user.id)
        return render(request, "inicio.html", {"lista_proyectos": lista_proyectos})

    return render("login.html")


# Cierra sesión de un usuario y carga la vista de login
def cerrar_sesion(request):
    do_logout(request)
    return render(request, "login.html")


# Carga la vista de registrar gerente
def registrar_gerente(request):
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    pais_controller = PaisController()
    lista_paises = pais_controller.listar_paises()
    return render(request, "registration/registrar_gerente.html",
                  {"lista_sectores": lista_sectores, "lista_paises": lista_paises})


# Duplica el usuario para accerder a los metodos de autenticación de django
def registrar_usuario(usuario, correo, password, nombre):
    user = User.objects.create_user(
        username=usuario, 
        email=correo, 
        password=password, 
        first_name=nombre
    )
    user.save()
    return User.objects.get(username=usuario)


# Registra un nuevo gerente en la bd riesgos
def nuevo_gerente(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.validar_gerente(request.POST["gerente_usuario"])
    if gerente == None:
        sector_controller = SectorController()
        sector = sector_controller.obtener_sector(request.POST["gerente_sector"])
        user = registrar_usuario(
                    request.POST["gerente_usuario"], 
                    request.POST["gerente_correo"],
                    request.POST["gerente_password"], 
                    request.POST["gerente_nombre"]
                    )
        fecha_creacion=get_fecha_actual()
        mensaje = gerente_controller.registrar_gerente(
            user.id, 
            request.POST["gerente_usuario"],
            request.POST["gerente_correo"], 
            request.POST["gerente_nombre"],
            sector, 
            request.POST["gerente_profesion"],
            request.POST["gerente_empresa"],
            request.POST["gerente_pais"],
            request.POST["metodologia"],
            request.POST["certificacion"],
            fecha_creacion
            )
        return render(request, "registration/login.html", {"mensaje": mensaje})
    sector_controller = SectorController()
    pais_controller = PaisController()

    lista_sectores = sector_controller.listar_sectores()
    lista_paises = pais_controller.listar_paises()

    return render(
        request,
        "registration/registrar_gerente.html",
        dict(
        mensaje_editar="El usuario ya se encuentra registrado.",
        lista_sectores=lista_sectores,
        lista_paises=lista_paises
        )
    )


# Muestra el perfil del gerente y actualiza su información
def mi_perfil(request):
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    if request.method == "POST":
        sector = sector_controller.obtener_sector(request.POST["gerente_sector"])
        mensaje = gerente_controller.actualizar_gerente(gerente, request.POST["gerente_nombre"],
                                                        request.POST["gerente_correo"],
                                                        request.POST["gerente_profesion"],
                                                        request.POST["gerente_empresa"], sector,
                                                        request.POST["certificacion"],
                                                        request.POST["metodologia"])
        return render(request, "mi_perfil.html",
                      {"gerente": gerente, "lista_sectores": lista_sectores, "mensaje": mensaje})

    return render(request, "mi_perfil.html", {"gerente": gerente, "lista_sectores": lista_sectores})


# Carga la vista de inicio
@login_required(login_url='/accounts/login/')
def inicio(request):
    proyecto_controller = ProyectoController()
    lista_proyectos = proyecto_controller.listar_proyectos(request.user.id)

    return render(request, "inicio.html", {"lista_proyectos": lista_proyectos})


"""
////////////////////////////////////////////////
    Metodos y views relacionados con proyecto 
////////////////////////////////////////////////
"""


# Carga la vista de registrar proyecto y lo registra
def nuevo_proyecto(request):
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    fecha_actual = datetime.datetime.now()
    formato = "%Y-%m-%d"
    today = fecha_actual.strftime(formato)
    data = {"lista_sectores": lista_sectores, "today": today}
    rbs_controller = RbsController()
    rbs = rbs_controller.get_rbs_gerente_id(request.user.id)
    if rbs:
        data["rbs"] = rbs
    if (request.method == "POST"):
        proyecto_controller = ProyectoController()
        aux = proyecto_controller.validar_proyecto(request.POST["proyecto_nombre"], request.user.id)
        print(aux)
        if aux == None:
            try:
                gerente_controller = GerenteController()
                sector = sector_controller.obtener_sector(request.POST["proyecto_sector"])
                print("sector", sector)
                gerente = gerente_controller.obtener_gerente(request.user.id)

                proyecto = proyecto_controller.registrar_proyecto(
                    request.POST["proyecto_nombre"],
                    request.POST["proyecto_objetivo"],
                    request.POST["proyecto_alcance"],
                    request.POST["proyecto_descripcion"],
                    request.POST["proyecto_presupuesto"],
                    request.POST["proyecto_fecha_inicio"],
                    gerente,
                    sector
                )
                if (proyecto):
                    data["mensaje"] = "Se registro un proyecto exitosamente."
                else:
                    data["mensaje"] = "No se pudo registrar exitosamente."
                if (request.POST["actividades"] == '1'):
                    actividades = json.loads(request.POST["actividades_data"])["tasks"]
                    orden = 0
                    for actividad in actividades:
                        act = Actividad(
                            actividad_id="p_" + str(proyecto.proyecto_id) + "_a_" + str(actividad["uid"]),
                            actividad_orden=orden,
                            actividad_uuid=actividad["uid"],
                            actividad_nombre=actividad["name"],
                            actividad_level=actividad["level"],
                            actividad_wbs=actividad["WBS"],
                            proyecto=proyecto,
                            actividad_fecha_inicio=actividad["start"],
                            actividad_fecha_fin=actividad["end"],
                            duracion=actividad["duration"],
                        )
                        act.save()
                        orden = orden + 1
                return render(request, "nuevo_proyecto.html", data)

            except Exception as inst:

                print(inst)
                raise inst
                return HttpResponse(status=400)

            data["mensaje"] = "El nombre del proyecto ya se encuentra en uso."

    return render(request, "nuevo_proyecto.html", data)


"""
/////////////////////////////////////
    Metodos de la EDR
////////////////////////////////////
"""


# Carga la vista de la RBS
def mi_rbs(request):
    rbs_controller = RbsController()
    if (rbs_controller.get_rbs_gerente_id(request.user.id)):
        return render(request, "mi_rbs.html")
    else:
        return render(request, "mi_rbs_inicial.html")


def rbs_configurar(request):
    rbs_controller = RbsController()
    if request.method == 'POST':
        rbs_option = request.POST.get('rbs_option', "")
        try:
            if rbs_option == "1":
                rbs_controller.crear_rbs_pmbok(request.user.id)
            elif rbs_option == "2":
                rbs_controller.crear_rbs_sugerida(request.user.id)
            elif rbs_option == "3":
                rbs_controller.crear_rbs_blanco(request.user.id)
            return HttpResponse({"msg": "rbs_creada"}, status=202)
        except Exception as inst:
            print(inst)
            return HttpResponse({"msg": "error"}, status=404)
    else:
        return HttpResponse({"msg": "error"}, status=404)


"""
////////////////////////////////////////////////
    Metodos relacionados con la rbs general
////////////////////////////////////////////////
"""


def profile(request):
    if request.method == 'GET':
        rbs_controller = RbsController()
        rbs = rbs_controller.obtener_rbs_general(request.user.id)
        return JsonResponse(rbs, safe=False)
    else:
        return HttpResponse(status=404)


def confirmar_cambios_rbs(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            acciones = json.loads(request.POST.get('acciones', None))
            rbs = Rbs.objects.get(gerente_id=request.user.id)
            elementos_nuevos = {}
            for accion in acciones:
                if accion['accion'] == 'agregar_c':
                    categoria = Categoria(
                        categoria_nombre=accion['categoria_nombre'],
                        categoria_descripcion=accion['categoria_descripcion'],
                        rbs=rbs
                    )
                    categoria.save()
                    elementos_nuevos[accion['categoria_id']] = categoria
                elif accion['accion'] == 'agregar_sc':
                    if ('new' in accion['categoria_id']):
                        categoria = elementos_nuevos[accion['categoria_id']]
                    else:
                        categoria = Categoria(categoria_id=accion['categoria_id'])
                    subCategoria = SubCategoria(
                        sub_categoria_nombre=accion['sub_categoria_nombre'],
                        sub_categoria_descripcion=accion['sub_categoria_descripcion'],
                        categoria=categoria
                    )
                    subCategoria.save()
                    elementos_nuevos[accion['sub_categoria_id']] = subCategoria
                elif accion['accion'] == 'eliminar_c':
                    if ('new' in accion['categoria_id']):
                        categoria = elementos_nuevos[accion['categoria_id']]
                        del elementos_nuevos[accion['categoria_id']]
                    else:
                        categoria = Categoria(categoria_id=accion['categoria_id'])
                    categoria.delete()
                elif accion['accion'] == 'eliminar_sc':
                    if ('new' in accion['sub_categoria_id']):
                        sub_categoria = elementos_nuevos[accion['sub_categoria_id']]
                        del elementos_nuevos[accion['sub_categoria_id']]
                    else:
                        sub_categoria = SubCategoria(sub_categoria_id=accion['sub_categoria_id'])
                    sub_categoria.delete()
                elif accion['accion'] == 'editar_c':
                    if ('new' in accion['categoria_id']):
                        categoria = elementos_nuevos[accion['categoria_id']]
                    else:
                        categoria = Categoria(categoria_id=accion['categoria_id'])
                    Categoria.objects.filter(categoria_id=categoria.categoria_id).update(
                        categoria_nombre=accion['categoria_nombre'],
                        categoria_descripcion=accion['categoria_descripcion'])
                elif accion['accion'] == 'editar_sc':
                    if ('new' in accion['sub_categoria_id']):
                        sub_categoria = elementos_nuevos[accion['sub_categoria_id']]
                    else:
                        sub_categoria = SubCategoria(sub_categoria_id=accion['sub_categoria_id'])
                    SubCategoria.objects.filter(sub_categoria_id=sub_categoria.sub_categoria_id).update(
                        sub_categoria_nombre=accion['sub_categoria_nombre'],
                        sub_categoria_descripcion=accion['sub_categoria_descripcion'])
            return JsonResponse({"hola": request.user.username, "e": acciones}, safe=False)
        else:
            return HttpResponse({"Error": "error"}, status=404)


# Carga la vista de nuevo riesgo y registra un riesgo asociado a una subcategoria
def nuevo_riesgo(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)
    if request.method == 'POST':
        subcategoria = subcategoria_controller.obtener_subcategoria(request.POST["sub_categoria_id"])
        riesgo_controller = RiesgoController()
        mensaje = riesgo_controller.registrar_riesgo(request.POST["riesgo_nombre"], request.POST["riesgo_causa"],
                                                     request.POST["riesgo_evento"], request.POST["riesgo_efecto"],
                                                     request.POST["riesgo_tipo"], subcategoria)
        return render(request, "nuevo_riesgo.html",
                      {"lista_subcategorias": lista_subcategorias, "rbs": rbsJSON, "mensaje": mensaje})

    return render(request, "nuevo_riesgo.html", {"lista_subcategorias": lista_subcategorias, "rbs": rbsJSON})


# Carga la tabla dinamica con el listado de riesgos
def mis_riesgos(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)
    return render(request, "mis_riesgos.html", {'rbs': rbsJSON, "lista_subcategorias": lista_subcategorias})


# Edita un riesgo de un gerente y carga el listado de riesgos
def editar_riesgo(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)

    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.listar_riesgos(request.user.id)
    riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])

    subcategoria = subcategoria_controller.obtener_subcategoria(request.POST["sub_categoria_id"])

    mensaje_editar = riesgo_controller.editar_riesgo(riesgo, request.POST["riesgo_nombre"],
                                                     request.POST["riesgo_evento"], request.POST["riesgo_efecto"],
                                                     request.POST["riesgo_causa"], request.POST["riesgo_tipo"],
                                                     subcategoria)

    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)
    if request.method == 'POST':
        return render(request, "mis_riesgos.html",
                      {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "mensaje_editar": mensaje_editar,
                       "lista_subcategorias": lista_subcategorias})

    return render(request, "mis_riesgos.html",
                  {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "lista_subcategorias": lista_subcategorias})


# Elimina un riesgo de un gerente y carga el listado de riesgos
def eliminar_riesgo(request):
    subcategoria_controller = SubcategoriaController()
    lista_subcategorias = subcategoria_controller.listar_subcategorias(request.user.id)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.listar_riesgos(request.user.id)
    riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
    mensaje_eliminar = riesgo_controller.eliminar_riesgo(riesgo)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa(request.user.id)
    rbsJSON = dumps(rbs)

    if request.method == 'POST':
        return render(request, "mis_riesgos.html",
                      {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "mensaje_eliminar": mensaje_eliminar,
                       "lista_subcategorias": lista_subcategorias})

    return render(request, "mis_riesgos.html",
                  {'rbs': rbsJSON, "lista_riesgos": lista_riesgos, "lista_subcategorias": lista_subcategorias})


def asociar_riesgo(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    riesgo_controller = RiesgoController()
    if request.method == 'POST':
        try:
            riesgos_seleccionados = json.loads(request.POST.get('riesgos_seleccionados', None))
            riesgos_sugeridos = json.loads(request.POST.get('riesgos_sugeridos', None))
            aux = riesgo_controller.asosiar_riesgos_proyecto(riesgos_seleccionados, proyecto)
            aux = riesgo_controller.asosiar_riesgos_sugeridos_proyecto(riesgos_sugeridos, proyecto)
            return HttpResponse(status=200)
        except Exception as e:
            raise e
            return HttpResponse(status=400)

        # Carga la vista de nueva respuesta y registra una respuesta asociada a un riesgo


def nueva_respuesta(request):
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.listar_riesgos(request.user.id)

    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        respuesta = respuesta_controller.registrar_respuesta(request.POST["respuesta_nombre"],
                                                             request.POST["respuesta_descripcion"])

        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])

        mensaje = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)

        return render(request, "nueva_respuesta.html", {"lista_riesgos": lista_riesgos, "mensaje": mensaje})

    return render(request, "nueva_respuesta.html", {"lista_riesgos": lista_riesgos})


# Carga el listado de respuestas de un gerente
def mis_respuestas(request):
    respuesta_controller = RespuestaController()

    lista_riesgos_respuesta = respuesta_controller.listar_respuesta_riesgo(request.user.id)

    return render(request, "mis_respuestas.html", {"lista_riesgos_respuesta": lista_riesgos_respuesta})


# Elimina una respuesta y carga el listado de respuestas de un gerente
def eliminar_respuesta(request):
    respuesta_controller = RespuestaController()

    lista_riesgos_respuesta = respuesta_controller.listar_respuesta_riesgo(request.user.id)

    if request.method == 'POST':
        respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id_e"])

        mensaje_eliminar = respuesta_controller.eliminar_respuesta(respuesta)
        return render(request, "mis_respuestas.html",
                      {"lista_riesgos_respuesta": lista_riesgos_respuesta, "mensaje_eliminar": mensaje_eliminar})

    return render(request, "mis_respuestas.html", {"lista_riesgos_respuesta": lista_riesgos_respuesta})


# Actualiza la información de una respuesta y carga el listado de respuestas de un gerente
def editar_respuesta(request):
    respuesta_controller = RespuestaController()
    lista_riesgos_respuesta = respuesta_controller.listar_respuesta_riesgo(request.user.id)

    if request.method == 'POST':
        respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id"])

        mensaje_editar = respuesta_controller.editar_respuesta(respuesta, request.POST["respuesta_nombre"],
                                                               request.POST["respuesta_descripcion"])
        return render(request, "mis_respuestas.html",
                      {"lista_riesgos_respuesta": lista_riesgos_respuesta, "mensaje_editar": mensaje_editar})

    return render(request, "mis_respuestas.html", {"lista_riesgos_respuesta": lista_riesgos_respuesta})


# Registra un tipo de recurso para un gerente y carga los recursos de un gerente
"""
def tipo_recurso(request):
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    if request.method == 'POST':
        gerente_controller = GerenteController()
        gerente = gerente_controller.obtener_gerente(request.user.id)

        mensaje = tipo_recurso_controller.registrar_tipo_recurso(request.POST['tipo_recurso_nombre'],
                                                                 request.POST['tipo_recurso_descripcion'], gerente)

        return render(request, "nuevo_recurso.html", {"mensaje": mensaje, "tipos_recursos": tipos_recursos})
    return render(request, "nuevo_recurso.html", {"tipos_recursos": tipos_recursos})
"""

"""
# Elimina un tipo de recurso y carga el listado de tipos de recursos
def eliminar_tipo_recurso(request):
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    if request.method == 'POST':
        tipo_recurso = tipo_recurso_controller.obtener_tipo_recurso(request.POST['tipo_recurso_id'])

        mensaje_eliminar = tipo_recurso_controller.eliminar_tipo_recurso(tipo_recurso)
        return render(request, "nuevo_recurso.html",
                      {"tipos_recursos": tipos_recursos, "mensaje_eliminar": mensaje_eliminar})

    return render(request, "nuevo_recurso.html", {"tipos_recursos": tipos_recursos})
"""

"""
# Actualiza la información de un tipo de recurso y carga el listado de tipos de recursos
def editar_tipo_recurso(request):
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)

    if request.method == 'POST':
        tipo_recurso = tipo_recurso_controller.obtener_tipo_recurso(request.POST['tipo_recurso_id'])

        mensaje_editar = tipo_recurso_controller.editar_tipo_recurso(tipo_recurso, request.POST['tipo_recurso_nombre'],
                                                                     request.POST['tipo_recurso_descripcion'])

        return render(request, "nuevo_recurso.html",
                      {"tipos_recursos": tipos_recursos, "mensaje_editar": mensaje_editar})

    return render(request, "nuevo_recurso.html", {"tipos_recursos": tipos_recursos})
"""


# Carga la vista de roles del equipo
def roles_equipo(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    return render(request, "roles_equipo.html", {"lista_roles": lista_roles})


# Agrega un nuevo rol y carga la vista de roles de un gerente
def nuevo_rol(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    if request.method == 'POST':

        rol = rol_controller.registrar_rol(request.POST['rol_nombre'], request.POST['rol_descripcion'], gerente)
        if rol == None:
            mensaje_editar = "No se pudo registrar el nuevo rol."
            return render(request, "roles_equipo.html", {"mensaje_error": mensaje_editar, "lista_roles": lista_roles})
        mensaje = "Se registro el nuevo rol exitosamente."
        return HttpResponseRedirect(reverse('roles_equipo'))

    return render(request, "roles_equipo.html", {"lista_roles": lista_roles})


# Actualiza la información de un rol y carga la vista de roles del gerente
def editar_rol(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)
    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        rol_editado = rol_controller.editar_rol(rol, request.POST['rol_nombre'], request.POST['rol_descripcion'])
        if rol_editado == None:
            mensaje_editar = "No se pudo actualizar la información del rol."
            return render(request, "roles_equipo.html", {"mensaje_error": mensaje_editar, "lista_roles": lista_roles})
        mensaje_editar = "Se actualizo la información del rol exitosamente."
        return render(request, "roles_equipo.html", {"mensaje_editar": mensaje_editar, "lista_roles": lista_roles})

    return render(request, "roles_equipo.html", {"lista_roles": lista_roles})


# Elimina un rol y carga la vista de roles del gerente
def eliminar_rol(request):
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)
    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        rol_eliminado = rol_controller.eliminar_rol(rol)
        if rol_eliminado == False:
            mensaje_editar = "No se pudo eliminar la información del rol."
            return render(request, "roles_equipo.html", {"mensaje_error": mensaje_editar, "lista_roles": lista_roles})
        mensaje_eliminar = "Se elimino la información del rol exitosamente."
        return render(request, "roles_equipo.html", {"mensaje_eliminar": mensaje_eliminar, "lista_roles": lista_roles})

    return render(request, "roles_equipo.html", {"lista_roles": lista_roles})


# Carga la vista de un proyecto y permite editarlo
def mi_proyecto(request, id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(id)
    sector_controller = SectorController()
    lista_sectores = sector_controller.listar_sectores()
    duracion = ""
    fecha_actual = datetime.datetime.now()
    fecha_proyecto = datetime.datetime(proyecto.proyecto_fecha_inicio.year, proyecto.proyecto_fecha_inicio.month,
                                       proyecto.proyecto_fecha_inicio.day, 00, 00, 00, 000000)
    if proyecto.proyecto_fecha_finl != None:
        fecha_proyecto_final = datetime.datetime(proyecto.proyecto_fecha_finl.year, proyecto.proyecto_fecha_finl.month,
                                                 proyecto.proyecto_fecha_finl.day, 00, 00, 00, 000000)

        dias = dias = abs((fecha_proyecto - fecha_proyecto_final).days)
        duracion = "El proyecto ya ha finalizado. Tuvo una duración de %i dias." % (dias)
    elif fecha_proyecto > fecha_actual:
        duracion = "El proyecto aun no ha iniciado."
    else:
        dias = abs((fecha_actual - fecha_proyecto).days)
        duracion = "%i dias." % (dias)

    data = {"proyecto": proyecto, "lista_sectores": lista_sectores, "duracion": duracion}

    if (proyecto_controller.has_actividades(id)):
        data["actividades"] = True

    if request.method == 'POST':
        sector = sector_controller.obtener_sector(request.POST["proyecto_sector"])
        mensaje = proyecto_controller.editar_proyecto(proyecto, request.POST["proyecto_nombre"],
                                                      request.POST["proyecto_objetivo"],
                                                      request.POST["proyecto_alcance"],
                                                      request.POST["proyecto_descripcion"],
                                                      request.POST["proyecto_presupuesto"],
                                                      request.POST["proyecto_fecha_inicio"], sector)
        data["mensaje"] = mensaje
        if (request.POST["actividades"] == '1'):
            actividades = json.loads(request.POST["actividades_data"])["tasks"]
            orden = 0
            for actividad in actividades:
                act = Actividad(
                    actividad_id="p_" + str(proyecto.proyecto_id) + "_a_" + str(actividad["uid"]),
                    actividad_orden=orden,
                    actividad_uuid=actividad["uid"],
                    actividad_nombre=actividad["name"],
                    actividad_level=actividad["level"],
                    actividad_wbs=actividad["WBS"],
                    proyecto=proyecto,
                    actividad_fecha_inicio=actividad["start"],
                    actividad_fecha_fin=actividad["end"],
                    duracion=actividad["duration"],
                )
                act.save()
                orden = orden + 1
        return render(request, "procesos/proyecto.html", data)

    return render(request, "procesos/proyecto.html", data)


def eliminar_riesgo_proyecto(request, proyecto_id):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()
        riesgo_proyecto = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
        mensaje_eliminar = riesgo_controller.eliminar_riesgo_by_proyecto(riesgo_proyecto)

        proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
        rbs_controller = RbsController()
        rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
        rbsJSON = dumps(rbs)
        riesgo_controller = RiesgoController()
        lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)

        # Falta agregar de aqui para abajo
        responsable_controller = ResponsableController()
        lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
        actividad_controller = ActividadController()
        lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))

        # Retorna responsables por riesgo de un proyecto
        responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
        # Retorna actividades por riesgo de un proyecto
        actividades_riesgo = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

        # (Funcion que retorna respuestas por riesgo de un proyecto (Revisar)!!!)
        respuesta_controller = RespuestaController()
        respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

        lista_riesgos_sugeridos = riesgo_controller.get_riesgos_sugeridos(proyecto.sector, request.user.id)
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
        """return render(
            request,
            "procesos/identificar_riesgos.html",
            dict(
                proyecto=proyecto,
                rbs=rbsJSON,
                lista_riesgos=lista_riesgos,
                mensaje_eliminar=mensaje_eliminar,
                lista_responsables=lista_responsables,
                lista_actividades=lista_actividades,
                responsables_riesgo=responsables_riesgo,
                actividades_riesgo=actividades_riesgo
            )
        )"""
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


def editar_riesgo_proyecto(request, proyecto_id):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()

        riesgo_editado = riesgo_controller.editar_riesgo_proyecto(
            proyecto_id,
            request.POST["riesgo_id_editar"],
            request.POST["riesgo_nombre"],
            request.POST["riesgo_causa"],
            request.POST["riesgo_evento"],
            request.POST["riesgo_efecto"],
            request.POST["riesgo_tipo"],
            #request.POST["riesgo_fecha_manifestacion"],
        )

        data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)

        return render(request, "procesos/identificar_riesgos.html", data)


################################################################
### Metodo util que permite centralizar los datos necesarios
### para renderizar identificar riesgos
################################################################

def get_data_render_identificar_riesgo(gerente_id, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(gerente_id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    # Falta agregar de aqui para abajo
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = actividad_controller.listar_actividades_proyecto(proyecto_id)

    # Retorna responsables por riesgo de un proyecto
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    # Retorna actividades por riesgo de un proyecto
    actividades_riesgo = actividad_controller.listar_actividades_riesgo(proyecto_id)

    # (Funcion que retorna respuestas por riesgo de un proyecto (Revisar)!!!)
    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

    lista_riesgos_sugeridos = riesgo_controller.get_riesgos_sugeridos(proyecto.sector, gerente_id);

    if (len(lista_riesgos_sugeridos) > 0):
        return {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
                'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
                'lista_riesgos_sugeridos': lista_riesgos_sugeridos, 'respuestas_riesgo': respuestas_riesgo}

    return {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
            'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
            "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
            'respuestas_riesgo': respuestas_riesgo}


def proyecto_nueva_respuesta(request, proyecto_id):
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)
    if request.method == 'POST':
        aux = respuesta_controller.validar_respuesta(request.POST["respuesta_nombre"], proyecto_id)
        if not aux:
            respuesta = respuesta_controller.registrar_respuesta(request.POST["respuesta_nombre"],
                                                                 request.POST["respuesta_descripcion"])
            riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
            mensaje_no = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)
            proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
            riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
            mensaje = respuesta_controller.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta,
                                                                        request.POST["tipo_respuesta"])
            proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
            rbs_controller = RbsController()
            rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
            rbsJSON = dumps(rbs)
            riesgo_controller = RiesgoController()
            lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
            responsable_controller = ResponsableController()
            lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
            actividad_controller = ActividadController()
            lista_actividades = actividad_controller.listar_actividades_proyecto(proyecto_id)
            responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
            actividades_riesgo = actividad_controller.listar_actividades_riesgo(proyecto_id)

            data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)

            data['mensaje'] = mensaje

            return render(request, "procesos/identificar_riesgos.html", data)
        data['mensaje_editar'] = "Ya cuentas con esta respuesta asociada al proyecto."
        return render(request, "procesos/identificar_riesgos.html", data)

    return render(request, "procesos/identificar_riesgos.html", data)


def registrar_riesgo_proyecto(request):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()
        rbs_controller = RbsController()
        proyecto_controller = ProyectoController()

        mensaje = riesgo_controller.registrar_riesgo_proyecto(
            request.POST["riesgo_nombre"],
            request.POST["riesgo_causa"],
            request.POST["riesgo_evento"],
            request.POST["riesgo_efecto"],
            request.POST["riesgo_tipo"],
            request.POST["sub_categoria_id"],
            request.POST["proyecto_id"]
        )

        proyecto = proyecto_controller.obtener_proyecto(request.POST["proyecto_id"])
        rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto.proyecto_id)
        rbsJSON = dumps(rbs)
        riesgo_controller = RiesgoController()
        lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
        responsable_controller = ResponsableController()
        lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
        actividad_controller = ActividadController()
        lista_actividades = actividad_controller.listar_actividades_proyecto(proyecto.proyecto_id)
        responsables_riesgo = riesgo_controller.listar_responsables_riesgo(proyecto.proyecto_id)
        actividades_riesgo = actividad_controller.listar_actividades_riesgo(proyecto.proyecto_id)

        return render(request, "procesos/identificar_riesgos.html",
                      {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos, 'mensaje': mensaje,
                       'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                       "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo})


# Carga la vista de los recursos de un proyecto y registra nuevos recursos
def recursos(request, id):
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(id)
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(id)
    if request.method == 'POST':
        mensaje = recurso_controller.registrar_recurso(proyecto, request.POST['recurso_nombre'],
                                                       request.POST['recurso_costo'], request.POST['tipo_recurso_id'], )

        return render(request, "procesos/mis_recursos.html",
                      {"proyecto": proyecto, "lista_recursos": lista_recursos, "mensaje": mensaje,
                       "tipos_recursos": tipos_recursos})

    return render(request, "procesos/mis_recursos.html",
                  {"proyecto": proyecto, "lista_recursos": lista_recursos, "tipos_recursos": tipos_recursos})


# Elimina un recurso de un proyecto y carga la vista de recursos del proyecto
def eliminar_recurso(request, id):
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(id)
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(id)
    if request.method == 'POST':
        recurso = recurso_controller.obtener_recurso(request.POST['recurso_id'])

        mensaje_eliminar = recurso_controller.eliminar_recurso(recurso)
        return render(request, "procesos/mis_recursos.html",
                      {"proyecto": proyecto, "lista_recursos": lista_recursos, "mensaje_eliminar": mensaje_eliminar,
                       "tipos_recursos": tipos_recursos})

    return render(request, "procesos/mis_recursos.html",
                  {"proyecto": proyecto, "lista_recursos": lista_recursos, "tipos_recursos": tipos_recursos})


# Actualiza la información de un recurso para un proyecto y carga la vista de recursos del proyecto
def editar_recurso(request, id):
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(id)
    tipo_recurso_controller = TipoRecursoController()
    tipos_recursos = tipo_recurso_controller.listar_tipos_recursos(request.user.id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(id)
    if request.method == 'POST':
        recurso = recurso_controller.obtener_recurso(request.POST['recurso_id'])
        mensaje_editar = recurso_controller.editar_recurso(recurso, request.POST['recurso_nombre'],
                                                           request.POST['recurso_costo'])
        return render(request, "procesos/mis_recursos.html",
                      {"proyecto": proyecto, "lista_recursos": lista_recursos, "mensaje_editar": mensaje_editar,
                       "tipos_recursos": tipos_recursos})

    return render(request, "procesos/mis_recursos.html",
                  {"proyecto": proyecto, "lista_recursos": lista_recursos, "tipos_recursos": tipos_recursos})


# Carga la vista de planificar proyecto y regista responsables para el proyecto
"""def planificar_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto_id)
    if request.method == 'POST':
        
        mensaje = responsable_controller.registrar_responsable(request.POST['nombre_responsable'], request.POST['descripcion_responsable'], proyecto_id)

        return render(request, "procesos/planificar.html", {'proyecto':proyecto, "mensaje":mensaje, "lista_responsables":lista_responsables})
    


    return render(request, "procesos/planificar.html", {'proyecto':proyecto, "lista_responsables":lista_responsables})
"""
"""
////////////////////////////////////////////////////////////////////////////
    METODOS PARA PLANIFICAR PROYECTO
/////////////////////////////////////////////////////////////////////////////
"""


def planificar_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto_id)
    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)
    if rbs_proyecto:
        # No vacía
        return render(request, "procesos/planificar.html",
                      {'proyecto': proyecto, 'rbs': True, 'rbs_proyecto': rp, 'rbs_sugerida': rs,
                       "lista_responsables": lista_responsables, "lista_roles": lista_roles, "impactos": impactos,
                       "probabilidades": probabilidades, "clasificacion_riesgo": clasificacion_riesgo})
    else:
        # Vacía
        return render(request, "procesos/planificar.html",
                      {'proyecto': proyecto, 'rbs_proyecto': rp, 'rbs_sugerida': rs,
                       "lista_responsables": lista_responsables, "lista_roles": lista_roles, "impactos": impactos,
                       "probabilidades": probabilidades, "clasificacion_riesgo": clasificacion_riesgo})

def planificar_proyecto_2(request, proyecto_id, mensaje):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto_id)
    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)
    if rbs_proyecto:
        # No vacía
        return render(
            request,
            "procesos/planificar.html",
            {'proyecto': proyecto,
             'rbs': True,
             'rbs_proyecto': rp,
             'rbs_sugerida': rs,
             "lista_responsables": lista_responsables,
             "lista_roles": lista_roles,
             "impactos": impactos,
             "probabilidades": probabilidades,
             "clasificacion_riesgo": clasificacion_riesgo,
             "mensaje":mensaje
             })
    else:
        # Vacía
        return render(request, "procesos/planificar.html",
                      {'proyecto': proyecto, 'rbs_proyecto': rp, 'rbs_sugerida': rs,
                       "lista_responsables": lista_responsables, "lista_roles": lista_roles, "impactos": impactos,
                       "probabilidades": probabilidades, "clasificacion_riesgo": clasificacion_riesgo, "mensaje":mensaje})


def registrar_responsable(request):
    proyecto_controller = ProyectoController()
    proyecto_id = request.POST['proyecto_id']
    proyecto = proyecto_controller.obtener_proyecto(request.POST['proyecto_id'])
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(request.POST['proyecto_id'])
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(request.POST['proyecto_id'])
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        mensaje = responsable_controller.registrar_responsable(request.POST['nombre_responsable'],
                                                               request.POST['descripcion_responsable'],
                                                               proyecto.proyecto_id, rol)

        return HttpResponseRedirect(reverse('planificar_proyecto_2', args=(proyecto_id, mensaje)))

    return planificar_proyecto(request, proyecto_id)


def editar_responsable(request):
    responsable_controller = ResponsableController()
    responsable = responsable_controller.obtener_responsable(request.POST['responsable_id'])
    proyecto_id = request.POST['proyecto_id_editar']
    lista_responsables = responsable_controller.listar_responsables(responsable.proyecto_id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(responsable.proyecto_id)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto.proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)

    if request.method == 'POST':
        rol = rol_controller.get_rol_by_id(request.POST['rol_id'])
        mensaje_editar = responsable_controller.editar_responsable(responsable, request.POST['responsable_nombre'],
                                                                   request.POST['responsable_descripcion'], rol)

        return render(request, "procesos/planificar.html",
                      dict(proyecto=proyecto,
                           rbs=True,
                           rbs_proyecto=rp,
                           rbs_sugerida=rs,
                           lista_responsables=lista_responsables,
                           mensaje_editar=mensaje_editar,
                           lista_roles=lista_roles,
                           impactos=impactos,
                           probabilidades=probabilidades,
                           clasificacion_riesgo=clasificacion_riesgo
                           )
                )

    return render(request, "procesos/planificar.html",
                  dict(
                      proyecto=proyecto,
                      rbs=True,
                      rbs_proyecto=rp,
                      rbs_sugerida=rs,
                      lista_responsables=lista_responsables,
                      lista_roles=lista_roles,
                      impactos=impactos,
                      probabilidades=probabilidades,
                      clasificacion_riesgo=clasificacion_riesgo
                  )
            )


def eliminar_responsable(request):
    responsable_controller = ResponsableController()
    responsable = responsable_controller.obtener_responsable(request.POST['responsable_id'])
    proyecto_id = request.POST['proyecto_id_el']
    lista_responsables = responsable_controller.listar_responsables(responsable.proyecto_id)
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(responsable.proyecto_id)
    rbs_controller = RbsController()
    rbs_sugerida = rbs_controller.obtener_rbs_sugerida(proyecto.sector.sector_id)
    rbs_proyecto = rbs_controller.obtener_rbs_proyecto(proyecto.proyecto_id)
    rp = dumps(rbs_proyecto)
    rs = dumps(rbs_sugerida)
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    gerente_controller = GerenteController()
    gerente = gerente_controller.obtener_gerente(request.user.id)
    rol_controller = RolController()
    lista_roles = rol_controller.listar_roles(gerente)

    impactos = proyecto_controller.obtener_impactos_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_by_proyecto_id(proyecto_id)
    clasificacion_riesgo = proyecto_controller.obtener_clasificaciones_riesgo_by_proyecto_id(proyecto_id)

    if request.method == 'POST':
        mensaje_eliminar = responsable_controller.eliminar_responsable(responsable)
        return HttpResponseRedirect(reverse('mi_proyecto', args=(proyecto_id,)))

    return HttpResponseRedirect(reverse('mi_proyecto', args=(proyecto_id,)))

def nuevo_responsable_riesgo(request, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    # Falta agregar de aqui para abajo
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = actividad_controller.listar_actividades_proyecto(proyecto_id)
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    actividades_riesgo = actividad_controller.listar_actividades_riesgo(proyecto_id)

    if request.method == 'POST':
        responsable = responsable_controller.obtener_responsable(request.POST['responsable_id'])
        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
        proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto.proyecto_id, riesgo.riesgo_id)

        mensaje = riesgo_controller.agregar_responsable_riesgo(proyecto_riesgo, responsable)
        #return render(request, "procesos/identificar_riesgos.html",{'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,"responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,"mensaje": mensaje})
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    #return render(request, "procesos/identificar_riesgos.html",{'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,"responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo})
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))

def eliminar_responsable_riesgo(request, proyecto_id):
    if request.method == 'POST':
        responsable_id = request.POST['responsable_id']
        riesgo_id = request.POST['riesgo_id']
        responsable_controller = ResponsableController()
        responsable_controller.eliminar_responsable_riesgo(responsable_id, riesgo_id, proyecto_id)


        # return render(request, "procesos/identificar_riesgos.html",{'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,"responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,"mensaje": mensaje})
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
        # return render(request, "procesos/identificar_riesgos.html",{'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,"responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo})
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


def nueva_actividad_riesgo(request, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    actividades_riesgo = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

    if request.method == 'POST':
        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
        proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto.proyecto_id, riesgo.riesgo_id)
        aux = actividad_controller.validar_actividad(proyecto_riesgo.proyecto_has_riesgo_id,
                                                     request.POST["actividad_id"])
        if aux == None:
            actividad = actividad_controller.obtener_actividad(request.POST["actividad_id"])
            mensaje = actividad_controller.registrar_actividad_riesgo(proyecto_riesgo, actividad)
            #return render(request, "procesos/identificar_riesgos.html",{'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,"responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,'respuestas_riesgo':respuestas_riesgo,"mensaje": mensaje})
            return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
        mensaje_editar = "Ya cuentas con esta actividad asignada al riesgo."
        #return render(request, "procesos/identificar_riesgos.html",{'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,"responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,'respuestas_riesgo':respuestas_riesgo,"mensaje_editar": mensaje_editar})
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    #return render(request, "procesos/identificar_riesgos.html",{'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,"responsables_riesgo": responsables_riesgo,'respuestas_riesgo':respuestas_riesgo, 'actividades_riesgo': actividades_riesgo})
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))

def actualizar_definiciones_riesgo(request, proyecto_id):
    if request.method == "POST":
        proyecto_controller = ProyectoController()
        definiciones = filtrar_definiciones(request)
        impactos = definiciones["impactos"]
        probabilidades = definiciones["probabilidades"]
        proyecto_controller.actualizar_impactos_by_proyecto_id(impactos, proyecto_id)
        proyecto_controller.actualizar_probabilidades_by_proyecto_id(probabilidades, proyecto_id)
    return planificar_proyecto(request, proyecto_id)


def filtrar_definiciones(request):
    impactos = []
    probabilidades = []
    for key, value in request.POST.items():
        if ('impacto_nombre_' in key):
            x = key.split("_")[2]
            impactos.append({
                "nombre": value,
                "valor": request.POST.get('impacto_valor_' + str(x))
            })
        elif ('propabilida_nombre_' in key):
            x = key.split("_")[2]
            probabilidades.append({
                "nombre": value,
                "valor": request.POST.get('propabilida_valor_' + str(x))
            })
    return {"impactos": impactos, "probabilidades": probabilidades}


def actualizar_clasificacion_riesgo(request, proyecto_id):
    if request.method == "POST":
        proyecto_controller = ProyectoController()
        clasificaciones = filtrar_clasificaciones(request)
        proyecto_controller.actualizar_clasificacion_riesgo_by_proyecto_id(clasificaciones, proyecto_id)
    return planificar_proyecto(request, proyecto_id)


def filtrar_clasificaciones(request):
    aux = []
    for key, value in request.POST.items():
        if 'clasificacion_nombre' in key:
            x = key.split("_")[2]
            aux.append({
                "nombre": value,
                "color": request.POST.get('clasificacion_color_' + str(x)),
                "valor_min": request.POST.get('clasificacion_min_' + str(x)),
                "valor_max": request.POST.get('clasificacion_max_' + str(x)),
            })
    return aux


"""
////////////////////////////////////////////////////////////////////////////
    METODOS PARA IDENTIFICAR RIESGOS DEL PROYECTO
/////////////////////////////////////////////////////////////////////////////
"""


def identificar_proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(proyecto_id=proyecto_id)
    rbs_controller = RbsController()
    rbs = rbs_controller.obtener_rbs_completa_by_proyecto(request.user.id, proyecto_id)
    rbsJSON = dumps(rbs)
    riesgo_controller = RiesgoController()
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)

    # Falta agregar de aqui para abajo
    responsable_controller = ResponsableController()
    lista_responsables = responsable_controller.listar_responsables(proyecto.proyecto_id)
    actividad_controller = ActividadController()
    lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))

    # Retorna responsables por riesgo de un proyecto
    responsables_riesgo = dumps(riesgo_controller.listar_responsables_riesgo(proyecto_id))
    # Retorna actividades por riesgo de un proyecto
    actividades_riesgo = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

    # (Funcion que retorna respuestas por riesgo de un proyecto (Revisar)!!!)
    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))

    lista_riesgos_sugeridos = riesgo_controller.get_riesgos_sugeridos(proyecto.sector, request.user.id)

    if (len(lista_riesgos_sugeridos) > 0):
        return render(request, "procesos/identificar_riesgos.html",
                      {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
                       'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                       "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
                       'lista_riesgos_sugeridos': lista_riesgos_sugeridos, 'respuestas_riesgo': respuestas_riesgo})

    return render(request, "procesos/identificar_riesgos.html",
                  {'proyecto': proyecto, 'rbs': rbsJSON, 'lista_riesgos': lista_riesgos,
                   'lista_responsables': lista_responsables, 'lista_actividades': lista_actividades,
                   "responsables_riesgo": responsables_riesgo, 'actividades_riesgo': actividades_riesgo,
                   'respuestas_riesgo': respuestas_riesgo})


def eliminar_actividad_proyecto(request, proyecto_id):
    data = get_data_render_identificar_riesgo(request.user.id, proyecto_id)
    if request.method == 'POST':
        actividad_controller = ActividadController()
        actividad = actividad_controller.desasociar_actividad_riesgo(proyecto_id, request.POST['riesgo_id_actividad'],
                                                                     request.POST['actividad_id_riesgo'])
        if (actividad):
            data["mensaje_eliminar"] = "Eliminado"
        #return render(request, "procesos/identificar_riesgos.html", data)
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    #return render(request, "procesos/identificar_riesgos.html", data)
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


def nueva_respuesta_identificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)



    if request.method == 'POST':
        # Valida que una respuesta no se llame igual en el mismo proyecto (No se si deberia ser asi)
        aux = respuesta_controller.validar_respuesta(request.POST["respuesta_nombre"], proyecto_id)
        if not aux:
            respuesta = respuesta_controller.registrar_respuesta(
                request.POST["respuesta_nombre"],
                request.POST["respuesta_descripcion"],
                request.POST["tipo_respuesta"]
            )
            riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
            mensaje_no = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)
            proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
            riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
            mensaje = respuesta_controller.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta,
                                                                        request.POST["tipo_respuesta"])

            respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
        return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))
    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))


def desasociar_respuesta_identificar(request, proyecto_id):
    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        riesgo_id = request.POST["riesgo_id_eliminar"]
        respuesta_id = request.POST['respuesta_id_eliminar']

        respuesta_controller.desasociar_respuesta_riesgo_by_proyecto(respuesta_id, riesgo_id, proyecto_id)

    return HttpResponseRedirect(reverse('identificar', args=(proyecto_id,)))




"""
////////////////////////////////////////////////////////////////////////////
    METODOS DE EVALUAR RIESGOS
/////////////////////////////////////////////////////////////////////////////
"""


def evaluar_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()

    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = dumps(riesgo_controller.get_riesgos_by_proyecto_2(proyecto))

    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))

    valores = dumps(get_valores_by_proyecto(proyecto_id))
    return render(request, "procesos/evaluar.html",
                  {'proyecto': proyecto, 'lista_riesgos': lista_riesgos, 'valores': valores, 'rangos': rangos})


def get_valores_by_proyecto(proyecto_id):
    proyecto_controller = ProyectoController()
    impactos = proyecto_controller.obtener_impactos_parseados_by_proyecto_id(proyecto_id)
    probabilidades = proyecto_controller.obtener_probabilidades_parseados_by_proyecto_id(proyecto_id)
    impactos.update(probabilidades)
    return impactos


def get_valores_by_proyecto_linea(proyecto_id, linea_base):
    proyecto_controller = ProyectoController()
    impactos = proyecto_controller.obtener_impactos_parseados_by_proyecto_id_linea(proyecto_id, linea_base)
    probabilidades = proyecto_controller.obtener_probabilidades_parseados_by_proyecto_id_linea(proyecto_id, linea_base)
    impactos.update(probabilidades)
    return impactos


def actualizar_valores(request, proyecto_id):
    if request.method == 'POST':
        proyecto_controller = ProyectoController()
        valores = json.loads(request.POST["valores"])
        # try:
        proyecto_controller.actualizar_valores_riesgo_proyecto(valores, proyecto_id)
        # except Exception as e:
        #    print(e)
        #   return HttpResponse(status=500)
        return HttpResponse(status=200)
    return HttpResponse(status=500)


"""
////////////////////////////////////////////////////////////////////////////
    METODOS DE PLANIFICAR RESPUESTAS
/////////////////////////////////////////////////////////////////////////////
"""


def get_data_planificar_respuesta(proyecto_id: int):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    actividad_controller=ActividadController()

    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)

    actividades_by_riesgos = dumps(actividad_controller.listar_actividades_riesgo(proyecto_id))

    # Listado de respuestas por riesgo, reutilizado de identificar
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    recurso_controller = RecursoController()
    # Recursos generales del proyecto
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    # Tareas por acciones por riesgo del proyecto
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    # Este metodo me lo invente para no tener que volver a consultar los los riesgos de un proyecto
    # Entre menos llamados a los metodos que hacen innerjoin mucho mejor
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))
    valores = dumps(get_valores_by_proyecto(proyecto_id))
    linea_base = crear_arreglo_linea_base(proyecto.proyecto_linea_base)

    actividad_controller = ActividadController()
    lista_actividades = dumps(actividad_controller.listar_actividades_proyecto(proyecto_id))

    return dict(
        proyecto=proyecto,
        lista_riesgos=lista_riesgos,
        respuestas_riesgo=respuestas_riesgo,
        lista_recursos=lista_recursos,
        lista_tareas=lista_tareas,
        respuestas_sugeridas=respuestas_sugeridas,
        riesgos_evaluados=riesgos_evaluados,
        rangos=rangos,
        valores=valores,
        linea_base=linea_base,
        actividades_by_riesgos=actividades_by_riesgos
    )


def crear_arreglo_linea_base(numero):
    aux = []
    for i in range(numero):
        aux.append(i + 1)

    return aux


def planificar_respuestas(request, proyecto_id):
    # proyecto = Proyecto.objects.using('base').get(proyecto_id=2, proyecto_linea_base=1)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base
    return render(
        request,
        "procesos/planificar_respuestas.html",
        get_data_planificar_respuesta(proyecto_id)
    )

def planificar_respuestas_2(request, proyecto_id, mensaje, mensaje_editar):
    # proyecto = Proyecto.objects.using('base').get(proyecto_id=2, proyecto_linea_base=1)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base)
    # proyecto = Proyecto.objects.get(proyecto_id=17)
    # print(proyecto.proyecto_nombre, proyecto.linea_base
    data = get_data_planificar_respuesta(proyecto_id)
    if mensaje_editar == 'NONE':
        data['mensaje'] = mensaje
    else:
        data['mensaje_editar'] = mensaje_editar
    return render(
        request,
        "procesos/planificar_respuestas.html",
        data
    )

def nueva_respuesta_planificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    data = get_data_planificar_respuesta(proyecto_id)

    if request.method == 'POST':
        # Valida que una respuesta no se llame igual en el mismo proyecto (No se si deberia ser asi)
        aux = respuesta_controller.validar_respuesta(request.POST["respuesta_nombre"], proyecto_id)
        if not aux:
            respuesta = respuesta_controller.registrar_respuesta(
                request.POST["respuesta_nombre"],
                request.POST["respuesta_descripcion"],
                request.POST["tipo_respuesta"]
            )
            riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
            mensaje_no = respuesta_controller.registrar_respuesta_riesgo(respuesta, riesgo)
            proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
            riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
            mensaje = respuesta_controller.registrar_respuesta_proyecto(proyecto_riesgo, riesgo_respuesta,
                                                                        request.POST["tipo_respuesta"])

            respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
            data['mensaje']=mensaje
            return render(
                request,
                "procesos/planificar_respuestas.html",
                data
            )
        data['mensaje_editar']="Ya cuentas con esta respuesta asociada al proyecto."
        return render(
            request,
            "procesos/planificar_respuestas.html",
            data
        )

    return render(
        request,
        "procesos/planificar_respuestas.html",
        data
    )


def asociar_respuesta_sugeridas(request, proyecto_id):
    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        riesgo_id = request.POST["riesgo_id_rta"]
        respuestas_id = filtrar_respuestas_id_from_request(request)

        respuestas = respuesta_controller.registrar_respuesta_sugeridas_riesgo(respuestas_id, riesgo_id, proyecto_id)

    return planificar_respuestas(request, proyecto_id)


def editar_respuesta_planificar(request, proyecto_id):
    if request.method == 'POST':
        riesgo_controller = RiesgoController()
        respuesta_controller = RespuestaController()
        respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id"])
        riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
        mensaje_editar = respuesta_controller.editar_respuesta(respuesta, request.POST["respuesta_nombre"],
                                                               request.POST["respuesta_descripcion"])
        proyecto_riesgo = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, riesgo.riesgo_id)
        riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
        respuesta_proyecto = respuesta_controller.get_riesgo_respuesta_by_id(proyecto_riesgo, riesgo_respuesta)
        print(respuesta_proyecto)
        mensaje_editar = respuesta_controller.actualizar_tipo_respuesta(respuesta_proyecto,
                                                                        request.POST["tipo_respuesta"])
    return planificar_respuestas(request, proyecto_id)


def desasociar_respuesta_riesgo(request, proyecto_id):
    if request.method == 'POST':
        respuesta_controller = RespuestaController()

        riesgo_id = request.POST["riesgo_id_eliminar"]
        respuesta_id = request.POST['respuesta_id_eliminar']

        respuesta_controller.desasociar_respuesta_riesgo_by_proyecto(respuesta_id, riesgo_id, proyecto_id)

    return planificar_respuestas(request, proyecto_id)


def filtrar_respuestas_id_from_request(request):
    aux = []
    for key, value in request.POST.items():
        if 'respuesta_sugerida_' in key:
            aux.append(value)
    return aux


def nueva_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))
    valores = dumps(get_valores_by_proyecto(proyecto_id))
    if request.method == 'POST':
        # Todavia no esta validado, me falta hacer pruebas cuando tenga el parseo de fecha de diego
        aux = tarea_controller.validar_tarea(request.POST["tarea_nombre"], request.POST["respuesta_id"])
        if not aux:
            riesgo_proyecto = riesgo_controller.get_riesgo_by_proyecto(proyecto_id, request.POST["riesgo_id"])
            riesgo = riesgo_controller.obtener_riesgo(request.POST["riesgo_id"])
            respuesta = respuesta_controller.obtener_respuesta(request.POST["respuesta_id"])
            riesgo_respuesta = respuesta_controller.obtener_respuesta_riesgo(riesgo.riesgo_id, respuesta.respuesta_id)
            proyecto_riesgo_respuesta = respuesta_controller.get_riesgo_respuesta_by_id(riesgo_proyecto,
                                                                                        riesgo_respuesta)

            tarea = tarea_controller.registrar_tarea(
                proyecto_riesgo_respuesta,
                request.POST["tarea_nombre"],
                request.POST["tarea_descripcion"],
                request.POST["tarea_fecha_inicio"],
                request.POST["tarea_fecha_fin"],
                request.POST["tarea_fecha_inicio"],
                request.POST["tarea_fecha_fin"]
            )
            fecha_ini = datetime.datetime.strptime(request.POST["tarea_fecha_inicio"], '%Y-%m-%d')
            fecha_final = datetime.datetime.strptime(request.POST["tarea_fecha_fin"], '%Y-%m-%d')
            semanas = abs((fecha_ini - fecha_final).days) / 7
            dias = abs((fecha_ini - fecha_final).days) #perdoname niñita
            tarea.duracion = dias
            tarea.save()
            lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
            if tarea == None:
                mensaje_editar = "No se pudo registrar la tarea."
                return HttpResponseRedirect(reverse('planificar_respuestas_2', args=(proyecto_id,'', mensaje_editar)))
            else:
                mensaje = "Nueva tarea registrada."
                return HttpResponseRedirect(reverse('planificar_respuestas_2', args=(proyecto_id,mensaje, 'NONE')))
        return HttpResponseRedirect(reverse('planificar_respuestas_2', args=(proyecto_id, '', "La tarea ya se encuentra asociada a la respuesta.")))
    return HttpResponseRedirect(reverse('planificar_respuestas', args=(proyecto_id,)))

def eliminar_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))
    valores = dumps(get_valores_by_proyecto(proyecto_id))
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    if request.method == 'POST':
        tarea = tarea_controller.get_tarea_by_id(request.POST["tarea_id"])
        mensaje_eliminar = tarea_controller.eliminar_tarea(tarea)
        lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
        return render(
            request,
            "procesos/planificar_respuestas.html",
            dict(
                proyecto=proyecto,
                lista_riesgos=lista_riesgos,
                respuestas_riesgo=respuestas_riesgo,
                lista_recursos=lista_recursos,
                lista_tareas=lista_tareas,
                respuestas_sugeridas=respuestas_sugeridas,
                riesgos_evaluados=riesgos_evaluados,
                rangos=rangos,
                valores=valores,
                mensaje_eliminar=mensaje_eliminar
            )
        )

    return render(
        request,
        "procesos/planificar_respuestas.html",
        dict(
            proyecto=proyecto,
            lista_riesgos=lista_riesgos,
            respuestas_riesgo=respuestas_riesgo,
            lista_recursos=lista_recursos,
            lista_tareas=lista_tareas,
            respuestas_sugeridas=respuestas_sugeridas,
            riesgos_evaluados=riesgos_evaluados,
            rangos=rangos,
            valores=valores
        )
    )


def editar_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto(proyecto)
    recurso_controller = RecursoController()
    lista_recursos = recurso_controller.listar_recursos(proyecto_id)
    tarea_controller = TareaController()
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
    respuestas_sugeridas = dumps(respuesta_controller.obtener_respuestas_sugeridas(proyecto_id))
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id(lista_riesgos, proyecto_id))
    rangos = dumps(proyecto_controller.obtener_rangos_parseados_by_proyecto_id(proyecto_id))
    valores = dumps(get_valores_by_proyecto(proyecto_id))

    if request.method == 'POST':
        tarea = tarea_controller.get_tarea_by_id(request.POST["tarea_id"])
        tarea_editada = tarea_controller.editar_tarea(tarea, request.POST["tarea_nombre"],
                                                      request.POST["descripcion_tarea"],
                                                      request.POST["tarea_fecha_inicio"],
                                                      request.POST["tarea_fecha_fin"])

        fecha_ini = datetime.datetime.strptime(request.POST["tarea_fecha_inicio"], '%Y-%m-%d')
        fecha_final = datetime.datetime.strptime(request.POST["tarea_fecha_fin"], '%Y-%m-%d')
        semanas = abs((fecha_ini - fecha_final).days) / 7
        tarea_editada.duracion = semanas
        tarea_editada.save()
        mensaje_editar = "Se actualizó la tarea exitosamente."
        lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))

        return render(
            request,
            "procesos/planificar_respuestas.html",
            dict(
                proyecto=proyecto,
                lista_riesgos=lista_riesgos,
                respuestas_riesgo=respuestas_riesgo,
                lista_recursos=lista_recursos,
                lista_tareas=lista_tareas,
                respuestas_sugeridas=respuestas_sugeridas,
                riesgos_evaluados=riesgos_evaluados,
                rangos=rangos,
                valores=valores,
                mensaje_editar=mensaje_editar
            )
        )

    return render(
        request,
        "procesos/planificar_respuestas.html",
        dict(
            proyecto=proyecto,
            lista_riesgos=lista_riesgos,
            respuestas_riesgo=respuestas_riesgo,
            lista_recursos=lista_recursos,
            lista_tareas=lista_tareas,
            respuestas_sugeridas=respuestas_sugeridas,
            riesgos_evaluados=riesgos_evaluados,
            rangos=rangos,
            valores=valores
        )
    )


def nuevo_recurso_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    recurso_controller = RecursoController()
    data = get_data_planificar_respuesta(proyecto_id)
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    if request.method == 'POST':
        tarea_controller = TareaController()
        respuesta_controller = RespuestaController()
        tarea = tarea_controller.get_tarea_by_id(request.POST["tarea_id"])
        recurso = recurso_controller.obtener_recurso(request.POST["recurso_id"])

        aux = tarea_controller.get_recurso_tarea_by_id(tarea, recurso)

        if aux is None:
            mensaje = tarea_controller.agregar_recurso_tarea(tarea, recurso, request.POST["recurso_cantidad"])
            data['mensaje'] = mensaje
        else:
            mensaje_editar = "Ya cuentas con este recurso asignado a la tarea."
            data['mensaje_editar'] = mensaje_editar

        data["respuestas_riesgo"] = dumps(respuesta_controller.listar_riesgos_respuesta(proyecto_id))
        data["lista_tareas"] = dumps(tarea_controller.listar_tareas_group_by_riesgo(proyecto))
        data["lista_recursos"] = recurso_controller.listar_recursos(proyecto_id)

    return render(
        request,
        "procesos/planificar_respuestas.html",
        data
    )


def desvincular_recurso_tarea(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    recurso_controller = RecursoController()
    tarea_controller = TareaController()
    data = get_data_planificar_respuesta(proyecto_id)

    if request.method == 'POST':
        tarea_id = request.POST["tarea_id"]
        recurso_id = request.POST["recurso_id"]
        # tarea_recurso = tarea_controller.get_recurso_tarea_by_id(tarea, recurso)
        mensaje_eliminar = tarea_controller.eliminar_recurso_tarea_2(recurso_id, tarea_id)
        data = get_data_planificar_respuesta(proyecto_id)
        data['lista_recursos'] = recurso_controller.listar_recursos(proyecto_id)
        data['mensaje_eliminar'] = mensaje_eliminar

    return render(
        request,
        "procesos/planificar_respuestas.html",
        data
    )


def linea_base(request, proyecto_id, numero_linea):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    lista_riesgos = riesgo_controller.get_riesgos_by_proyecto_linea(proyecto, numero_linea)  # En teoria ya
    # Listado de respuestas por riesgo, reutilizado de identificar
    respuestas_riesgo = dumps(
        respuesta_controller.listar_riesgos_respuesta_linea(proyecto_id, numero_linea))  # En teoria ya
    recurso_controller = RecursoController()
    # Recursos generales del proyecto
    lista_recursos = recurso_controller.listar_recursos_linea(proyecto_id, numero_linea)  # En teoria ya
    tarea_controller = TareaController()
    # Tareas por acciones por riesgo del proyecto
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo_linea(proyecto, numero_linea))  # En teoria ya
    # Este metodo me lo invente para no tener que volver a consultar los los riesgos de un proyecto
    # Entre menos llamados a los metodos que hacen innerjoin mucho mejor
    riesgos_evaluados = dumps(riesgo_controller.evaluar_riesgos_by_proyecto_id_linea(lista_riesgos, proyecto_id,
                                                                                     numero_linea))  # En teoria ya
    rangos = dumps(
        proyecto_controller.obtener_rangos_parseados_by_proyecto_id_linea(proyecto_id, numero_linea))  # En teoria ya
    valores = dumps(get_valores_by_proyecto_linea(proyecto_id, numero_linea))  # Este
    linea_base = crear_arreglo_linea_base(proyecto.proyecto_linea_base)
    data = dict(
        proyecto=proyecto,
        lista_riesgos=lista_riesgos,
        respuestas_riesgo=respuestas_riesgo,
        lista_recursos=lista_recursos,
        lista_tareas=lista_tareas,
        riesgos_evaluados=riesgos_evaluados,
        rangos=rangos,
        valores=valores,
        linea_base=linea_base,
        numero_linea=numero_linea
    )

    return render(
        request,
        "procesos/linea_base.html",
        data
    )


"""
////////////////////////////////////////////////////////////////////////////
    METODOS CONTROLAR RIESGOS
/////////////////////////////////////////////////////////////////////////////
"""


@login_required(login_url='/accounts/login/')
def controlar_riesgos(request, proyecto_id):
    proyecto_controller = ProyectoController()
    riesgo_controller = RiesgoController()
    respuesta_controller = RespuestaController()
    tarea_controller = TareaController()

    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    respuestas_riesgo = dumps(respuesta_controller.listar_riesgos_respuesta_base(proyecto_id))
    lista_tareas = dumps(tarea_controller.listar_tareas_group_by_riesgo_base(proyecto))


    return render(
        request,
        "procesos/controlar_riesgos.html",
        dict(
            proyecto=proyecto,
            respuestas_riesgo=respuestas_riesgo,
            lista_tareas=lista_tareas
        )
    )


def crear_linea_base(request, proyecto_id):
    proyecto_controller = ProyectoController()
    gerente_id = request.user.id
    rta = proyecto_controller.crear_linea_base(gerente_id, proyecto_id)
    if rta:
        return HttpResponse({'rta': rta}, status=200)
    else:
        return HttpResponse({'rta': rta}, status=500)


def actualizar_gantt(request, proyecto_id):
    proyecto_controller = ProyectoController()
    gantt = json.loads(request.POST['gantt'])
    rta = proyecto_controller.actualizar_gantt(proyecto_id, gantt)
    if rta:
        return HttpResponse({'rta': rta}, status=200)
    else:
        return HttpResponse({'rta': rta}, status=500)


"""
////////////////////////////////////////////////////////////////////////////
    METODOS CERRAR PROYECTO
/////////////////////////////////////////////////////////////////////////////
"""


def cerrar_proyecto(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    leccion_controller = LeccionController()
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)
    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones

    )

    if request.method == 'POST':
        fecha_actual = datetime.datetime.now()
        aux = proyecto_controller.cerrar_proyecto(proyecto, fecha_actual)
        data['mensaje_eliminar'] = "Se ha finalizado la gestión de riesgos de forma exitosa."

    return render(
        request,
        "procesos/cerrar_proyecto.html", data
    )


def registrar_leccion(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    leccion_controller = LeccionController()
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)

    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones
    )

    if request.method == 'POST':

        leccion = leccion_controller.registrar_leccion(proyecto, request.POST["descripcion_leccion"])
        return HttpResponseRedirect(reverse('cerrar_proyecto', args=(proyecto_id,)))
        """if leccion == True:
            data['mensaje'] = "lección aprendida registrada exitosamente."
            return render(request, "procesos/cerrar_proyecto.html", data)

        data['mensaje_editar'] = "No se pudo registrar la lección aprendida."
        return render(
            request,
            "procesos/cerrar_proyecto.html", data
        )"""
    return HttpResponseRedirect(reverse('cerrar_proyecto', args=(proyecto_id,)))
    """return render(
        request,
        "procesos/cerrar_proyecto.html", data
    )"""


def eliminar_leccion(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    leccion_controller = LeccionController()
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)

    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones
    )

    if request.method == 'POST':

        leccion = leccion_controller.get_leccion_by_id(request.POST["leccion_id"])
        if leccion != None:
            data['mensaje_eliminar'] = leccion_controller.eliminar_leccion(leccion)
            return render(
                request,
                "procesos/cerrar_proyecto.html", data
            )

        data['mensaje_editar'] = "Esta lección ya ha sido eliminada."
        return render(
            request,
            "procesos/cerrar_proyecto.html", data
        )

    return render(
        request,
        "procesos/cerrar_proyecto.html", data
    )


def editar_leccion(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)
    tarea_controller = TareaController()
    tareas = tarea_controller.listar_tareas_no_iniciadas(proyecto)
    leccion_controller = LeccionController()
    lista_lecciones = leccion_controller.listar_lecciones(proyecto)

    data = dict(
        proyecto=proyecto,
        tareas_no_iniciadas=tareas,
        lista_lecciones=lista_lecciones
    )

    if request.method == 'POST':

        leccion = leccion_controller.get_leccion_by_id(request.POST["leccion_id"])
        if leccion != None:
            data['mensaje_editar'] = leccion_controller.editar_leccion(leccion, request.POST["descripcion_leccion"])
            return render(
                request,
                "procesos/cerrar_proyecto.html", data
            )

        data['mensaje_editar'] = "No se ha encontrado la lección que se intenta editar."
        return render(
            request,
            "procesos/cerrar_proyecto.html", data
        )

    return render(
        request,
        "procesos/cerrar_proyecto.html", data
    )


def gantt(request):
    return render(
        request,
        "procesos/gantt.html",
    )


"""
////////////////////////////////////////////////////////////////////////////
    METODOS DE INFORMES
/////////////////////////////////////////////////////////////////////////////
"""


def generar_informe_identificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_identificar(proyecto)

    zip_file = open(reporte, 'rb')
    t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(zip_file, content_type=t)
    response['Content-Disposition'] = 'attachment; filename="%s"' % reporte
    if os.path.exists("demofile.txt"):
        os.remove("demofile.txt")
    else:
        print("The file does not exist")
    return response


def generar_informe_planificar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_planificar(proyecto)

    zip_file = open(reporte, 'rb')
    t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(zip_file, content_type=t)
    response['Content-Disposition'] = 'attachment; filename="%s"' % reporte
    if os.path.exists("demofile.txt"):
        os.remove("demofile.txt")
    else:
        print("The file does not exist")
    return response


def generar_informe_evaluar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_evaluar(proyecto)

    zip_file = open(reporte, 'rb')
    t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(zip_file, content_type=t)
    response['Content-Disposition'] = 'attachment; filename="%s"' % reporte
    if os.path.exists("demofile.txt"):
        os.remove("demofile.txt")
    else:
        print("The file does not exist")
    return response


def generar_informe_planificar_respuesta(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_planificar_respuesta(proyecto)

    zip_file = open(reporte, 'rb')
    t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(zip_file, content_type=t)
    response['Content-Disposition'] = 'attachment; filename="%s"' % reporte

    if os.path.exists(reporte):
        os.remove(reporte)
    else:
        print("The file does not exist", reporte)
    return response


def generar_informe_controlar(request, proyecto_id):
    proyecto_controller = ProyectoController()
    proyecto = proyecto_controller.obtener_proyecto(proyecto_id)

    reporte_controller = ReporteController()
    reporte = reporte_controller.generar_reporte_controlar_riesgos(proyecto)

    zip_file = open(reporte, 'rb')
    t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(zip_file, content_type=t)
    response['Content-Disposition'] = 'attachment; filename="%s"' % reporte

    if os.path.exists(reporte):
        os.remove(reporte)
    else:
        print("The file does not exist", reporte)
    return response


"""
////////////////////////////////////////////////////////////////////////////
    METODO PARA GENERAR REPORTES EN EXCEL
/////////////////////////////////////////////////////////////////////////////
"""

"""class ExampleViewSet(APIView):

    def get(self, request, format=None):
        ur = 'C:\\Users\\DiegoCV\\Documents\\tesis\\tesis\\codigo\\ufps_risk_api\\app_risk_api\\modulos\\servicios_generales\\test.xlsx'
        zip_file = open(ur, 'rb')
        print(zip_file)
        t = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(zip_file, content_type=t)
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'CDX_COMPOSITES_20140626.xlsx'

        return response"""


def mi_pass(request):
    return render(
        request,
        "registration/password_reset_form.html")


#######################################
## METODOS UTIL
#######################################
def get_fecha_actual():
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    return date_time
