#!/usr/bin/env python3
from proyectos import *
from colecciones import *
from consola import *
import utilidades as util


contextos = Contextos()
contextos.agregar("proyectos", {})
contextos.agregar("tareas", {})
proyectos = {}
id_max = len(proyectos)

# Tomado del constructor de Proyecto en proyectos.py.  Mantener sincronizado
nombres_argumentos_proyecto = (
    "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
    "estado", "empresa", "gerente", "equipo" )
mensajes_argumentos_proyecto = (
    "Ingrese el nombre del proyecto: ",
    "Ingrese la descripción del proyecto: ",
    "Ingrese la fecha de inicio del proyecto (dd/mm/yyyy): ",
    "Ingrese la fecha de vencimiento del proyecto (dd/mm/yyyy): ",
    "Ingrese el estado actual del proyecto: ",
    "Ingrese el nombre de la empresa del proyecto: ",
    "Ingrese el nombre del gerente del proyecto: ",
    "Ingrese el nombre del equipo del proyecto: " )
# Tomado del constructor de Tarea en proyectos.py.  Mantener sincronizado

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

def leer_id_proyecto(consola, mensaje):
    "Solicita un ID de proyecto al usuario."
    " Devuelve un resultado de error si aplica."
    id_proyecto = leer_id(consola, mensaje)
    if isinstance(id_proyecto, Resultado): return id_proyecto
    if id_proyecto not in proyectos:
        return Resultado("Error: no existe un proyecto con ese ID: "
                         + str(id_proyecto), None, tipo_error="Valor")
    return id_proyecto

def leer_id_tarea(consola, mensaje):
    "Solicita un ID de tarea al usuario."
    " Devuelve un resultado de error si aplica."
    id_tarea = leer_id(consola, mensaje)
    if isinstance(id_tarea, Resultado): return id_tarea
    if proyecto_seleccionado.buscar_tarea("id", id_tarea) is None:
        return Resultado("Error: no existe una tarea en este proyecto con ese ID: "
                         + str(id_tarea), None, tipo_error="Valor")
    return id_tarea

def leer_fecha(argumentos, nombre):
    "Interpreta una fecha desde los argumentos de línea de comandos."
    " Devuelve un resultado de error si aplica."
    try:
       argumentos[nombre] = util.str_a_fecha(argumentos[nombre])
    except ValueError as e:
        return Resultado("Error: '%s' no es una fecha válida: %s"
                         % (nombre, argumentos[nombre]),
                         None,
                         tipo_error="Valor" )

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


def fn_proyectos(consola, linea_comando):
    "Cambia al menú de proyectos"
    consola.cambiar_contexto("proyectos")
    consola.ayuda()
    return Resultado("", fn_proyectos)
contextos["principal"]["proyectos"] = Comando(fn_proyectos, "proyectos")
# Recordar añadir regresar al final de cada sección

def fn_agregar_proyecto(consola, linea_comando):
    "Añade un nuevo proyecto"
    global id_max
    argumentos = consola.leer_argumentos(nombres_argumentos_proyecto,
                                         mensajes_argumentos_proyecto)
    for nombre in ("fecha_inicio", "fecha_vencimiento"):
        res = leer_fecha(argumentos, nombre)
        if isinstance(res, Resultado):  # Resultado de error
            res.origen = fn_agregar_proyecto
            return res

    id_max += 1
    argumentos["id_"] = id_max
    proyecto = Proyecto(**argumentos)
    proyectos[id_max] = proyecto
    return Resultado("El proyecto ha sido creado, su ID es " + str(proyecto.id),
                     fn_agregar_proyecto)
contextos["proyectos"]["agregar"] = Comando(fn_agregar_proyecto, "agregar")

def fn_enumerar_proyectos(consola, linea_comando):
    "Enumera los proyectos registrados"
    if len(proyectos) == 0:
        return Resultado("No hay proyectos para mostrar.", fn_enumerar_proyectos)
    resultado = "\n\n".join(str(proyecto) for proyecto in proyectos.values())
    return Resultado(resultado, fn_enumerar_proyectos)
contextos["proyectos"]["mostrar"] = Comando(fn_enumerar_proyectos, "mostrar")

def fn_consultar_proyecto(consola, linea_comando):
    "Consulta un proyecto existente"
    id_proyecto = leer_id_proyecto(
        consola, "Ingrese el ID del proyecto que desea consultar: ")
    if isinstance(id_proyecto, Resultado):  # Resultado de error
        id_proyecto.origen = fn_consultar_proyecto
        return id_proyecto

    return Resultado(format(proyectos[id_proyecto], "g"), fn_consultar_proyecto)
contextos["proyectos"]["consultar"] = \
    Comando(fn_consultar_proyecto, "consultar [id]")

def fn_modificar_proyecto(consola, linea_comando):
    "Modifica un proyecto existente"
    id_proyecto = leer_id_proyecto(
        consola, "Ingrese el ID del proyecto que desea modificar: ")
    if isinstance(id_proyecto, Resultado):  # Resultado de error
        id_proyecto.origen = fn_modificar_proyecto
        return id_proyecto
    print(format(proyectos[id_proyecto], "g"))
    
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

    proyecto = proyectos[id_proyecto]
    for nombre, valor in argumentos.items():
        if valor == "": continue
        setattr(proyecto, nombre, valor)
    return Resultado("Proyecto modificado exitosamente.", fn_modificar_proyecto)
contextos["proyectos"]["modificar"] = Comando(fn_modificar_proyecto, "modificar")

def fn_eliminar_proyecto(consola, linea_comando):
    "Elimina un proyecto"
    id_proyecto = leer_id_proyecto(
        consola, "Ingrese el ID del proyecto que desea eliminar: ")
    if isinstance(id_proyecto, Resultado):  # Resultado de error
        id_proyecto.origen = fn_consultar_proyecto
        return id_proyecto

    print(proyectos[id_proyecto])
    if consola.confirmar("Está seguro que desea eliminar este proyecto?"):
        del proyectos[id_proyecto]
        return Resultado(
            "El proyecto con ID %d ha sido eliminado." % id_proyecto,
            fn_eliminar_proyecto)
    return Resultado("", fn_eliminar_proyecto)
contextos["proyectos"]["eliminar"] = \
    Comando(fn_eliminar_proyecto, "eliminar [id]")

def fn_regresar_a_principal(consola, linea_comando):
    "Regresa al menú principal"
    consola.cambiar_contexto("principal")
    consola.ayuda()
    return Resultado("", fn_regresar_a_principal)
contextos["proyectos"]["regresar"] = Comando(fn_regresar_a_principal,
                                             "regresar")



def fn_tareas(consola, linea_comando):
    "Cambiar al menú de tareas"
    if len(proyectos) == 0:
        return Resultado("Error: debe crear al menos un proyecto antes"
                         " de ingresar en el menú de tareas", fn_tareas)
    consola.cambiar_contexto("tareas")
    consola.ayuda()
    return Resultado("", fn_tareas)
contextos["principal"]["tareas"] = Comando(fn_tareas, "tareas")
contextos["tareas"]["regresar"] = cmd_regresar


def main():
    consola = Consola(contextos)
    consola.consola()
    # Por ahora es todo

if __name__ == "__main__":
    main()

