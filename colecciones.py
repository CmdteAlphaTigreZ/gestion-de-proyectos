# Biblioteca de clases abstractas y concretas de colecciones
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-07-01
# Cambios:
#   v1
#     * Versión inicial
#   v2
#     * Funciones de búsqueda
#     * Conversiones a 'str'
#     * NodoArbolBinario

import utilidades as util


class ClaveValor:
    """Par de clave y valor que se compara en términos de su clave.

    No se debería cambiar directamente sus atributos una vez que forma parte
    de una estructura que lo utiliza para realizar ordenamientos.
    Esto no se impone; sin embargo, el funcionamiento correcto de estas
    estructuras dependen de ello."""

    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor

    def __eq__(self, otro):
        if not isinstance(otro, ClaveValor):
            return NotImplemented
        return self.clave == otro.clave

    def __ne__(self, otro):
        return not self == otro

    def __lt__(self, otro):
        if not isinstance(otro, ClaveValor):
            return NotImplemented
        return self.clave < otro.clave

    def __le__(self, otro):
        return self < otro or self == otro

    def __gt__(self, otro):
        return not self <= otro

    def __ge__(self, otro):
        return not self < otro

class Vista:
    "Vista de solo lectura de una colección."

    def __init__(self, coleccion, funcion_obtener=None, funcion_tamano=None):
        self.__coleccion = coleccion
        self.__obtener = self.__tamano = None
        if funcion_obtener is not None:
            self.__obtener = funcion_obtener
        else:
            for nombre in ("obtener", "buscar", "get", "__getitem__"):
                if hasattr(type(coleccion), nombre):
                    self.__obtener = getattr(type(coleccion), nombre)
        if self.__obtener is None:
            raise TypeError("Función para obtener de colección desconocida")
        elif not hasattr(type(self.__obtener), "__call__"):
            raise TypeError("obtener no es llamable")

        if funcion_tamano is not None:
            self.__tamano = funcion_tamano
        else:
            for nombre in ("largo", "longitud", "tamano", "__len__", "size"):
                if hasattr(type(coleccion), nombre):
                    self.__tamano = getattr(type(coleccion), nombre)
        if self.__tamano is not None:
            try:
                int(funcion_tamano(self.__coleccion))
            except (TypeError, ValueError) as e:
                raise TypeError("tamano no es válido") from e
        else:
            self.__tamano = len

    def __getitem__(self, clave):
        return self.__obtener(self.__coleccion, clave)

    def __len__(self):
        return self.__tamano(self.__coleccion)

    @property
    def tipo(self):
        return type(self.__coleccion)

    def __repr__(self):
        return "Vista(%r)" % self.tipo


class NodoLista:
    "Nodo doblemente enlazado conteniendo un valor cualquiera."

    def __init__(self, valor=None):
        self.valor = valor
        self.__nodo_anterior = None
        self.__nodo_siguiente = None
        self.__repr = False  # Para __repr__

    def anterior(self):
        return self.__nodo_anterior

    def siguiente(self):
        return self.__nodo_siguiente

    def enlazar_a(self, siguiente):
        "Enlaza al 'NodoLista' como el siguiente"
        if siguiente is not None:
            util.comprobar_tipos("siguiente", siguiente, NodoLista)
        self.__nodo_siguiente = siguiente
        if siguiente is not None:
            siguiente.__nodo_anterior = self

    def enlazar_desde(self, anterior):
        "Enlaza al 'NodoLista' como el anterior"
        if anterior is not None:
            util.comprobar_tipos("anterior", anterior, NodoLista)
        self.__nodo_anterior = anterior
        if anterior is not None:
            anterior.__nodo_siguiente = self

    def __repr__(self):
        if self.__repr:
            return "..."
        else:
            self.__repr = True
            resultado = "NodoLista(%r)" % self.valor
            self.__repr = False
            return resultado

class ListaEnlazada:
    "Lista doblemente enlazada heterogénea."

    __ERROR_NO_SLICE = NotImplementedError("sin soporte para 'slice'")

    def __init__(self, iterable=None):
        "Se copian los elementos de 'iterable' si se proporciona."
        self.__cabeza = None
        self.__cola = None
        self.__longitud = 0
        if iterable is not None:
            self.extender(iterable)
        self.__str = False  # Para __str__

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
        nuevo = NodoLista(valor)
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
        nuevo = NodoLista(valor)
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
        "Evita un comportamiento indeseado con None, para asemejarse más a Python."
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
        else:
            self.__cabeza = None
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
                self.__cola = None
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

    def __iadd__(self, iterable):
        "Anexa todos los elementos de iterable a la lista"
        iterable = iter(iterable)
        # Copiado de 'anexar' para evitar la comparación innecesaria
        # de la cabeza con 'None'.  Mantener sincronizado con 'anexar'
        if self.__cabeza is None:
            try:
                nuevo = NodoLista(next(iterable))
            except StopIteration:
                return
            self.__cabeza = self.__cola = nuevo
            self.__longitud += 1
        for valor in iterable:
            nuevo = NodoLista(valor)
            nuevo.enlazar_desde(self.__cola)
            self.__cola = nuevo
            self.__longitud += 1
        return self

    extender = __iadd__
    extend = extender

    def __add__(self, lista):
        if not isinstance(lista, ListaEnlazada):
            return NotImplemented
        union = ListaEnlazada()
        union += self
        union += lista
        return union

    # Véase la documentación de estas funciones en utilidades.py
    indice = util.indice
    index = indice

    buscar = util.buscar

    buscar_por_atributo = util.buscar_por_atributo

    def limpiar(self):
        "Vacía la lista"
        self.__cabeza = self.__cola = None
        self.__longitud = 0

    clear = limpiar

    def copiar(self):
        """Realiza una copia plana de la lista.

        Los nodos de la copia son independientes de la lista original,
        pero no necesariamente los valores.
        """
        return ListaEnlazada(self)

    copy = copiar

    class IteradorL2E:
        "Iterador de lista doblemente enlazada"

        def __init__(self, lista, adelante=True):
            "'adelante' indica la dirección de iteración"
            util.comprobar_tipos("lista", lista, ListaEnlazada)
            if adelante:
                self.__nodo = lista._ListaEnlazada__cabeza
                self.__funcion = NodoLista.siguiente
            else:
                self.__nodo = lista._ListaEnlazada__cola
                self.__funcion = NodoLista.anterior

        def __iter__(self):
            return self

        def __next__(self):
            if self.__nodo is None:
                raise StopIteration()
            valor = self.__nodo.valor
            self.__nodo = self.__funcion(self.__nodo)
            return valor

    def __iter__(self):
        "Devuelve un iterador eficiente sobre la lista enlazada."
        return self.IteradorL2E(self)

    def __reversed__(self):
        "Devuelve un iterador reverso eficiente sobre la lista enlazada."
        return self.IteradorL2E(self, adelante=False)

    def __str__(self):
        # Así funciona 'list'.
        if self.__str:
            # Protección contra llamadas recursivas
            return "[...]"
        else:
            self.__str = True
            resultado = "[%s]" % ", ".join(map(repr, self))
            self.__str = False
            return resultado

    def __repr__(self):
        return "ListaEnlazada(%s)" % self


class NodoArbolBinario():
    "Nodo de un árbol binario."

    def __init__(self, valor=None):
        self.valor = valor
        self.__nodo_padre = None
        self.__nodo_izquierdo = None
        self.__nodo_derecho = None
        self.__repr = False  # Para __repr__

    def padre(self):
        return self.__nodo_padre

    def izquierdo(self):
        return self.__nodo_izquierdo

    def derecho(self):
        return self.__nodo_derecho

    def enlazar_a_izquierdo(self, izquierdo):
        "Enlaza al 'NodoArbolBinario' como el izquierdo"
        if izquierdo is not None:
            util.comprobar_tipos("izquierdo", izquierdo, NodoArbolBinario)
        self.__nodo_izquierdo = izquierdo
        if izquierdo is not None:
            izquierdo.__nodo_padre = self

    def enlazar_a_derecho(self, derecho):
        "Enlaza al 'NodoArbolBinario' como el derecho"
        if derecho is not None:
            util.comprobar_tipos("derecho", derecho, NodoArbolBinario)
        self.__nodo_derecho = derecho
        if derecho is not None:
            derecho.__nodo_padre = self

    def desenlazar_padre(self):
        "Desenlaza el 'NodoArbolBinario' padre."
        " También desenlaza este nodo en el padre."
        if self.__nodo_padre is not None:
            if self == self.__nodo_padre.__nodo_izquierdo:
                self.__nodo_padre.__nodo_izquierdo = None
            elif self == self.__nodo_padre.__nodo_derecho:
                self.__nodo_padre.__nodo_derecho = None
            self.__nodo_padre = None

    def __repr__(self):
        if self.__repr:
            return "..."
        else:
            self.__repr = True
            resultado = "NodoArbolBinario(%r)" % self.valor
            self.__repr = False
            return resultado

class ArbolBinario:

    PREORDEN = -1
    INORDEN = 0
    POSTORDEN = 1

    ERROR_VALOR_INEXISTENTE = "El valor no está presente en el árbol: "

    def __init__(self, iterable=None):
        #"Se copian los elementos de 'iterable' si se proporciona."
        self.__raiz = None
        self._ultimo_padre = None
        self._ultimo_nodo = None
        if iterable is not None:
            self.extender(iterable)

    def __len__(self):
        cuenta = -1
        # Preorden es más eficiente
        for cuenta, ignorar in enumerate(self.preorden()):
            pass
        return cuenta + 1

    tamano = __len__

    def __buscar_padre(self, valor, raiz=None):
        """Busca el padre que tendría un nodo con el 'valor' dado.

        Devuelve un par (tuple) con el padre respectivo en este
        arbol binario, buscando el hijo a partir de 'raiz', y un entero
        entre -1, 0 y 1 que indique en qué posición iría el nodo
        con el valor dado como hijo.

        Para la izquierda, devuelve -1.  Para la derecha, devuelve 1.
        Devuelve (None, 0) cuando no hay padre para un nodo con tal valor.
        El último caso implica que el nodo correspondería a la raíz.

        En cualquier caso, el nodo con tal valor podría o no existir
        actualmente en el árbol.
        """
        if raiz is not None:
            padre = raiz.padre()
            hijo = raiz
        else:
            padre = None
            hijo = self.__raiz
        while hijo is not None:
            if valor == hijo.valor:
                break
            padre = hijo
            if valor < padre.valor:
                hijo = padre.izquierdo()
            elif valor > padre.valor:
                hijo = padre.derecho()
            else:
                raise TypeError("valor no ordenado")
        if padre is None:
            posicion = 0
        elif valor < padre.valor:
            posicion = -1
        else:
            posicion = 1
        return padre, posicion

    def __buscar(self, valor):
        "Obtiene el nodo cuyo valor se compara igual con el valor dado."
        padre, posicion = self.__buscar_padre(valor)
        if padre is None:
            nodo_encontrado = self.__raiz
        elif posicion == -1:
            nodo_encontrado = padre.izquierdo()
        else:
            nodo_encontrado = padre.derecho()
        return nodo_encontrado

    def buscar(self, valor):
        """Obtiene el elemento que se compare igual con el valor dado.

        Devuelve None si no se encuentra dicho elemento."""
        nodo_encontrado = self.__buscar()
        return nodo_encontrado.valor if nodo_encontrado is not None else None

    def __insertar_aux(self, nodo, valor, cambiar):
        "Si cambiar es True, levanta KeyError, de lo contrario cambia"
        " el valor del nodo por 'valor' y devuelve el valor anterior."
        " El nodo no puede ser None."
        if not cambiar:
            raise KeyError("El valor ya está presente en el árbol: %s == %s"
                           % (valor, nodo.valor))
        self._ultimo_nodo = None  # Si no hay adición (pero cambio), señalizarlo
        anterior, nodo.valor = nodo.valor, valor
        return anterior

    def insertar(self, valor, cambiar=False):
        """Inserta el valor en el árbol binario.

        Si el valor ya está presente y cambiar es False, levanta una
        excepción KeyError.  Si cambiar es True, cambia el elemento
        por el valor dado y devuelve el elemento anterior.
        Si cambiar es False y la inserción tiene éxito devuelve None.
        """
        padre, posicion = self.__buscar_padre(valor)
        anterior = None
        if padre is None:
            if self.__raiz is None:
                self.__raiz = self._ultimo_nodo = NodoArbolBinario(valor)
            else:
                anterior = self.__insertar_aux(self.__raiz, valor, cambiar)
        elif posicion == -1:
            if padre.izquierdo() is None:
                self._ultimo_nodo = NodoArbolBinario(valor)
                padre.enlazar_a_izquierdo(self._ultimo_nodo)
            else:
                anterior = self.__insertar_aux(padre.izquierdo(),
                                               valor, cambiar)
        else:
            if padre.derecho() is None:
                self._ultimo_nodo = NodoArbolBinario(valor)
                padre.enlazar_a_derecho(self._ultimo_nodo)
            else:
                anterior = self.__insertar_aux(padre.derecho(), valor, cambiar)
        return anterior if cambiar else None

    insert = insertar

    def agregar(self, valor):
        "Agrega el valor al árbol. Levanta KeyError si ya está presente."
        self.insertar(valor, cambiar=False)

    add = agregar

    def cambiar(self, valor_viejo, valor_nuevo):
        """Cambiar el valor del nodo con el valor viejo por el valor nuevo.

        Devuelve el valor anterior."""
        nodo = self.__buscar(valor_viejo)
        if nodo is None:
            raise KeyError(self.ERROR_VALOR_INEXISTENTE + str(valor_viejo))
        return self.__insertar_aux(nodo, valor_nuevo, cambiar=True)

    def extender(self, iterable):
        "Inserta los elementos de iterable en el árbol, eliminando duplicados."
        for valor in iterable:
            self.insertar(valor, cambiar=True)

    extend = extender

    def __minmax_nodo(self, padre, posicion):
        if padre is None:
            return None
        if posicion == -1:
            lado = NodoArbolBinario.izquierdo
        else:
            lado = NodoArbolBinario.derecho
        hijo = lado(padre)
        while hijo is not None:
            padre = hijo
            hijo = lado(padre)
        return padre

    def minimo(self):
        if self.__raiz is None:
            raise KeyError("el árbol está vacío")
        nodo = self.__minmax_nodo(self.__raiz, -1)
        return nodo.valor

    def maximo(self):
        if self.__raiz is None:
            raise KeyError("el árbol está vacío")
        nodo = self.__minmax_nodo(self.__raiz, 1)
        return nodo.valor

    def __remover_nodo(self, a_remover):
        if a_remover is None:
            return None
        padre = a_remover.padre()
        if padre is None or padre.derecho() is a_remover:
            este_lado = NodoArbolBinario.derecho
            otro_lado = NodoArbolBinario.izquierdo
            enlazar = NodoArbolBinario.enlazar_a_derecho
        else:
            este_lado = NodoArbolBinario.izquierdo
            otro_lado = NodoArbolBinario.derecho
            enlazar = NodoArbolBinario.enlazar_a_izquierdo

        if otro_lado(a_remover) is not None:
            if este_lado(a_remover) is not None:
                if este_lado(otro_lado(a_remover)) is None:
                    enlazar(otro_lado(a_remover), este_lado(a_remover))
                    reemplazo = otro_lado(a_remover)
                else:
                    posicion = -1 if este_lado is NodoArbolBinario.derecho \
                               else 1
                    extremo = self.__minmax_nodo(otro_lado(a_remover), posicion)
                    extremo.valor, a_remover.valor = \
                       a_remover.valor, extremo.valor
                    a_remover = extremo
                    self.__remover_nodo(a_remover)  # No es recursivo realmente
                    return a_remover  # Termina aquí. No hay más reemplazo
            else:
                reemplazo = otro_lado(a_remover)
        else:
            reemplazo = este_lado(a_remover)
        if padre is None:
            self.__raiz = reemplazo
            if reemplazo is not None:
                reemplazo.desenlazar_padre()
        else:
            enlazar(padre, reemplazo)
        self._ultimo_nodo = reemplazo
        self._ultimo_padre = padre
        #a_remover.desenlazar_padre()
        #a_remover.enlazar_a_izquierdo(None)
        #a_remover.enlazar_a_derecho(None)
        return a_remover

    def remover(self, valor):
        "Remueve el valor dado.  Levanta KeyError si no se halla."
        # ARREGLAR ESTO...
        a_remover = self.__buscar(valor)
        if a_remover is None:
            raise KeyError(self.ERROR_VALOR_INEXISTENTE + str(valor))
        a_remover = self.__remover_nodo(a_remover)  # Puede no ser el mismo
        return a_remover.valor

    remove = remover

    def limpiar(self):
        "Vacía el arbol"
        self.__raiz = None

    clear = limpiar

    def copiar(self):
        """Realiza una copia plana del árbol.

        Los nodos de la copia son independientes del árbol original,
        pero no necesariamente los valores.
        """
        return ArbolBinario(self.preorden())  # Primero los padres

    copy = copiar

    class IteradorArbolBinario:

        # Copiar el valor de ArbolBinario.INORDEN porque Python
        # no permite hacer referencia a la clase en los valores por defecto
        # de los métodos.
        def __init__(self, arbol, orden=0, nodos=False):
            util.comprobar_tipos("arbol", arbol, ArbolBinario)
            raiz = arbol._ArbolBinario__raiz
            if orden == ArbolBinario.PREORDEN:
                self.__pila = Pila()
                if raiz is not None:
                    self.__pila.insertar(raiz)
                self.__funcion = self.__preorden
            elif orden == ArbolBinario.INORDEN:
                self.__generador = self.__inorden_generador(raiz)
                self.__funcion = self.__inorden
            elif orden == ArbolBinario.POSTORDEN:
                self.__generador = self.__postorden_generador(raiz)
                self.__funcion = self.__postorden
            else:
                raise ValueError("Orden de recorrido inválido: " + str(orden))
            self.__nodos = nodos

        def __iter__(self): return self

        def __next__(self):
            if self.__nodos:
                return self.__funcion()
            else:
                return self.__funcion().valor

        def __preorden(self):
            if len(self.__pila) == 0:
                raise StopIteration()
            procesado = self.__pila.extraer()
            if procesado.derecho() is not None:
                self.__pila.insertar(procesado.derecho())
            if procesado.izquierdo() is not None:
                self.__pila.insertar(procesado.izquierdo())
            return procesado

        def __inorden_generador(self, nodo):
            if nodo is not None:
                yield from self.__inorden_generador(nodo.izquierdo())
                yield nodo
                yield from self.__inorden_generador(nodo.derecho())

        def __inorden(self):
            return next(self.__generador)

        def __postorden_generador(self, nodo):
            if nodo is not None:
                yield from self.__postorden_generador(nodo.izquierdo())
                yield from self.__postorden_generador(nodo.derecho())
                yield nodo

        def __postorden(self):
            return next(self.__generador)

    def __iter__(self):
        "Devuelve un iterador inorden del arbol binario"
        return self.IteradorArbolBinario(self)

    inorden = __iter__

    def preorden(self):
        "Devuelve un iterador preorden del arbol binario"
        return self.IteradorArbolBinario(self, ArbolBinario.PREORDEN)

    def postorden(self):
        "Devuelve un iterador postorden del arbol binario"
        return self.IteradorArbolBinario(self, ArbolBinario.POSTORDEN)

class ArbolAVL(ArbolBinario):
    pass

class NodoArbolNario:
    "Nodo de un árbol n-ario."

    def __init__(self, valor=None):
        self.valor = valor
        self.__nodo_padre = None
        self.__nodos_hijos = []
        self.__repr = False  # Para __repr__

    def padre(self):
        return self.__nodo_padre

    def hijos(self):
        "Devuelve una copia de los hijos"
        return Vista(self.__nodos_hijos, list.__getitem__)

    def raiz(self):
        raiz = self
        while raiz.__nodo_padre is not None:
            raiz = raiz.__nodo_padre
        return raiz

    def __len__(self):
        "Devuelve la cantidad de hijos"
        return len(self.__nodos_hijos)

    def __getitem__(self, indice):
        "Devuelve el hijo con posición en el índice dado."
        return self.__nodos_hijos[indice]

    def __setitem__(self, indice, hijo):
        """Cambia el hijo posicionado en 'indice' con 'hijo'.

        Para añadir uno nuevo, úsese el método 'agregar'"""
        util.comprobar_tipos("hijo", hijo, NodoArbolNario)
        self.__nodos_hijos[indice] = hijo
        hijo.__nodo_padre = self

    def __delitem__(self, indice):
        "Elimina el hijo con posición en el índice dado."
        del self.__nodos_hijos[indice]

    def agregar(self, hijo_s):
        "Agrega uno o varios hijos nuevos al nodo."
        varios = True
        try:
            hijo_s = list(hijo_s)
        except TypeError:
            varios = False
        if varios:
            util.comprobar_tipos(("hijo",) * len(hijo_s), hijo_s,
                                 (NodoArbolNario,) * len(hijo_s) )
            self.__nodos_hijos += hijo_s
            for hijo in hijo_s:
                hijo.__nodo_padre = self
        else:
            util.comprobar_tipos("hijo", hijo_s, NodoArbolNario)
            self.__nodos_hijos.append(hijo_s)
            hijo_s.__nodo_padre = self

    def remover(self, hijo):
        "Elimina un hijo por identidad.  Devuelve un booleano indicando éxito."
        util.comprobar_tipos("hijo", hijo, NodoArbolNario)
        try:
            self.__nodos_hijos.remove(hijo)
            return True
        except ValueError:
            return False

    def desenlazar_padre(self):
        "Desenlaza el 'NodoArbolBinario' padre."
        " También desenlaza este nodo en el padre."
        if self.__nodo_padre is not None:
            self.__nodo_padre.remover(self)
            self.__nodo_padre = None

    def __repr__(self):
        if self.__repr:
            return "..."
        else:
            self.__repr = True
            resultado = "NodoArbolNario(%r)#%d" % (self.valor, len(self))
            self.__repr = False
            return resultado

class ArbolNario:
    pass


class Secuencia:
    "Interfaz común para varias colecciones secuenciales"

    def __init__(self, iterable=None):
        # Almacen de datos de soporte para la interfaz, por ahora ListaEnlazada
        self._soporte = ListaEnlazada(iterable)

    def __len__(self): return len(self._soporte)
    largo = __len__

    def __getitem__(self, indice): return self._soporte[indice]
    obtener = __getitem__

    def __setitem__(self, indice, valor): self._soporte[indice] = valor
    cambiar = __setitem__

    def indice(self, valor_buscado): return self._soporte.indice(valor_buscado)
    index = indice

    def __iadd__(self, iterable):
        self._soporte += iterable
        return self
    extender = __iadd__
    extend = extender

    def __add__(self, secuencia):
        if isinstance(secuencia, type(self)):
            tipo = type(self)
        elif isinstance(self, type(secuencia)):
            tipo = type(secuencia)
        else:
            return NotImplemented
        union = tipo()
        union += self
        union += secuencia
        return union

    def buscar(self, funcion): return self._soporte.buscar(funcion)

    def buscar_por_atributo(self, nombre, valor):
        return self._soporte.buscar_por_atributo(nombre, valor)

    def limpiar(self): self._soporte.limpiar()
    clear = limpiar

    def __iter__(self): return iter(self._soporte)

    def __str__(self): return str(self._soporte)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, self)

class Lista(ListaEnlazada, Secuencia):
    pass

class Pila(Secuencia):
    "Pila: el último elemento insertado es el primero extraído."

    def __init__(self, iterable=None):
        super().__init__(iterable)
        self._ListaEnlazada__str = False  # Para __str__

    def insertar(self, valor):
        "Inserta 'valor' en la cima de la pila.  Admite None."
        self._soporte.anexar(valor)
    push = insertar

    def extraer(self):
        "Extrae el valor en la cima de la pila."
        return self._soporte.extraer_ultimo()
    pop = extraer

    def __iter__(self): return reversed(self._soporte)

    # Conveniencia para self[0]
    @property
    def cima(self): return self[len(self) - 1]

    __str__ = ListaEnlazada.__str__

class Cola(Secuencia):
    "Cola: el primer elemento anexado es el primero extraído."

    def anexar(self, valor):
        "Anexa 'valor' al final de la cola."
        self._soporte.anexar(valor)
    append = anexar

    def extraer(self):
        "Extrae el valor en el frente de la cola."
        return self._soporte.extraer(0)
    pop = extraer

    # Conveniencia para self[0]
    @property
    def frente(self): return self[0]
