# Biblioteca de utilidades genéricas de programación
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-07-01
# Cambios:
#   v1
#     * Versión inicial
#   v2
#     * Función de formato estilo párrafo (envolver_y_sangrar)
#     * Funciones de búsqueda en iterables
#     * Comprobación de tipos simplificada


from datetime import datetime

# Definición de tipo 'funcion_t' para usarse en validación de tipos
def f():
    pass
funcion_t = type(f)
del f

# Definición de tipo 'metodo_t', misma idea
class A:
    def f():
        pass
metodo_t = type(A().f)
del A


def comprobar_tipos(nombres, valores, tipos):
    """Comprueba los tipos de los valores, generando una excepción con \
    el nombre del primer valor inválido si lo hay

    Los tres argumentos deben ser secuencias de igual longitud:
    nombres debe contener datos tipo 'str'
    valores debe contener datos tipo 'tipo'
    tipos debe contener datos tipo 'type' que representen el 'tipo' del valor

    Alternativamente, si nombres es tipo 'str' en sí, los argumentos
    se toman como los valores directos en lugar de secuencias.
    Permite comprobar el tipo de un solo valor sin insertarlo en una
    secuencia previamente.
    """
    unico = isinstance(nombres, str)
    if unico:
        if not isinstance(valores, tipos):
            raise TypeError("'%s' no es de tipo '%s': %s"
                            % (nombres, tipos.__name__, valores))
    else:
        if not len(nombres) == len(valores) == len(tipos):
            raise ValueError(
                "debe haber la misma cantidad de nombres, valores y tipos")
        for nombre, valor, tipo in zip(nombres, valores, tipos):
            if not isinstance(valor, tipo):
                raise TypeError("'%s' no es de tipo '%s': %s"
                                % (nombre, tipo.__name__, valor))

def str_a_fecha(fecha):
    "Convierte fechas en formato 'DD-MM-YYYY' a 'datetime.date'"
    return datetime.strptime(fecha, "%d/%m/%Y").date()

def fecha_a_str(fecha):
    "Convierte fechas 'datetime.date' al formato 'DD-MM-YYYY'"
    return fecha.strftime("%d/%m/%Y")

def envolver_y_sangrar(texto, ancho=72, sangrado=2):
    """Inserta saltos de línea y sangra texto para salida formateada.

    El ancho corresponde con el ancho total del texto resultante,
    incluyendo el sangrado.  El ancho no vacío de la columna de texto
    es ancho - sangrado.
    """
    ancho -= sangrado
    if ancho < 1: raise ValueError("El ancho debe ser mayor que el sangrado")
    sangrado = " " * sangrado
    i = 0; len_texto = len(texto)
    resultado = []
    texto = texto.split(" ")
    len_palabras = len(texto) - 1   # Cuenta una por adelantado
    while len_texto > 0:
        j = i + 1; len_linea = len(texto[i]); linea = ""
        while j <= len_palabras:
            len_linea += len(texto[j]) + 1
            if len_linea > ancho:
                break
            j += 1
        if j != len_palabras + 1:   # Se contó una palabra de más
            len_linea -= len(texto[j])
        if len(texto[i]) > ancho:   # Palabra muy larga, sola en una línea
            linea = texto[i][:ancho]
            texto[i] = texto[i][ancho:]
            len_linea = ancho
            j -= 1
        else:
            linea = " ".join(texto[i:j])
        resultado.append(sangrado + linea)
        len_texto -= len_linea
        i = j
    return "\n".join(resultado)

def a_float(valor):
    "Conversion a número de coma flotante."
    inicial = valor
    try:
        if type(valor) == str:
            valor = valor.replace("," , ".")
            if valor.count(".") > 1:
                raise ValueError("\
Error: Los números pueden tener sólo un separador decimal.")
        valor = float(valor)
        return valor
    except ValueError as e:
        if e.args[0][:5] != "Error":
            raise ValueError("Error: Valor numérico inválido: " + str(inicial))\
                  from e
        else:
            raise

def indice(iterable, valor_buscado):
    """Obtiene el índice del primer elemento igual a 'valor_buscado'.

    Devuelve -1 si no se encuentra el valor buscado.
    El índice puede ser irrelevante si el iterable no es una secuencia.
    """
    for i, valor in enumerate(iterable):
        if valor == valor_buscado:
            return i
    return -1

def buscar(iterable, funcion):
    """Obtiene el primer elemento para el que la funcion devuelve True.

    Devuelve None si no se encuentra dicho elemento."""
    for valor in iterable:
        if funcion(valor):
            return valor
    return None

def buscar_por_atributo(iterable, nombre, valor):
    """Obtiene el primer elemento cuyo atributo 'nombre' es igual a 'valor'.

    Devuelve None si no se encuentra dicho elemento."""
    for elemento in iterable:
        try:
            if getattr(elemento, nombre) == valor:
                return elemento
        except AttributeError:
            pass
    return None
