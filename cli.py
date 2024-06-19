from proyectos import *
from colecciones import *
from consola import *
import utilidades as util


contextos = Contextos()
contextos.agregar("proyectos", {})
contextos.agregar("tareas", {})
proyectos = {}
id_max = len(proyectos)

def leer_fecha_proyecto(argumentos, nombre):
    "Interpreta una fecha desde los argumentos de línea de comandos."
    " Devuelve un resultado de error si aplica."
    try:
       argumentos[nombre] = util.leer_fecha(argumentos[nombre])
    except ValueError as e:
        return Resultado("Error: '%s' no es una fecha válida: %s"
                         % (nombre, argumentos[nombre]),
                         None,
                         tipo_error="Valor" )


def fn_proyectos(consola, linea_comando):
    "Cambiar al menú de proyectos"
    consola.cambiar_contexto("proyectos")
    consola.ayuda()
    return Resultado("", fn_proyectos)
contextos["principal"]["proyectos"] = Comando(fn_proyectos, "proyectos")
# Recordar añadir regresar al final de cada sección

def fn_agregar_proyecto(consola, linea_comando):
    "Añade un nuevo proyecto"
    global id_max
    argumentos = consola.leer_argumentos((
        "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
        "estado", "empresa", "gerente", "equipo"
    ), (
        "Ingrese el nombre del proyecto: ",
        "Ingrese la descripción del proyecto: ",
        "Ingrese la fecha de inicio del proyecto (dd/mm/yyyy): ",
        "Ingrese la fecha de vencimiento del proyecto (dd/mm/yyyy): ",
        "Ingrese el estado actual del proyecto: ",
        "Ingrese el nombre de la empresa del proyecto: ",
        "Ingrese el nombre del gerente del proyecto: ",
        "Ingrese el nombre del equipo del proyecto: "
    ))
    for nombre in ("fecha_inicio", "fecha_vencimiento"):
        if argumentos[nombre] != "":
            res = leer_fecha_proyecto(argumentos, nombre)
            if isinstance(res, Resultado):  # Resultado de error
                res.origen = fn_agregar_proyecto
                return res

    id_max += 1
    proyecto = Proyecto( *([id_max] + list(argumentos.values())) )
    proyectos[id_max] = proyecto
    return Resultado("El proyecto ha sido creado, su ID es " + str(proyecto.id),
                     fn_agregar_proyecto)
contextos["proyectos"]["agregar"] = Comando(fn_agregar_proyecto, "agregar")

def fn_modificar_proyecto(consola, linea_comando):
    "Modifica un proyecto existente"
    id_proyecto = consola.leer_argumentos( ("id",),
        ("Ingrese el ID del Proyecto que desea modificar: ",), linea_comando)["id"]
    id_proyecto = int(id_proyecto)
    if id_proyecto not in proyectos:
        return Resultado("El ID del proyecto no existe", self)
    
    print("Para mantener una propiedad del proyecto intacta"
          " solo presione 'Enter'")
    argumentos = consola.leer_argumentos((
        "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
        "estado", "empresa", "gerente", "equipo"
    ), (
        "Ingrese el nombre del proyecto: ",
        "Ingrese la descripción del proyecto: ",
        "Ingrese la fecha de inicio del proyecto (dd/mm/yyyy): ",
        "Ingrese la fecha de vencimiento del proyecto (dd/mm/yyyy): ",
        "Ingrese el estado actual del proyecto: ",
        "Ingrese el nombre de la empresa del proyecto: ",
        "Ingrese el nombre del gerente del proyecto: ",
        "Ingrese el nombre del equipo del proyecto: "
    ))
    for nombre in ("fecha_inicio", "fecha_vencimiento"):
        if argumentos[nombre] != "":
            res = leer_fecha_proyecto(argumentos, nombre)
            if isinstance(res, Resultado):
                res.origen = fn_modificar_proyecto
                return res

    proyecto = proyectos[id_proyecto]
    for nombre, valor in argumentos.items():
        if valor == "": continue
        setattr(proyecto, nombre, valor)
    return Resultado("Proyecto modificado exitosamente", self)
contextos["proyectos"]["modificar"] = Comando(fn_modificar_proyecto, "modificar")


def fn_tareas(consola, linea_comando):
    "Cambiar al menú de tareas"
    consola.cambiar_contexto("tareas")
    consola.ayuda()
    return Resultado("", fn_tareas)
contextos["principal"]["tareas"] = Comando(fn_tareas, "tareas")


def main():
    consola = Consola(contextos)
    consola.consola()
    # Por ahora es todo

if __name__ == "__main__":
    main()

