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
        self.__pila_prioridades = Pila()
        self.__cola_vencimientos = Cola()

    @property
    def tareas(self): return self.__tareas

    @property
    def pila_prioridades(self): return self.__pila_prioridades

    @property
    def cola_vencimientos(self): return self.__cola_vencimientos

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def agregar_pila(self, pila_prioridades):
        self.pila_prioridades.append(pila_prioridades)

    def agregar_prioridad(self, tarea_prioritaria):
        self.pila_prioridades.apilar(tarea_prioritaria)
        print(f"Tarea prioritaria '{tarea_prioritaria.nombre}' agregada.")

    def agregar_cola(self, cola_vencimientos):
        self.cola_vencimientos.append(cola_vencimientos)

    def __format__(self, formato):
        if formato == "":
            return str(self)
        elif formato != "g":
            raise ValueError("la especificación de formato debe ser '' o 'g'")
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}"',
                     'Descripcion:\n{descripcion}',
                     'Fecha de inicio: {fecha_inicio}',
                     'Fecha de vencimiento: {fecha_vencimiento}',
                     'Estado actual: "{self.estado}"',
                     'Empresa: {self.empresa}',
                     'Gerente: {self.gerente}',
                     'Equipo: {self.equipo}' ]
        resultado = "\n".join(resultado)
        resultado = resultado.format(
            self=self,
            fecha_inicio=util.fecha_a_str(self.fecha_inicio),
            fecha_vencimiento=util.fecha_a_str(self.fecha_vencimiento),
            descripcion=util.envolver_y_sangrar(self.descripcion)
        )
        return resultado

    def __str__(self):
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}',
                     'Estado actual: "{self.estado}"' ]
        resultado = "\n".join(resultado)
        return resultado.format(self=self)


class Tarea:

    def __init__(
        self,
        id_,
        nombre,
        empresa_cliente,
        descripcion,
        fecha_inicio,
        fecha_vencimiento,
        estado,
        porcentaje,
    ):
        self.id = id_
        self.nombre = nombre
        self.empresa_cliente = empresa_cliente
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.porcentaje = porcentaje
        self.subtareas = Lista()


class Subtarea:
    def __init__(self, id_, nombre, descripcion, estado):
        self.id = id_
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
