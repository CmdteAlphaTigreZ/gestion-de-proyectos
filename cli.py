from proyectos import *
from colecciones import *
from consola import *
from datetime import datetime


contextos = Contextos()
contextos.agregar("proyectos", {})
contextos.agregar("tareas", {})
proyectos = Lista()


def fn_proyectos(consola, linea_comando):
    "Cambiar al menú de proyectos"
    consola.cambiar_contexto("proyectos")
    consola.ayuda()
contextos["principal"]["proyectos"] = Comando(fn_proyectos, "proyectos")

def fn_agregar_proyecto(consola, linea_comando):
    "Añade un nuevo proyecto"
    #nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, \
    #    empresa, gerente, equipo \
    argumentos \
        = consola.leer_comando(linea_comando, (
            "Ingrese el nombre del proyecto: ",
            "Ingrese la descripción del proyecto: ",
            "Ingrese la fecha de inicio del proyecto (dd/mm/yyyy): "
            "Ingrese la fecha de vencimiento del proyecto (dd/mm/yyyy): ",
            "Ingrese el estado actual del proyecto: ",
            "Ingrese el nombre de la empresa del proyecto: ",
            "Ingrese el nombre del gerente del proyecto: ",
            "Ingrese el nombre del equipo del proyecto: "
    ))
    argumentos[2] = datetime.strptime(argumentos[2], "%d/%m/%Y")
    argumentos[3] = datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
    proyecto = Proyecto( *([len(proyectos)] + argumentos) )
    proyectos.anexar(proyecto)
    print("El proyecto ha sido creado, su ID es " + str(proyecto.id))
contextos["proyectos"]["agregar"] = Comando(fn_agregar_proyecto, "agregar")


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

