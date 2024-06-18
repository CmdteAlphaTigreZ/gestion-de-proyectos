# Biblioteca de utilidades genéricas de programación

# Definición de tipo 'funcion_t' para usarse en validación de tipos
def f():
    pass
funcion_t = type(f)
del f


def comprobar_tipos(nombres, valores, tipos):
    """
    Comprueba los tipos de los valores, generando una excepción con \
    el nombre del primer valor inválido si lo hay

    Los tres argumentos deben ser secuencias de igual longitud:
    nombres debe contener datos tipo 'str'
    valores debe contener datos tipo 'tipo'
    tipos debe contener datos tipo 'type' que representen el 'tipo' del valor
    """
    if not len(nombres) == len(valores) == len(tipos):
        raise ValueError("debe haber la misma cantidad de nombres, valores y tipos")
    for nombre, valor, tipo in zip(nombres, valores, tipos):
        if not isinstance(valor, tipo):
            raise TypeError("'%s' no es de tipo '%s': %s"

                            % (nombre, tipo.__name__, valor))
def leer_fecha(fecha):
    "Convierte fechas en formato 'YY-MM-DDDD' a 'datetime.date'"
    return datetime.strptime(fecha, "%Y-%m-%d").date()

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
