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
from datetime import date
import utilidades as util


class Proyecto:
    """Proyecto

    El 'id' debe ser un entero, y las fechas datetime.date.
    Por ahora no hay más restricciones, y las presentes no se imponen.
    """

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
        self.__tareas = ArbolNario(duplicados=False)
        self.__tareas.insertar_nodo(self)

    @property
    def tareas(self):
        "Árbol n-ario de tareas del proyecto."
        return self.__tareas

    def agregar_tarea(self, tarea):
        "Agrega una 'Tarea' al proyecto, solo si no está ya incluida."
        if self.buscar_tarea("id", tarea.id) is None:
            self.__tareas.insertar_nodo(tarea.subtareas.raiz,
                                        self.__tareas.raiz)

    def buscar_tarea(self, atributo, valor):
        """Busca la primera tarea cuyo atributo sea el valor dado.

        'atributo' debe ser tipo 'str', el nombre del atributo buscado
        Si el atributo no está presente en alguna tarea,
        simplemente se ignora.
        Devuelve None si no encuentra la tarea buscada
        """
        iterador = self.__tareas.en_anchura()
        next(iterador)  # Descartar raíz
        return util.buscar_por_atributo(iterador, atributo, valor)

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
            cant_tareas=len(self.__tareas) - 1,
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
    """Tarea

    El 'porcentaje' debe ser un 'float'.
    Véase la documentación de Proyecto para el resto."""

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
        self.__subtareas = ArbolNario(duplicados=False)
        self.__subtareas.insertar_nodo(self)

    @property
    def subtareas(self):
        "Subárbol n-ario de subtareas de la tarea."
        return self.__subtareas

    def agregar_subtarea(self, tarea):
        "Agrega una 'Tarea' como subtarea, solo si no está ya incluida."
        if self.buscar_subtarea("id", tarea.id) is None:
            self.__tareas.insertar_nodo(tarea.subtareas.raiz
                                        self.__subtareas.raiz)

    def buscar_subtarea(self, atributo, valor):
        """Busca la primera subtarea cuyo atributo sea el valor dado.

        Véase la documentación de Proyecto.buscar_tarea.
        """
        iterador = self.__subtareas.en_anchura()
        next(iterador)  # Descartar raíz
        return util.buscar_por_atributo(iterador, atributo, valor)

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
            cant_subtareas=len(self.subtareas) - 1,
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
    "Gestor de proyectos multiempresa."

    ERROR_NO_FORZADO = 1
    ERROR_NO_EMPRESA = 10
    __MSG_ERROR_NO_EMPRESA = "No hay empresa con proyectos siendo gestionados"
    ERROR_PROYECTO_NO_PERTENECE = 11
    ERROR_NO_PROYECTO = 20
    ERROR_TAREA_NO_PERTENECE = 21
    ERROR_NO_TAREA = 30

    def __init__(self):
        self.id_empresa_max = 0
        self.id_proyecto_max = 0
        self.id_tarea_max = 0
        self.__empresas = ListaEnlazada()
        self.empresa = None
        self.proyecto = None
        self.__tareas = Pila()

    @property
    def empresas(self):
        "Lista que almacena todas las empresas gestionadas."
        return self.__empresas

    @property
    def tareas(self):
        "Pila que almacena la cadena de subtareas en edición."
        return self.__tareas

    def gestionar_proyectos(self, empresa, forzar=False):
        if not forzar \
            and not (self.empresa is None and self.proyecto is None
                     and len(self.__tareas) == 0):
            raise RuntimeError("Debe salir de la gestión de la empresa actual"
                               " para cambiar la empresa gestionada",
                               Gestor.ERROR_NO_FORZADO)
        self.__tareas.vaciar()
        self.proyecto = None
        self.empresa = empresa

    def gestionar_tareas(self, proyecto, forzar=False):
        if not forzar \
            and not (self.proyecto is None and len(self.__tareas) == 0):
            raise RuntimeError("Debe salir de la gestión del proyecto actual"
                               " para cambiar el proyecto gestionado",
                               Gestor.ERROR_NO_FORZADO)
        if self.empresa is None:
            raise RuntimeError(Gestor.__MSG_ERROR_NO_EMPRESA,
                               Gestor.ERROR_NO_EMPRESA)
        if self.empresa.proyectos.buscar(ClaveValor(proyecto.id, None)) is None:
            raise RuntimeError("El proyecto no pertenece a la empresa en edición",
                               Gestor.ERROR_PROYECTO_NO_PERTENECE)
        self.__tareas.vaciar()
        self.proyecto = proyecto

    def gestionar_subtareas(self, tarea):
        if self.empresa is None:
            raise RuntimeError(Gestor.__MSG_ERROR_NO_EMPRESA,
                               Gestor.ERROR_NO_EMPRESA)
        if self.proyecto is None:
            raise RuntimeError("No hay proyecto con tareas siendo gestionadas",
                               Gestor.ERROR_NO_PROYECTO)
        if len(self.__tareas) == 0:
            raiz = self.proyecto.tareas.raiz
        else:
            raiz = self.__tareas.cima.subtareas.raiz
        if util.buscar(
            lambda nodo: nodo.valor is not None and nodo.valor.id == tarea.id,
            raiz.hijos()
        ) is None:
            raise RuntimeError("La tarea no pertenece al proyecto o tarea padre"
                               " en edición", Gestor.ERROR_TAREA_NO_PERTENECE)
        self.__tareas.insertar(tarea)

    def regresar_a_empresas(self, forzar=False):
        if not forzar \
            and not (self.proyecto is None and len(self.__tareas) == 0):
            raise RuntimeError("Debe regresar de la edición de tareas antes de"
                               " regresar de la edición de proyectos",
                               Gestor.ERROR_NO_FORZADO)
        if self.empresa is None:
            raise RuntimeError("No se está gestionando los proyectos de una"
                               " empresa.  El contexto actual ya es la gestión"
                               " de empresas", Gestor.ERROR_NO_EMPRESA)
        # POR HACER: Guardar proyectos de la empresa
        self.__tareas.vaciar()
        self.proyecto = None
        self.empresa = None

    def regresar_a_proyectos(self, forzar=False):
        if not forzar and len(self.__tareas) != 0:
            raise RuntimeError("Debe regresar de la edición de subtareas antes"
                               " de regresar de la edición de tareas del"
                               " proyecto", Gestor.ERROR_NO_FORZADO)
        if self.proyecto is None:
            raise RuntimeError("No se está gestionando las tareas de un"
                               " proyecto.  El contexto actual ya es la gestión"
                               " de proyectos", Gestor.ERROR_NO_PROYECTO)
        # POR HACER: Guardar tareas del proyecto
        self.__tareas.vaciar()
        self.proyecto = None

    def regresar_a_tarea_padre(self):
        if len(self.__tareas) != 0:
            raise RuntimeError("No se está gestionando las subtareas de una"
                               " tarea.  El contexto actual es la gestión"
                               " de las tareas principales de un proyecto",
                               Gestor.ERROR_NO_TAREA)
        # POR HACER: Guardar subtareas de la tarea
        self.__tareas.extraer()

    def regresar(self):
        if len(self.__tareas) != 0:
            self.regresar_a_tarea_padre()
        elif self.proyecto is not None:
            self.regresar_a_proyectos()
        elif self.empresa is not None:
            self.regresar_a_empresas()
        else:
            raise RuntimeError("El contexto actual ya es la gestión de empresas"
                               ".  No hay dónde regresar",
                               Gestor.ERROR_NO_EMPRESA)
