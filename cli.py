#!/usr/bin/env python3
# Interfaz en línea de comandos para la gestión de proyectos
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-07-01
# Cambios:
#   v1
#     * Versión inicial

from proyectos import *
from colecciones import *
from consola import *
import utilidades as util


contextos = Contextos()
contextos.agregar("proyectos", {})
contextos.agregar("tareas", {})
contextos.agregar("subtareas", {})
gestor = Gestor()

# Tomado del constructor de Empresa en proyectos.py.  Mantener sincronizado
nombres_argumentos_empresa = (
    "nombre", "descripcion", "fecha_creacion", "direccion",
    "telefono", "correo", "gerente", "equipo_contacto" )
mensajes_argumentos_empresa = (
    "Nombre de la empresa: ",
    "Descripción de la empresa: ",
    "Fecha de creación de la empresa (dd/mm/yyyy): ",
    "Dirección de la empresa (en una línea): ",
    "Número de teléfono de la empresa (sin espacios ni guiones): ",
    "Dirección de correo electrónico de la empresa: ",
    "Nombre del gerente de la empresa: ",
    "Nombre del equipo de contacto de la empresa: " )

# Tomado del constructor de Proyecto en proyectos.py.  Mantener sincronizado
nombres_argumentos_proyecto = (
    "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
    "estado", "empresa", "gerente", "equipo" )
mensajes_argumentos_proyecto = (
    "Nombre del proyecto: ",
    "Descripción del proyecto: ",
    "Fecha de inicio del proyecto (dd/mm/yyyy): ",
    "Fecha de vencimiento del proyecto (dd/mm/yyyy): ",
    "Estado actual del proyecto (No iniciado, Detenido, En progreso, Completado): ",
    "Nombre de la empresa del proyecto: ",
    "Nombre del gerente del proyecto: ",
    "Nombre del equipo del proyecto: " )

# Tomado del constructor de Tarea en proyectos.py.  Mantener sincronizado
nombres_argumentos_tarea = (
    "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
    "estado", "porcentaje", "empresa_cliente" )
mensajes_argumentos_tarea = (
    "Nombre de la tarea: ",
    "Descripción de la tarea: ",
    "Fecha de inicio de la tarea (dd/mm/yyyy): ",
    "Fecha de vencimiento de la tarea (dd/mm/yyyy): ",
    "Estado actual de la tarea (No iniciado, Detenido, En progreso, Completado): ",
    "Porcentaje de progreso de la tarea (de 0.00 a 100.00): ",
    "Nombre de la empresa cliente a la que va dirigida la tarea: " )

ESTADOS_VALIDOS = ["No iniciado", "Detenido", "En progreso", "Completado"]

def leer_id(consola, mensaje):
    "Solicita un ID al usuario."
    " Devuelve un resultado de error si aplica."
    id_ = consola.leer_argumentos( ("id",),
        (mensaje,) )["id"]
    try:
        id_ = int(id_)
    except ValueError:
        return Resultado("Error: el dato ingresado no es un ID válido: "
                         + id_, None, tipo_error="Valor")
    return id_

_MSG_ERROR_EMPRESA_NO_ID = ("Error: "
                            + Gestor._MSG_ERROR_EMPRESA_NO_ID[0].lower()
                            + Gestor._MSG_ERROR_EMPRESA_NO_ID[1:] )
_MSG_ERROR_PROYECTO_NO_ID = ("Error: "
                             + Gestor._MSG_ERROR_PROYECTO_NO_ID[0].lower()
                             + Gestor._MSG_ERROR_PROYECTO_NO_ID[1:] )

def id_a_empresa(consola, mensaje):
    "Solicita un ID de empresa al usuario."
    " Devuelve un resultado de error si aplica."
    id_empresa = leer_id(consola, mensaje)
    if isinstance(id_empresa, Resultado): return id_empresa
    empresa = gestor.buscar_empresa("id", id_empresa)
    if empresa is None:
        return Resultado(_MSG_ERROR_EMPRESA_NO_ID + str(id_empresa),
                         None, tipo_error="Valor")
    return empresa

def id_a_proyecto(consola, mensaje):
    "Solicita un ID de proyecto al usuario."
    " Devuelve un resultado de error si aplica."
    id_proyecto = leer_id(consola, mensaje)
    if isinstance(id_proyecto, Resultado): return id_proyecto
    proyecto = gestor.empresa.buscar_proyecto_por_id(id_proyecto)
    if proyecto is None:
        return Resultado(_MSG_ERROR_PROYECTO_NO_ID + str(id_proyecto),
                         None, tipo_error="Valor")
    return proyecto

def id_a_tarea(consola, mensaje):
    "Solicita un ID de tarea al usuario."
    " Devuelve un resultado de error si aplica."
    id_tarea = leer_id(consola, mensaje)
    if isinstance(id_tarea, Resultado): return id_tarea
    tarea = gestor.buscar_tarea("id", id_tarea)
    if tarea is None:
        if len(gestor.tareas) == 0:
            mensaje = "Error: no existe una tarea en este proyecto con ese ID: "
        else:
            mensaje = "Error: no existe una subtarea en esta tarea con ese ID: "
        return Resultado(mensaje + str(id_tarea), None, tipo_error="Valor")
    return tarea

def leer_fecha(argumentos, nombre):
    "Interpreta una fecha desde los argumentos de línea de comandos."
    " Devuelve un resultado de error si aplica."
    try:
        argumentos[nombre] = util.str_a_fecha(argumentos[nombre])
    except ValueError as e:
        return Resultado("Error: '%s' no es una fecha válida: %s"
                         % (nombre, argumentos[nombre]),
                         None, tipo_error="Valor" )
    return None

_traduccion_telefono = str.maketrans("", "", " -")
_max_telefono = 19999999999999

def leer_telefono(argumentos, nombre):
    original = argumentos[nombre]
    try:
        argumentos[nombre] = int(original.translate(_traduccion_telefono))
        if argumentos[nombre] > _max_telefono:
            raise ValueError("")
    except ValueError:
        return Resultado("Error: '%s' no es un número de teléfono válido: %s"
                         % (nombre, original),
                         None, tipo_error="Valor" )
    return None

def leer_porcentaje(argumentos, nombre):
    try:
        porcentaje = argumentos[nombre]
        if porcentaje[-1] == "%":
            porcentaje = porcentaje[:-1]
        argumentos[nombre] = util.a_float(porcentaje)
    except ValueError:
        return Resultado("Error: '%s' no es un porcentaje válido: %s"
                         % (nombre, argumentos[nombre]),
                         None, tipo_error="Valor" )
    return None

# Plantilla para función de cambio de contexto
# Recomendaciones:
#   * Cambiar el nombre
#   * Cambiar la cadena de documentación que está debajo del nombre
#   * Cambiar el nombre del contexto
##def fn_cambiar_contexto(consola, linea_comando):
##    "Regresa al menú principal"
##    consola.cambiar_contexto("principal")
##    consola.ayuda()
##    return Resultado("", fn_regresar)
def macro_regresar(consola, linea_comando, contexto, funcion):
    try:
        gestor.regresar()
    except RuntimeError as e:  # No debería pasar
        return Resultado("Error: " + e.args[0], funcion)
    consola.cambiar_contexto(contexto)
    consola.ayuda()
    return Resultado("", funcion)


def fn_agregar_empresa(consola, linea_comando):
    "Añade una nueva empresa"
    print("Ingrese la siguiente información requerida.")
    argumentos = consola.leer_argumentos(nombres_argumentos_empresa,
                                         mensajes_argumentos_empresa)
    res = leer_fecha(argumentos, "fecha_creacion")
    if isinstance(res, Resultado):  # Resultado de error
        res.origen = fn_agregar_empresa
        return res
    res = leer_telefono(argumentos, "telefono")
    if isinstance(res, Resultado):
        res.origen = fn_agregar_empresa
        return res

    try:
        empresa = gestor.agregar_empresa(argumentos)
    except ValueError as e:
        return Resultado("Error: " + e.args[0], fn_agregar_empresa,
                         tipo_error="Valor")
    return Resultado("La empresa ha sido creada, su ID es " + str(empresa.id),
                     fn_agregar_empresa)
contextos["principal"]["agregar"] = Comando(fn_agregar_empresa, "agregar")

def fn_enumerar_empresas(consola, linea_comando):
    "Enumera las empresas registradas"
    if len(gestor.empresas) == 0:
        return Resultado("No hay empresas para mostrar.", fn_enumerar_empresas)
    resultado = "\n\n".join(map(str, gestor.empresas))
    return Resultado(resultado, fn_enumerar_empresas)
contextos["principal"]["mostrar"] = Comando(fn_enumerar_empresas, "mostrar")

def fn_consultar_empresas(consola, linea_comando):
    "Consulta una empresa existente"
    empresa = id_a_empresa(
        consola, "Ingrese el ID de la empresa que desea consultar: ")
    if isinstance(empresa, Resultado):  # Resultado de error
        empresa.origen = fn_consultar_empresas
        return empresa

    return Resultado(format(empresa, "g"), fn_consultar_empresas)
contextos["principal"]["consultar"] = \
    Comando(fn_consultar_empresas, "consultar [id]")

def fn_modificar_empresa(consola, linea_comando):
    "Modifica una empresa existente"
    empresa = id_a_empresa(
        consola, "Ingrese el ID de la empresa que desea modificar: ")
    if isinstance(empresa, Resultado):  # Resultado de error
        empresa.origen = fn_modificar_empresa
        return empresa
    print(format(empresa, "g"))

    print("\nPara mantener una propiedad de la empresa intacta"
          " solo presione 'Enter'")
    argumentos = consola.leer_argumentos(nombres_argumentos_empresa,
                                         mensajes_argumentos_empresa)
    if argumentos["fecha_creacion"] != "":
        res = leer_fecha(argumentos, "fecha_creacion")
        if isinstance(res, Resultado):
            res.origen = fn_modificar_empresa
            return res
    if argumentos["telefono"] != "":
        res = leer_telefono(argumentos, "telefono")
        if isinstance(res, Resultado):
            res.origen = fn_modificar_empresa
            return res

    for nombre, valor in list(argumentos.items()):
        if valor == "":
            argumentos.pop(nombre)
    try:
        gestor.modificar_empresa(argumentos, empresa)
    except ValueError as e:
        return Resultado("Error: " + e.args[0], fn_modificar_empresa,
                         tipo_error="Valor")
    return Resultado("Empresa modificada exitosamente.", fn_modificar_empresa)
contextos["principal"]["modificar"] = Comando(fn_modificar_empresa, "modificar")

def fn_eliminar_empresa(consola, linea_comando):
    "Elimina una empresa"
    empresa = id_a_empresa(
        consola, "Ingrese el ID de la empresa que desea eliminar: ")
    if isinstance(empresa, Resultado):  # Resultado de error
        empresa.origen = fn_eliminar_empresa
        return empresa

    print(empresa)
    if consola.confirmar("Está seguro que desea eliminar esta empresa?"):
        gestor.eliminar_empresa(empresa)
        return Resultado(
            "La empresa con ID %d ha sido eliminada." % empresa.id,
            fn_eliminar_empresa)
    return Resultado("", fn_eliminar_empresa)
contextos["principal"]["eliminar"] = \
    Comando(fn_eliminar_empresa, "eliminar [id]")


def fn_proyectos(consola, linea_comando):
    "Cambia al menú de proyectos"
    if len(gestor.empresas) == 0:
        return Resultado("Error: debe crear al menos una empresa antes"
                         " de ingresar en el menú de proyectos", fn_proyectos)
    empresa = id_a_empresa(
        consola, "Ingrese el ID de la empresa cuyos proyectos desea gestionar: ")
    if isinstance(empresa, Resultado):  # Resultado de error
        empresa.origen = fn_proyectos
        return empresa

    gestor.gestionar_proyectos(empresa)
    consola.cambiar_contexto("proyectos")
    consola.ayuda()
    return Resultado("", fn_proyectos)
contextos["principal"]["proyectos"] = Comando(fn_proyectos, "proyectos [id]")
# Recordar añadir regresar al final de las secciones

def fn_agregar_proyecto(consola, linea_comando):
    "Añade un nuevo proyecto"
    print("Ingrese la siguiente información requerida.")
    argumentos = consola.leer_argumentos(nombres_argumentos_proyecto,
                                         mensajes_argumentos_proyecto)
    for nombre in ("fecha_inicio", "fecha_vencimiento"):
        res = leer_fecha(argumentos, nombre)
        if isinstance(res, Resultado):  # Resultado de error
            res.origen = fn_agregar_proyecto
            return res

    try:
        proyecto = gestor.agregar_proyecto(argumentos)
    except ValueError as e:
        return Resultado("Error: " + e.args[0], fn_agregar_proyecto,
                         tipo_error="Valor")
    return Resultado("El proyecto ha sido creado, su ID es " + str(proyecto.id),
                     fn_agregar_proyecto)
contextos["proyectos"]["agregar"] = Comando(fn_agregar_proyecto, "agregar")

def fn_enumerar_proyectos(consola, linea_comando):
    "Enumera los proyectos registrados"
    if len(gestor.empresa.proyectos) == 0:
        return Resultado("No hay proyectos para mostrar.", fn_enumerar_proyectos)
    resultado = "\n\n".join(map(str,
        (par.valor for par in gestor.empresa.proyectos) ))
    return Resultado(resultado, fn_enumerar_proyectos)
contextos["proyectos"]["mostrar"] = Comando(fn_enumerar_proyectos, "mostrar")

def fn_consultar_proyecto(consola, linea_comando):
    "Consulta un proyecto existente"
    proyecto = id_a_proyecto(
        consola, "Ingrese el ID del proyecto que desea consultar: ")
    if isinstance(proyecto, Resultado):  # Resultado de error
        proyecto.origen = fn_consultar_proyecto
        return proyecto

    return Resultado(format(proyecto, "g"), fn_consultar_proyecto)
contextos["proyectos"]["consultar"] = \
    Comando(fn_consultar_proyecto, "consultar [id]")

def fn_modificar_proyecto(consola, linea_comando):
    "Modifica un proyecto existente"
    proyecto = id_a_proyecto(
        consola, "Ingrese el ID del proyecto que desea modificar: ")
    if isinstance(proyecto, Resultado):  # Resultado de error
        proyecto.origen = fn_modificar_proyecto
        return proyecto
    print(format(proyecto, "g"))
    
    print("\nPara mantener una propiedad del proyecto intacta"
          " solo presione 'Enter'")
    argumentos = consola.leer_argumentos(nombres_argumentos_proyecto,
                                         mensajes_argumentos_proyecto)
    for nombre in ("fecha_inicio", "fecha_vencimiento"):
        if argumentos[nombre] != "":
            res = leer_fecha(argumentos, nombre)
            if isinstance(res, Resultado):
                res.origen = fn_modificar_proyecto
                return res

    for nombre, valor in list(argumentos.items()):
        if valor == "":
            argumentos.pop(nombre)
    try:
        gestor.modificar_proyecto(argumentos, proyecto)
    except ValueError as e:
        return Resultado("Error: " + e.args[0], fn_modificar_proyecto,
                         tipo_error="Valor")
    return Resultado("Proyecto modificado exitosamente.", fn_modificar_proyecto)
contextos["proyectos"]["modificar"] = Comando(fn_modificar_proyecto, "modificar")

def fn_eliminar_proyecto(consola, linea_comando):
    "Elimina un proyecto"
    proyecto = id_a_proyecto(
        consola, "Ingrese el ID del proyecto que desea eliminar: ")
    if isinstance(proyecto, Resultado):  # Resultado de error
        proyecto.origen = fn_eliminar_proyecto
        return proyecto

    print(proyecto)
    if consola.confirmar("Está seguro que desea eliminar este proyecto?"):
        gestor.eliminar_proyecto(proyecto)
        return Resultado(
            "El proyecto con ID %d ha sido eliminado." % proyecto.id,
            fn_eliminar_proyecto)
    return Resultado("", fn_eliminar_proyecto)
contextos["proyectos"]["eliminar"] = \
    Comando(fn_eliminar_proyecto, "eliminar [id]")


def fn_tareas(consola, linea_comando):
    "Gestiona las tareas de un proyecto"
    if len(gestor.empresa.proyectos) == 0:
        return Resultado("Error: debe crear al menos un proyecto antes"
                         " de ingresar en el menú de tareas", fn_tareas)
    proyecto = id_a_proyecto(
        consola, "Ingrese el ID del proyecto cuyas tareas desea gestionar: ")
    if isinstance(proyecto, Resultado):  # Resultado de error
        proyecto.origen = fn_tareas
        return proyecto
    gestor.gestionar_tareas(proyecto)
    consola.cambiar_contexto("tareas")
    consola.ayuda()
    return Resultado("", fn_tareas)
contextos["proyectos"]["tareas"] = Comando(fn_tareas, "tareas [id]")

def fn_agregar_tarea(consola, linea_comando):
    "Añade una nueva tarea al proyecto"
    print("Ingrese la siguiente información requerida.")
    argumentos = consola.leer_argumentos(nombres_argumentos_tarea,
                                         mensajes_argumentos_tarea)
    for nombre in ("fecha_inicio", "fecha_vencimiento"):
        res = leer_fecha(argumentos, nombre)
        if isinstance(res, Resultado):  # Resultado de error
            res.origen = fn_agregar_tarea
            return res
    res = leer_porcentaje(argumentos, "porcentaje")
    if isinstance(res, Resultado):
        res.origen = fn_agregar_tarea
        return res

    try:
        tarea = gestor.agregar_tarea(argumentos)
    except ValueError as e:
        return Resultado("Error: " + e.args[0], fn_agregar_tarea,
                         tipo_error="Valor")
    return Resultado("La tarea ha sido creada, su ID es " + str(tarea.id),
                     fn_agregar_tarea)
contextos["tareas"]["agregar"] = Comando(fn_agregar_tarea, "agregar")

def fn_enumerar_tareas(consola, linea_comando):
    "Enumera las tareas asignadas al proyecto"
    tarea_principal = len(gestor.tareas) == 0
    if (len(gestor.proyecto.tareas) if tarea_principal
        else len(gestor.tareas.cima.subtareas)) == 0:
        return Resultado("No hay tareas para mostrar.", fn_enumerar_tareas)
    if tarea_principal:
        resultado = "\n\n".join(map(str, gestor.proyecto.tareas))
    else:
        resultado = "\n\n".join(map(str, gestor.tareas.cima.subtareas))
    return Resultado(resultado, fn_enumerar_tareas)
contextos["tareas"]["mostrar"] = Comando(fn_enumerar_tareas, "mostrar")

def fn_consultar_tarea(consola, linea_comando):
    "Consulta una tarea existente"
    tarea = id_a_tarea(
        consola, "Ingrese el ID de la tarea que desea consultar: ")
    if isinstance(tarea, Resultado):  # Resultado de error
        tarea.origen = fn_consultar_tarea
        return tarea

    return Resultado(format(tarea, "g"), fn_consultar_tarea)
contextos["tareas"]["consultar"] = Comando(fn_consultar_tarea, "consultar [id]")

def fn_modificar_tarea(consola, linea_comando):
    "Modifica una tarea existente"
    tarea = id_a_tarea(
        consola, "Ingrese el ID de la tarea que desea modificar: ")
    if isinstance(tarea, Resultado):  # Resultado de error
        tarea.origen = fn_modificar_tarea
        return tarea
    print(format(tarea, "g"))

    print("\nPara mantener una propiedad de la tarea intacta"
          " solo presione 'Enter'")
    argumentos = consola.leer_argumentos(nombres_argumentos_tarea,
                                         mensajes_argumentos_tarea)
    for nombre in ("fecha_inicio", "fecha_vencimiento"):
        if argumentos[nombre] != "":
            res = leer_fecha(argumentos, nombre)
            if isinstance(res, Resultado):
                res.origen = fn_modificar_tarea
                return res
    if argumentos["porcentaje"] != "":
        res = leer_porcentaje(argumentos, "porcentaje")
        if isinstance(res, Resultado):
            res.origen = fn_modificar_tarea
            return res

    for nombre, valor in list(argumentos.items()):
        if valor == "":
            argumentos.pop(nombre)
    try:
        gestor.modificar_tarea(argumentos, tarea)
    except ValueError as e:
        return Resultado("Error: " + e.args[0], fn_modificar_tarea,
                         tipo_error="Valor")
    return Resultado("Tarea modificada exitosamente.", fn_modificar_tarea)
contextos["tareas"]["modificar"] = Comando(fn_modificar_tarea, "modificar")

def fn_eliminar_tarea(consola, linea_comando):
    "Elimina una tarea del proyecto"
    tarea = id_a_tarea(
        consola, "Ingrese el ID de la tarea que desea eliminar: ")
    if isinstance(tarea, Resultado):  # Resultado de error
        tarea.origen = fn_eliminar_tarea
        return tarea

    print(tarea)
    if consola.confirmar("Está seguro que desea eliminar esta tarea?"):
        gestor.eliminar_tarea(tarea)
        return Resultado("La tarea con ID %d ha sido eliminada." % tarea.id,
                         fn_eliminar_tarea)
    return Resultado("", fn_eliminar_tarea)
contextos["tareas"]["eliminar"] = Comando(fn_eliminar_tarea, "eliminar [id]")


def fn_subtareas(consola, linea_comando):
    "Gestiona las subtareas de una tarea"
    if len(gestor.tareas) == 0:
        if len(gestor.proyecto.tareas) == 0:
            return Resultado("Error: debe crear al menos una tarea antes"
                             " de ingresar en el menú de subtareas",
                             fn_subtareas)
    else:
        if len(gestor.tareas.cima.subtareas) == 0:
            return Resultado("Error: debe crear al menos una subtarea antes"
                             " de ingresar en el menú de las subtareas"
                             " descendientes", fn_subtareas)
    tarea = id_a_tarea(
        consola, "Ingrese el ID de la tarea cuyas subtareas desea gestionar: ")
    if isinstance(tarea, Resultado):  # Resultado de error
        tarea.origen = fn_subtareas
        return tarea
    gestor.gestionar_subtareas(tarea)
    consola.cambiar_contexto("subtareas")
    consola.ayuda()
    return Resultado("", fn_subtareas)
contextos["tareas"]["subtareas"] = Comando(fn_subtareas, "subtareas [id]")

def fn_agregar_subtarea(consola, linea_comando):
    "Añade una nueva subtarea a la tarea"
    resultado = fn_agregar_tarea(consola, linea_comando)
    resultado.origen = fn_agregar_subtarea
    return resultado
contextos["subtareas"]["agregar"] = Comando(fn_agregar_subtarea, "agregar")

def fn_enumerar_subtareas(consola, linea_comando):
    "Enumera las subtareas asignadas a la tarea"
    resultado = fn_enumerar_tareas(consola, linea_comando)
    resultado.origen = fn_enumerar_subtareas
    return resultado
contextos["subtareas"]["mostrar"] = Comando(fn_enumerar_subtareas, "mostrar")

def fn_consultar_subtarea(consola, linea_comando):
    "Consulta una subtarea existente"
    resultado = fn_consultar_tarea(consola, linea_comando)
    resultado.origen = fn_consultar_subtarea
    return resultado
contextos["subtareas"]["consultar"] = \
    Comando(fn_consultar_subtarea, "consultar [id]")

def fn_modificar_subtarea(consola, linea_comando):
    "Modifica una subtarea existente"
    resultado = fn_modificar_tarea(consola, linea_comando)
    resultado.origen = fn_modificar_subtarea
    return resultado
contextos["subtareas"]["modificar"]= Comando(fn_modificar_subtarea, "modificar")

def fn_eliminar_subtarea(consola, linea_comando):
    "Elimina una subtarea de la tarea"
    resultado = fn_eliminar_tarea(consola, linea_comando)
    resultado.origen = fn_eliminar_subtarea
    return resultado
contextos["subtareas"]["eliminar"] = \
    Comando(fn_eliminar_subtarea, "eliminar [id]")


# Van al final para que aparezcan de último en la lista de comandos
def fn_regresar_a_empresas(consola, linea_comando):
    "Regresa al menú de empresas"
    return macro_regresar(consola, linea_comando,
                          "principal", fn_regresar_a_empresas)
contextos["proyectos"]["regresar"] = Comando(fn_regresar_a_empresas,
                                             "regresar")

def fn_regresar_a_proyectos(consola, linea_comando):
    "Regresa al menú de proyectos"
    return macro_regresar(consola, linea_comando,
                          "proyectos", fn_regresar_a_proyectos)
contextos["tareas"]["regresar"] = Comando(fn_regresar_a_proyectos, "regresar")

def fn_regresar_a_tarea_padre(consola, linea_comando):
    "Regresa al menú de la tarea padre"
    if len(gestor.tareas) <= 1:
        contexto = "tareas"
    else:
        contexto = "subtareas"
    return macro_regresar(consola, linea_comando,
                          contexto, fn_regresar_a_tarea_padre)
contextos["subtareas"]["regresar"] = \
    Comando(fn_regresar_a_tarea_padre, "regresar")


def main():
    consola = Consola(contextos)
    consola.consola()
    # Por ahora es todo

if __name__ == "__main__":
    main()

