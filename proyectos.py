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
import csv
import utilidades as util


def _comprobar_nombres_de_atributos(nombres, atributos):
    util.comprobar_tipos("atributos", atributos, dict)
    for nombre in atributos:
        if nombre not in nombres:
            raise AttributeError(nombre)


class Empresa:

    _NOMBRES_ATRIBUTOS = (
        "id", "nombre", "descripcion", "fecha_creacion", "direccion",
        "telefono", "correo", "gerente", "equipo_contacto",
        "_Empresa__proyectos" )

    def __init__(
        self,
        id_,
        nombre,
        descripcion,
        fecha_creacion,
        direccion,
        telefono,
        correo,
        gerente,
        equipo_contacto,
    ):
        self.id = id_
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.gerente = gerente
        self.equipo_contacto = equipo_contacto
        self.__proyectos = ArbolBinario()

    @property
    def proyectos(self):
        "Árbol binario de proyectos de la empresa."
        return self.__proyectos

    @staticmethod
    def validar_atributos(atributos):
        "Valida los atributos de la clase Empresa"
        try:
            _comprobar_nombres_de_atributos(_NOMBRES_ATRIBUTOS, atributos)
        except AttributeError as e:
            raise AttributeError(_MSG_ERROR_ATRIBUTO_INEXISTENTE % e.args[0])

    def agregar_proyecto(self, proyecto):
        "Agrega un 'Proyecto' a la empresa, solo si no está ya incluida."
        if self.buscar_proyecto_por_id(proyecto.id) is None:
            self.__proyectos.insertar(ClaveValor(proyecto.id, proyecto))

    def buscar_proyecto(self, atributo, valor):
        """Busca el primer proyecto cuyo atributo sea el valor dado.

        Véase la documentación de Proyecto.buscar_tarea.
        """
        return util.buscar_por_atributo((par.valor for par in self.__proyectos),
                                        atributo, valor)

    def buscar_proyecto_por_id(self, id_):
        """Busca un proyecto por ID eficientemente.

        Devuelve None si no se encuentra el proyecto buscado."""
        util.comprobar_tipos("id", id_, int)
        par = self.__proyectos.buscar(ClaveValor(id_, None))
        return par.valor if par is not None else None

    def eliminar_proyecto(self, proyecto):
        util.comprobar_tipos("proyecto", proyecto, Proyecto)
        self.__proyectos.remover(ClaveValor(proyecto.id, None))

    def modificar(self, atributos):
        """Modifica los atributos de esta empresa.

        Véase la documentación de Proyecto.modificar"""
        Proyecto.modificar(self, atributos)

    def __format__(self, formato):
        if formato == "":
            return str(self)
        elif formato != "g":
            raise ValueError("la especificación de formato debe ser '' o 'g'")
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}"',
                     'Descripción:\n{descripcion}',
                     'Fecha de creación: {fecha_creacion}',
                     'Dirección:\n{direccion}',
                     'Teléfono: {self.telefono}',
                     'Correo: {self.correo}',
                     'Gerente: {self.gerente}',
                     'Equipo de contacto: {self.equipo_contacto}',
                     'No. de proyectos: {cant_proyectos}']
        resultado = "\n".join(resultado)
        resultado = resultado.format(
            self=self,
            fecha_creacion=util.fecha_a_str(self.fecha_creacion),
            cant_proyectos=len(self.__proyectos),
            descripcion=util.envolver_y_sangrar(self.descripcion),
            direccion=util.envolver_y_sangrar(self.direccion)
        )
        return resultado

    def __str__(self):
        resultado = ['ID: {self.id}',
                     'Nombre: "{self.nombre}"', ]
        resultado = "\n".join(resultado)
        return resultado.format(self=self)


class Proyecto:
    """Proyecto

    El 'id' debe ser un entero, y las fechas datetime.date.
    Por ahora no hay más restricciones, y las presentes no se imponen.
    """

    _NOMBRES_ATRIBUTOS = (
        "id", "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
        "estado", "empresa", "gerente", "equipo", "_Proyecto__tareas")
    _MSG_ERROR_ATRIBUTO_INEXISTENTE = "Los 'Proyecto's no tienen atributo '%s'"

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

    @staticmethod
    def validar_atributos(atributos):
        "Valida los atributos de la clase Proyecto"
        try:
            _comprobar_nombres_de_atributos(_NOMBRES_ATRIBUTOS, atributos)
        except AttributeError as e:
            raise AttributeError(_MSG_ERROR_ATRIBUTO_INEXISTENTE % e.args[0])

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

    def eliminar_tarea(self, tarea):
        util.comprobar_tipos("tarea", tarea, Tarea)
        self.__tareas.remover_nodo(tarea, padre=self.__tareas.raiz)

    def modificar(self, atributos):
        """Modifica los atributos de este proyecto.

        'atributos' debe ser un diccionario que contenga los atributos
        que se desean modificar.  Se levanta una excepción AttributeError
        si algún atributo no pertence a la clase Proyecto.

        Si hay algún valor inválido, se levanta un ValueError."""
        self.validar_atributos(atributos)
        for nombre, valor in atributos.items():
            setattr(self, nombre, valor)

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

    _NOMBRES_ATRIBUTOS = (
        "id", "nombre", "descripcion", "fecha_inicio", "fecha_vencimiento",
        "estado", "porcentaje", "empresa_cliente", "_Tarea__subtareas")
    _MSG_ERROR_ATRIBUTO_INEXISTENTE = "Las 'Tarea's no tienen atributo '%s'"

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

    @staticmethod
    def validar_atributos(atributos):
        "Valida los atributos de la clase Tarea"
        try:
            _comprobar_nombres_de_atributos(_NOMBRES_ATRIBUTOS, atributos)
        except AttributeError as e:
            raise AttributeError(_MSG_ERROR_ATRIBUTO_INEXISTENTE % e.args[0])

    def agregar_subtarea(self, tarea):
        "Agrega una 'Tarea' como subtarea, solo si no está ya incluida."
        if self.buscar_subtarea("id", tarea.id) is None:
            self.__tareas.insertar_nodo(tarea.subtareas.raiz,
                                        self.__subtareas.raiz)

    def buscar_subtarea(self, atributo, valor):
        """Busca la primera subtarea cuyo atributo sea el valor dado.

        Véase la documentación de Proyecto.buscar_tarea.
        """
        iterador = self.__subtareas.en_anchura()
        next(iterador)  # Descartar raíz
        return util.buscar_por_atributo(iterador, atributo, valor)

    def eliminar_subtarea(self, tarea):
        util.comprobar_tipos("tarea", tarea, Tarea)
        self.__subtareas.remover_nodo(tarea, padre=self.__subtareas.raiz)

    def modificar(self, atributos):
        """Modifica los atributos de esta tarea.

        Véase la documentación de Proyecto.modificar"""
        Proyecto.modificar(self, atributos)

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
    __MSG_ERROR_EMPRESA_NO_ID = "No existe una empresa con ese ID: "
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

    def agregar_empresa(self, atributos, forzar=False):
        """Agrega una nueva 'Empresa' al sistema de gestión.

        'atributos' debe ser un diccionario que contenga los argumentos
        requeridos por el constructor de Empresa, excepto el ID.

        Si se provee un 'id', también se tiene que forzar la operación;
        de lo contrario, se levanta una excepción ValueError"""
        if not forzar:
            if "id_" in atributos:
                raise ValueError("No se puede especificar un ID")
        elif "id" in atributos:
            if "id_" in atributos:
                del atributos["id"]
            else:
                atributos["id_"] = atributos.pop("id")
        if "id_" not in atributos:
            self.id_empresa_max += 1
            atributos["id_"] = self.id_empresa_max
        elif self.__empresas.buscar_por_atributo("id", atributos["id_"]) \
            is not None:
            raise ValueError("Ya existe una empresa con ese ID")
        elif atributos["id_"] > self.id_empresa_max:
            self.id_empresa_max = atributos["id_"]

        empresa = Empresa(**atributos)
        self.__empresas.anexar(empresa)
        return empresa

    def buscar_empresa(self, atributo, valor):
        """Busca la primera empresa cuyo atributo sea el valor dado.

        Véase la documentación de Proyecto.buscar_tarea.
        """
        return util.buscar_por_atributo(self.__empresas, atributo, valor)

    def modificar_empresa(self, atributos):
        if "id_" in atributos:
            if "id" in atributos:
                del atributos["id_"]
            else:
                atributos["id"] = atributos.pop("id_")
        id_ = atributos.pop("id")
        empresa = self.buscar_empresa("id", id_)
        if empresa is None:
            raise ValueError(Gestor.__MSG_ERROR_EMPRESA_NO_ID + str(id_))
        empresa.modificar(atributos)

    def eliminar_empresa(self, id_):
        empresa = self.buscar_empresa("id", id_)
        if empresa is None:
            raise ValueError(Gestor.__MSG_ERROR_EMPRESA_NO_ID + str(id_))
        self.__empresas.remove(empresa)

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
        if self.empresa.buscar_proyecto_por_id(proyecto.id) is None:
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

    def guardar_empresas_en_csv(self, ruta_archivo_csv):
        with open(ruta_archivo_csv, mode="w", newline="", encoding="utf-8") \
            as archivo:
            nombres_atributos = list(Empresa._NOMBRES_ATRIBUTOS)
            nombres_atributos.remove("_Empresa__proyectos")
            escritor = csv.writer(archivo)
            escritor.writerow(nombres_atributos + ["proyectos"])
            indice_fecha = nombres_atributos.index("fecha_creacion")
            nombres_atributos.pop(indice_fecha)
            for empresa in self.empresas:
                serializacion = [getattr(empresa, nombre)
                                 for nombre in nombres_atributos]
                serializacion.insert(indice_fecha,
                                     util.fecha_a_str(empresa.fecha_creacion))
                id_proyectos = [proyecto.id for proyecto in empresa.proyectos]
                serializacion.append(str(id_proyectos))
                escritor.writerow(serializacion)
