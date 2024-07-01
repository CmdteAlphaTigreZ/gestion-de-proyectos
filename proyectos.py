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
        self.tareas.append(tarea)

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


