# Biblioteca de clases abstractas y concretas de colecciones
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-06-14
# Cambios:
#   v1
#     * Versión inicial

import utilidades as util

class Nodo:
    "Nodo doblemente enlazado conteniendo un valor cualquiera"

    def __init__(self, valor=None):
        self.valor = valor
        self.__nodo_anterior = None
        self.__nodo_siguiente = None

    def anterior(self):
        return self.__nodo_anterior

    def siguiente(self):
        return self.__nodo_siguiente

    def enlazar_a(self, siguiente):
        "Enlaza al 'Nodo' como el siguiente"
        util.comprobar_tipos("siguiente", siguiente, Nodo)
        self.__nodo_siguiente = siguiente
        if siguiente is not None:
            siguiente.__nodo_anterior = self

    def enlazar_desde(self, anterior):
        "Enlaza al 'Nodo' como el anterior"
        util.comprobar_tipos("anterior", anterior, Nodo)
        self.__nodo_anterior = anterior
        if anterior is not None:
            anterior.__nodo_siguiente = self

class ListaEnlazada:
    "Lista doblemente enlazada heterogénea"

    __ERROR_NO_SLICE = NotImplementedError("sin soporte para 'slice'")

    def __init__(self, iterable=None):
        self.__cabeza = None
        self.__cola = None
        self.__longitud = 0
        if iterable is not None:
            iterable = iter(iterable)
            # Copiado de 'anexar' para evitar la comparación innecesaria
            # de la cabeza con 'None'.  Mantener sincronizado con 'anexar'
            try:
                nuevo = Nodo(next(iterable))
            except StopIteration:
                return
            self.__cabeza = self.__cola = nuevo
            self.__longitud += 1
            for valor in iterable:
                nuevo = Nodo(valor)
                nuevo.enlazar_desde(self.__cola)
                self.__cola = nuevo
                self.__longitud += 1

    def __len__(self): return self.__longitud

    largo = __len__

    def __validar_indice(self, indice):
        if indice < 0 or indice >= self.__longitud:
            raise IndexError(str(indice))

    # Idealmente debería ser privado, pero se hace así para simplificar
    # ^ Esto era en Java, por ahora no parece haber problema con hacerlo
    #   privado, pero se puede revertir el cambio si es necesario
    def __obtener_nodo(self, indice):
        self.__validar_indice(indice)
        if indice < self.__longitud // 2:
            nodo = self.__cabeza
            for i in range(indice):
                nodo = nodo.siguiente()
        else:
            nodo = self.__cola
            for i in range(indice):
                nodo = nodo.anterior()
        return nodo

    def __getitem__(self, indice):
        if isinstance(indice, slice):
            raise __ERROR_NO_SLICE
        return self.__obtener_nodo(indice).valor

    obtener = __getitem__

    def __setitem__(self, indice, valor):
        if isinstance(indice, slice):
            raise __ERROR_NO_SLICE
        self.__obtener_nodo(indice).valor = valor

    cambiar = __setitem__

    def anexar(self, valor):
        nuevo = Nodo(valor)
        nuevo.enlazar_desde(self.__cola)
        self.__cola = nuevo
        if self.__cabeza is None:
            self.__cabeza = nuevo
        self.__longitud += 1

    append = anexar

    def insertar(self, indice, valor=None):
        """
        insertar(valor), inserta al comienzo
        insertar(indice, valor), inserta en la posición indicada
        No se puede insertar nulos con este método, para eso
        inserte un valor arbitrario y luego cámbielo con
        lista[i] = valor; si lo intenta estaría insertando al inicio
        """
        if valor is None:
            valor = indice
            indice = 0
        if indice == self.__longitud:
            self.anexar(valor)
            return
        nuevo = Nodo(valor)
        if indice == 0:
            nuevo.enlazar_a(self.__cabeza)
            self.__cabeza = nuevo
            if self.__cola is None:
                self.__cola = nuevo
        else:
            self.__validar_indice(indice)
            anterior = self.__obtener_nodo(indice - 1)
            nuevo.enlazar_a(anterior.siguiente())
            anterior.enlazar_a(nuevo)
        self.__longitud += 1

    def insert(self, indice, valor):
        if valor is None:
            raise TypeError("valor no puede ser 'None'")

    def extraer_ultimo(self):
        if self.__cola is None:
            raise IndexError("la lista está vacía")
        a_extraer = self.__cola
        self.__cola = self.__cola.anterior()
        if self.__cola is not None:
            a_extraer.enlazar_desde(None)
            self.__cola.enlazar_a(None)
        self.__longitud -= 1
        return a_extraer.valor

    def extraer(self, indice=None):
        if indice is None:
            indice = 0
        if indice == self.__longitud - 1:
            return self.extraer_ultimo()
        if indice == 0:
            if self.__cabeza is None:
                raise IndexError("la lista está vacía")
            a_extraer = self.__cabeza
            self.__cabeza = self.__cabeza.siguiente()
            if self.__cabeza is not None:
                a_extraer.enlazar_a(None)
                self.__cabeza.enlazar_desde(None)
        else:
            self.__validar_indice(indice)
            anterior = self.__obtener_nodo(indice - 1)
            a_extraer = anterior.siguiente()
            anterior.enlazar_a(a_extraer.siguiente())
            a_extraer.enlazar_desde(None)
            a_extraer.enlazar_a(None)
        self.__longitud -= 1
        return a_extraer.valor

    pop = extraer

    def __delitem__(self, indice):
        self.extraer(indice)

    def limpiar(self):
        "Vacía la lista"
        self.__cabeza = self.__cola = None
        self.__longitud = 0

    clear = limpiar

    def copiar(self):
        return ListaEnlazada(self)

    copy = copiar

    class IteradorL2E:
        "Iterador de lista doblemente enlazada"

        def __init__(self, lista, adelante=True):
            util.comprobar_tipos("lista", lista, ListaEnlazada)
            if adelante:
                self.__nodo = lista._ListaEnlazada__cabeza
                self.__funcion = Nodo.siguiente
            else:
                self.__nodo = lista._ListaEnlazada__cola
                self.__funcion = Nodo.anterior

        def __iter__(self):
            return self

        def __next__(self):
            if self.__nodo is None:
                raise StopIteration()
            valor = self.__nodo.valor
            self.__nodo = self.__funcion(self.__nodo)
            return valor

    def __iter__(self):
        return self.IteradorL2E(self)

    def __reversed__(self):
        return self.IteradorL2E(self, adelante=False)


class Secuencia:

    def __init__(self, iterable=None):
        # Almacen de datos de soporte para la interfaz, por ahora ListaEnlazada
        self.__soporte = ListaEnlazada(iterable)

    def __len__(self): return len(self.__soporte)
    largo = __len__

    def __getitem__(self, indice): return self.__soporte[indice]
    obtener = __getitem__

    def __setitem__(self, indice, valor): self.__soporte[indice] = valor
    cambiar = __setitem__

    def limpiar(self): self.__soporte.limpiar()
    clear = limpiar

    def __iter__(self): return iter(self.__soporte)

class Lista(ListaEnlazada, Secuencia):
    pass

class Pila(Secuencia):

    def insertar(self, valor):
        if valor is None:
            self.__soporte.insertar(0, 0)
            self.__soporte[0] = None
        else:
            self.__soporte.insertar(0, valor)
    push = insertar

    def extraer(self): return self.__soporte.extraer(0)
    pop = extraer

    # Conveniencia para self[0]
    @property
    def cima(self): return self[0]

class Cola(Secuencia):

    def anexar(self, valor): self.__soporte.anexar(valor)
    append = anexar

    def extraer(self): return self.__soporte.extraer_ultimo()
    pop = extraer

    # Conveniencia para self[0]
    @property
    def frente(self): return self[0]


# Implementaciones alternativas pero algo más complicadas de hacer funcionar
##class Pila:
##
##    def __init__(self, iterable=None):
##        ListaEnlazada.__init__(self, iterable)
##        self.__cima = self._ListaEnlazada__cabeza
##
##    __len__ = ListaEnlazada.__len__
##    largo = __len__
##
##    #__validar_indice = ListaEnlazada._ListaEnlazada__validar_indice
##    #__obtener_nodo = ListaEnlazada._ListaEnlazada__obtener_nodo
##
##    #__getitem__ = ListaEnlazada.__getitem__
##    #__setitem__ = ListaEnlazada.__setitem__
##    #__delitem__ = ListaEnlazada.__delitem__
##
##    insertar = ListaEnlazada.insertar
##    extraer = ListaEnlazada.extraer
##    pop = ListaEnlazada.pop
##    push = insertar
##
##    limpiar = ListaEnlazada.limpiar
##    clear = limpiar
##
##    def __iter__(self):
##        return ListaEnlazada.IteradorL2E(self)
##
##class Cola:
##
##    def __init__(self, iterable=None):
##        ListaEnlazada.__init__(self, iterable)
##        self.__inicio = self._ListaEnlazada__cabeza
##        self.__fin = self._ListaEnlazada__cola
##
##    __len__ = ListaEnlazada.__len__
##    largo = __len__
##
##    #__validar_indice = ListaEnlazada._ListaEnlazada__validar_indice
##    #__obtener_nodo = ListaEnlazada._ListaEnlazada__obtener_nodo
##
##    #__getitem__ = ListaEnlazada.__getitem__
##    #__setitem__ = ListaEnlazada.__setitem__
##    #__delitem__ = ListaEnlazada.__delitem__
##
##    anexar = ListaEnlazada.anexar
##    extraer = ListaEnlazada.extraer
##    pop = ListaEnlazada.pop
##    append = anexar
##
##    limpiar = ListaEnlazada.limpiar
##    clear = limpiar
##
##    def __iter__(self):
##        return ListaEnlazada.IteradorL2E(self)

