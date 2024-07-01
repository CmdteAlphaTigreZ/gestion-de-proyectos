# Módulo de gestión de proyectos
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-07-01
# Cambios:
#   v1
#     * Versión inicial
#   v2
#     * Funciones de búsqueda
#     * Gestor


from colecciones import *
#from datetime import datetime


class Proyecto:

    def __init__(
        self,
        id_,
        nombre,
        descripcion,
        fecha_inicio,
        fecha_vencimiento,
        estado,
        empresa,
        gerente,
        equipo,
    ):
        self.id = id_
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.empresa = empresa
        self.gerente = gerente
        self.equipo = equipo
        self.__tareas = Lista()

    @property
    def tareas(self): return self.__tareas

    def agregar_tarea(self, tarea):
        if self.tareas.indice(tarea) == -1:
            self.tareas.anexar(tarea)

    def buscar_tarea(self, atributo, valor):
        return self.tareas.buscar_por_atributo(atributo, valor)

    def __format__(self, formato):
        if formato == "":
            return str(self)
        elif formato != "g":
            raise ValueError("la especificación de formato debe ser '' o 'g'")
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}"',
                     'Descripción:\n{descripcion}',
                     'Fecha de inicio: {fecha_inicio}',
                     'Fecha de vencimiento: {fecha_vencimiento}',
                     'Estado actual: "{self.estado}"',
                     'Empresa: {self.empresa}',
                     'Gerente: {self.gerente}',
                     'Equipo: {self.equipo}',
                     'No. de tareas: {cant_tareas}']
        resultado = "\n".join(resultado)
        resultado = resultado.format(
            self=self,
            fecha_inicio=util.fecha_a_str(self.fecha_inicio),
            fecha_vencimiento=util.fecha_a_str(self.fecha_vencimiento),
            cant_tareas=len(self.__tareas),
            descripcion=util.envolver_y_sangrar(self.descripcion)
        )
        return resultado

    def __str__(self):
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}"',
                     'Estado actual: "{self.estado}"' ]
        resultado = "\n".join(resultado)
        return resultado.format(self=self)


class Tarea:

    def __init__(
        self,
        id_,
        nombre,
        descripcion,
        fecha_inicio,
        fecha_vencimiento,
        estado,
        porcentaje,
        empresa_cliente,
    ):
        self.id = id_
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.porcentaje = porcentaje
        self.empresa_cliente = empresa_cliente
        self.__subtareas = Lista()

    @property
    def subtareas(self): return self.__subtareas

    def agregar_subtarea(self, tarea):
        if self.subtareas.indice(tarea) == -1:
            self.subtareas.anexar(tarea)

    def buscar_subtarea(self, atributo, valor):
        return self.subtareas.buscar_por_atributo(atributo, valor)

    def __format__(self, formato):
        if formato == "":
            return str(self)
        elif formato != "g":
            raise ValueError("la especificación de formato debe ser '' o 'g'")
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}"',
                     'Descripción:\n{descripcion}',
                     'Fecha de inicio: {fecha_inicio}',
                     'Fecha de vencimiento: {fecha_vencimiento}',
                     'Estado actual: "{self.estado}"',
                     'Porcentaje de completación: {self.porcentaje:.2f}%',
                     'Empresa cliente: {self.empresa_cliente}',
                     'No. de subtareas: {cant_subtareas}' ]
        resultado = "\n".join(resultado)
        resultado = resultado.format(
            self=self,
            fecha_inicio=util.fecha_a_str(self.fecha_inicio),
            fecha_vencimiento=util.fecha_a_str(self.fecha_vencimiento),
            cant_subtareas=len(self.subtareas),
            descripcion=util.envolver_y_sangrar(self.descripcion)
        )
        return resultado

    def __str__(self):
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}"',
                     'Estado actual: "{self.estado}"' ]
        resultado = "\n".join(resultado)
        return resultado.format(self=self)

class Gestor:

    def __init__(self):
        self.id_proyecto_max = 0
        self.id_tarea_max = 0
        self.empresa = None
        self.proyecto = None
        self.__tareas = Pila()

    @property
    def tareas(self): return self.__tareas
