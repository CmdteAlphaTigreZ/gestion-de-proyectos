from proyectos import *
from colecciones import *
from consola import *
from datetime import datetime


contextos = Contextos()
contextos.agregar("proyectos", {})
contextos.agregar("tareas", {})
proyectos = {}
id_max = len(proyectos)

def fn_proyectos(consola, linea_comando):
    "Cambiar al menú de proyectos"
    consola.cambiar_contexto("proyectos")
    consola.ayuda()
contextos["principal"]["proyectos"] = Comando(fn_proyectos, "proyectos")

def fn_agregar_proyecto(consola, linea_comando):
    "Añade un nuevo proyecto"
    argumentos = consola.leer_argumentos(linea_comando, (
        "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
        "estado_actual", "empresa", "gerente", "equipo"
    ), (
        "Ingrese el nombre del proyecto: ",
        "Ingrese la descripción del proyecto: ",
        "Ingrese la fecha de inicio del proyecto (dd/mm/yyyy): "
        "Ingrese la fecha de vencimiento del proyecto (dd/mm/yyyy): ",
        "Ingrese el estado actual del proyecto: ",
        "Ingrese el nombre de la empresa del proyecto: ",
        "Ingrese el nombre del gerente del proyecto: ",
        "Ingrese el nombre del equipo del proyecto: "
    ) )
    argumentos["fecha_inicio"] = \
       datetime.strptime(argumentos["fecha_inicio"], "%d/%m/%Y")
    argumentos["fecha_vencimiento"] = \
        datetime.strptime(argumentos["fecha_vencimiento"], "%d/%m/%Y")
    id_max += 1
    proyecto = Proyecto( *([id_max] + list(argumentos.values())) )
    proyectos[id_max] = proyecto
    return Resultado("El proyecto ha sido creado, su ID es " + str(proyecto.id),
                     self)
contextos["proyectos"]["agregar"] = Comando(fn_agregar_proyecto, "agregar")

def fn_modificar_proyecto(consola, linea_comando):
    "Modifica un proyecto existente"
    id_proyecto = consola.leer_comando(
        linea_comando, "Ingrese el ID del Proyecto que desea modificar: ")[0]
    id_proyecto = int(id_proyecto)
    if id_proyecto not in proyectos:
        return Resultado("El ID del proyecto no existe", self)
    
    print("Para mantener una propiedad del proyecto intacta"
          " solo presione 'Enter'")
    argumentos = consola.leer_argumentos(linea_comando, (
        "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
        "estado_actual", "empresa", "gerente", "equipo"
    ), (
        "Ingrese el nombre del proyecto: ",
        "Ingrese la descripción del proyecto: ",
        "Ingrese la fecha de inicio del proyecto (dd/mm/yyyy): "
        "Ingrese la fecha de vencimiento del proyecto (dd/mm/yyyy): ",
        "Ingrese el estado actual del proyecto: ",
        "Ingrese el nombre de la empresa del proyecto: ",
        "Ingrese el nombre del gerente del proyecto: ",
        "Ingrese el nombre del equipo del proyecto: "
    ) )
    argumentos["fecha_inicio"] = \
       datetime.strptime(argumentos["fecha_inicio"], "%d/%m/%Y")
    argumentos["fecha_vencimiento"] = \
        datetime.strptime(argumentos["fecha_vencimiento"], "%d/%m/%Y")

    for nombre, valor in argumentos.items():
        if valor == "": continue
        setattr(proyecto, nombre, valor)
contextos["proyectos"]["modificar"] = Comando(fn_modificar_proyecto, "modificar")


def fn_tareas(consola, linea_comando):
    "Cambiar al menú de tareas"
    consola.cambiar_contexto("tareas")
    consola.ayuda()
contextos["principal"]["tareas"] = Comando(fn_tareas, "tareas")


def main():
    consola = Consola(contextos)
    consola.consola()
    # Por ahora es todo

if __name__ == "__main__":
    main()

