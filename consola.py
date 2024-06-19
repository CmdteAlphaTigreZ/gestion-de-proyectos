# Módulo de interfaz en línea de comandos para el programa de
# gestión de proyectos
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-06-15
# Cambios:
#   v1
#     * Versión inicial


import utilidades as util
funcion_t = util.funcion_t; metodo_t = util.metodo_t


class Comando:
    """
    Comando de consola que llama a una función con los argumentos de consola

    'ayuda' debe estar en la cadena de documentación de la función y sirve
      como pista para el usuario acerca de la funcionalidad del comando
    'sintaxis' es un texto que muestra la sintaxis válida con que se puede
      llamar al comando
    'descripción' es un texto de ayuda más extenso que describe toda la
      funcionalidad del comando
    'funcion' es una función que recibirá los argumentos de la línea de
      comandos, tomará el control de la consola, y luego *debe devolver su
      resultado como un objeto 'Resultado'*, no se debe mostrar en la consola
    """

    def __init__(self, funcion, sintaxis, descripcion=""):
        util.comprobar_tipos(
            ("ayuda", "sintaxis", "descripcion"),
            (funcion.__doc__, sintaxis, descripcion),
            (str, str, str)
        )
        self.ayuda = funcion.__doc__
        self.sintaxis = sintaxis
        self.descripcion = descripcion
        if isinstance(funcion, funcion_t):
            self.funcion = funcion
        elif isinstance(funcion, metodo_t):
            self.funcion = funcion.__func__
        else:
            raise TypeError("'funcion' no es de tipo 'function' o 'method': %s"
                            % funcion)

    def __call__(self, consola, linea_comando):
        resultado = self.funcion(consola, linea_comando)
        util.comprobar_tipos(("resultado",), (resultado,), (Resultado,))
        return resultado

    def __str__(self):
        "Devuelve la sintaxis del comando"
        return self.sintaxis


class Resultado:
    "Resultado de Comando"

    def __init__(self, resultado, origen, tipo_error=None):
        util.comprobar_tipos(("resultado",), (resultado,), (str,))
        if tipo_error is not None:
            util.comprobar_tipos(("tipo_error",), (tipo_error,), (str,))
        self.resultado = resultado
        self.origen = origen
        self.tipo_error = tipo_error


def _comprobar_comandos(comandos):
    util.comprobar_tipos(("comandos",), (comandos,), (dict,))
    util.comprobar_tipos(("comando",) * len(comandos),
                         tuple(comandos.values()),
                         (Comando,) * len(comandos))


# Nótese el plural, es un contenedor
class Contextos:
    "Contextos de Comandos"

    def __init__(self):
        self.__contextos = {"principal": {}}
        self.actual = "principal"

    def agregar(self, nombre, comandos):
        util.comprobar_tipos(("nombre",), (nombre,), (str,))
        _comprobar_comandos(comandos)
        if nombre in self.__contextos:
            raise ValueError(
                "Tiene que utilizar 'reemplazar' para cambiar un contexto existente")
        self.__contextos[nombre] = comandos

    def reemplazar(self, nombre, comandos):
        util.comprobar_tipos(("nombre",), (nombre,), (str,))
        _comprobar_comandos(comandos)
        if nombre not in self.__contextos:
            raise ValueError(
                "Tiene que utilizar 'agregar' para agregar un nuevo contexto")
        self.__contextos[nombre] = comandos

    def __getitem__(self, nombre):
        return self.__contextos[nombre]
    obtener = __getitem__

    def __iter__(self):
        return iter(self.__contextos)

    def copiar(self):
        copia = Contextos()
        for nombre, comandos in self.__contextos.items():
            copia.__contextos[nombre] = comandos.copy()
        return copia


class Consola:
    "Interfaz en línea de comandos"

    def __init__(self, contextos):
        # ¿Algo que añadir aquí?

        # Son públicos pero mejor no modificar arbitrariamente
        self.contextos = contextos.copiar()
        self.comandos = self.contextos["principal"]
        self.linea_comando = []
        
        self.comandos["ayuda"] = Comando(self.ayuda, "ayuda")
        self.comandos["salir"] = Comando(self.salir, "salir")

    def consola(self):
        "Procedimiento que implementa la interfaz en línea de comandos."

        print(self.ayuda().resultado)
        
        self.leer_comando()
        comando = self.linea_comando[0]
        while True:
            try:
                if comando == "salir" and "salir" in self.comandos:
                    if len(self.linea_comando) != 1:                    
                        mensaje_e = \
                            "Error: Sintaxis inválida: salir no toma argumentos."
                        print(mensaje_e)
                    elif self.salir():
                        break
                if comando == "ayuda":
                    if len(self.linea_comando) != 1:                    
                        mensaje_e = \
                            "Error: Sintaxis inválida: ayuda no toma argumentos."
                        print(mensaje_e)
                    print(self.ayuda().resultado)
                else:
                    try:
                        resultado = self.comandos[comando](self, self.linea_comando)
                        print(resultado.resultado, end="\n")
                    except KeyError as e:
                        mensaje_e = "Error: Comando desconocido: " + comando
                        print(mensaje_e)
                self.linea_comando = []
                self.leer_comando()
                comando = self.linea_comando[0]
            except KeyboardInterrupt:
                break
        print("Saliendo del programa...")

    def leer_comando(self, linea_comando=None):
        "Lee una línea de comando de la entrada. linea_comando debe ser '[]'"
        if linea_comando is None: linea_comando = self.linea_comando
        continuar = True
        while continuar:
            try:
                linea_comando.extend( input(">> ").split() )
            # Esta excepcion que sigue no debe ser capturada, está mal.
            #except EOFError as e:
            #    pass
            except UnicodeError as e:
                mensaje_e = "Error: Texto de entrada por consola inválido."
                print(mensaje_e)
            else:
                if len(linea_comando) != 0:
                    continuar = False

    def saludar(self):
        print("Nota: No se pueden añadir tareas si no hay proyectos creados",
              "y no se pueden crear subtareas si no hay tareas creadas",
              "-----Menu Principal-----",
              sep="\n")

    def ayuda(self, linea_comando=None):
        "Mostrar ayuda"
        # POR HACER!!!
        # Implementar ayuda con argumentos para ver la descripción de un comando
        ayuda = ["Comandos disponibles:"]
        for cmd in self.comandos.values():
            ayuda.append("""  {}
                                {}""".format(cmd.sintaxis, cmd.ayuda) )
        ayuda = "\n".join(ayuda)
        return Resultado(ayuda, self)

    def salir(self, linea_comando=None):
        "Salir de la consola"
        confirmacion = input("Seguro que desea salir (S/N): ")
        if confirmacion in ("S", "s"):
            return True
        print("Cierre cancelado")
        return False

    def cambiar_contexto(self, nombre=None):
        if nombre is None:
            nombre = "principal"
        self.contextos.actual = nombre
        self.comandos = self.contextos[nombre]

    def leer_argumentos(self, nombres, mensajes, linea_comando=None):
        """
        Lee argumentos de la línea de comandos y del usuario.\
         Acepta dos listas de texto y devuelve una lista de texto.

        Esta función obtiene los argumentos para un comando
        de la línea de comando sólo si todos están en ella,
        de lo contrario los solicita al usuario mostrando uno
        de los mensajes para cada argumento requerido sólo si
        no se proporciona ninguno en la línea de comando;
        levanta una excepción de uso inapropiado de no cumplirse
        alguna de estas condiciones.  Se considera que la cantidad
        de argumentos requeridos por el comando es la cantidad
        de mensajes para el usuario que recibe esta función
        como parámetro.

        Se devuelve una lista de todos los argumentos del comando
        en el orden en que se recibieron los mensajes al usuario
        para ellos.

        Debe capturarse desde el comando la excepción ValueError
        que puede levantar esta función.
        """

        if linea_comando is None: linea_comando = self.linea_comando
        len_linea_comando = len(linea_comando)
        len_argumentos = len(nombres)
        if len_argumentos != len(mensajes):
            raise ValueError(
                "'nombres' y 'mensajes' deben tener la misma longitud")
        
        # "argumentos = dict[str, str]"
        argumentos = {}

        if len_linea_comando - 1 == len_argumentos:
            for nombre, valor in zip(nombres, linea_comando[1:]):
                argumentos[nombre] = valor
        elif len_linea_comando == 1:
            try:
                for nombre, mensaje in zip(nombres, mensajes):
                    argumentos[nombre] = input(mensaje)
            except EOFError as e:
                raise ValueError("Error: No se proporcionó el dato.")\
                      from e
            except UnicodeError as e:
                raise UnicodeError("Error: Texto de entrada por consola inválido.")\
                      from e
        else:
            raise SyntaxError(
                "Error: Sintaxis inválida: "
                + str(self.comandos[linea_comando[0]]) )
        return argumentos

##    def cmd_leerconfig(linea_comando):
##        "Comando leerconfig. Acepta lista de texto y devuelve diccionario de texto."
##
##        argumentos = list()
##        try:
##            # Este comando no tiene parámetros, serán rechazados.
##            argumentos = leer_argumentos(linea_comando, [])
##        except ValueError as e:
##            return {"resultado": e.args[0], "tipo_error": "Valor"}
##        except SyntaxError as e:
##            return {"resultado": e.args[0], "tipo_error": "Sintaxis"}
##        except UnicodeError as e:
##            return {"resultado": e.args[0], "tipo_error": "Codificación de texto"}
##        configuracion = leerconfig()
##        return configuracion
##
##    info["leerconfig"]["comando"] = cmd_leerconfig
##
##    def leerconfig():
##        "Devuelve el contenido del archivo de configuración"
##
##        configuracion = str()
##        # Realmente es de uno de los tipos de archivo
##        archivo = open
##        try:
##            archivo = open(ruta_configuracion)
##            configuracion = archivo.read()
##        except OSError as e:
##            return {\
##                "resultado": "Error: No se pudo abrir el archivo de configuración.",
##                "tipo_error": "Archivo"}
##        except UnicodeError as e:
##            return {\
##                "resultado": "Error: Archivo de configuración con texto inválido.",
##                "tipo_error": "Codificación de texto"}
##        archivo.close()
##        return {"resultado": "\n" + configuracion + "\n",
##                "tipo_error": ""}
