# Módulo de interfaz en línea de comandos genérica
# Autor: Francisco Román, Francisco Unda y Santiago Pinto
# Fecha: 2024-07-01
# Cambios:
#   v1
#     * Versión inicial
#   v2
#     * Ayuda mejorada


import utilidades as util
funcion_t = util.funcion_t; metodo_t = util.metodo_t


class Comando:
    """Comando de consola que llama a una función con los argumentos de consola.

    'ayuda' debe estar en la cadena de documentación de la función y sirve
      como pista para el usuario acerca de la funcionalidad del comando;
      no debería terminar en un punto '.'.
    'sintaxis' es un texto que muestra la sintaxis válida con que se puede
      llamar al comando. Ej: comando <arg_reemplazado> [arg_opcional].
    'descripción' es un texto de ayuda más extenso que describe toda la
      funcionalidad del comando.
    'funcion' es una función que recibirá los argumentos de la línea de
      comandos, tomará el control de la consola, y luego *debe devolver su
      resultado como un objeto 'Resultado'*, preferiblemente no se debe
      mostrar en la consola.
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
    """Resultado de Comando

    'resultado' es el texto de resultado del comando.
    'origen' debería ser una la función o comando que generó el resultado;
      en este momento no está exactamente definido ni es usado.
    'tipo_error' es un texto que indica el tipo de error ocurrido, si lo hay;
      en este momento no está uniformizado dentro de la clase.
    """

    def __init__(self, resultado, origen, tipo_error=None):
        util.comprobar_tipos(("resultado",), (resultado,), (str,))
        if tipo_error is not None:
            util.comprobar_tipos(("tipo_error",), (tipo_error,), (str,))
        self.resultado = resultado
        self.origen = origen
        self.tipo_error = tipo_error


def _comprobar_comandos(comandos):
    "Utilizado para valida los tipos de *un* contexto."
    util.comprobar_tipos(("comandos",), (comandos,), (dict,))
    util.comprobar_tipos(("comando",) * len(comandos),
                         tuple(comandos.values()),
                         (Comando,) * len(comandos))


# Nótese el plural, es un contenedor
class Contextos:
    "Contextos de Comandos.  Un contexto es un diccionario de comandos."

    def __init__(self):
        self.__contextos = {"principal": {}}
        self.actual = "principal"  # Guarda el nombre del contexto activo

    def agregar(self, nombre, comandos):
        "Añade un nuevo contexto al contenedor."
        util.comprobar_tipos(("nombre",), (nombre,), (str,))
        _comprobar_comandos(comandos)
        if nombre in self.__contextos:
            raise ValueError(
                "Tiene que utilizar 'reemplazar' para cambiar un contexto existente")
        self.__contextos[nombre] = comandos

    def reemplazar(self, nombre, comandos):
        "Reemplaza un contexto existente en el contenedor por otro."
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
        "Devuelve cada contexto, no los nombres de ellos."
        return iter(self.__contextos.values())

    def copiar(self):
        "Copia semi-profunda de los contextos. No copia los comandos individuales."
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

        comando_ayuda = Comando(self.ayuda, "ayuda [nombre_comando]")
        comando_salir = Comando(self.salir, "salir")
        for comandos in self.contextos:
##            for comando in ("ayuda", "salir"):
##                comandos.pop(comando, None)
            comandos["ayuda"] = comando_ayuda
            comandos["salir"] = comando_salir

    def consola(self):
        "Procedimiento que implementa la interfaz en línea de comandos."

        self.saludar()
        self.ayuda()

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
##                if comando == "ayuda":
##                    if len(self.linea_comando) != 1:
##                        mensaje_e = \
##                            "Error: Sintaxis inválida: ayuda no toma argumentos."
##                        print(mensaje_e)
##                    self.ayuda()
                else:
                    try:
                        resultado = self.comandos[comando](self, self.linea_comando)
                        if resultado.resultado != "":
                            print(resultado.resultado, end="\n")
                    except KeyError as e:
                        mensaje_e = "Error: Comando desconocido: " + comando
                        print(mensaje_e)
                    except (ValueError, SyntaxError, UnicodeError) as e:
                        mensaje_e = e.args[0]
                        print(mensaje_e)
            except (KeyboardInterrupt, EOFError):
                print("Operación cancelada.")

            try:
                self.linea_comando = []
                self.leer_comando()
                comando = self.linea_comando[0]
            except (KeyboardInterrupt, EOFError):
                break
        print("Saliendo del programa...")

    def leer_comando(self, linea_comando=None):
        "Lee una línea de comando de la entrada. linea_comando debe ser '[]'"
        if linea_comando is None: linea_comando = self.linea_comando
        continuar = True
        while continuar:
            try:
                linea_comando.extend( input(">> ").split() )
            except UnicodeError as e:
                mensaje_e = "Error: Texto de entrada por consola inválido."
                print(mensaje_e)
            else:
                if len(linea_comando) != 0:
                    continuar = False

    def saludar(self):
        "Muestra un mensaje inicial en la consola."
        print("Nota: No se pueden añadir tareas si no hay proyectos creados"
              " y no se pueden crear subtareas si no hay tareas creadas",
              "\n-----Menu Principal-----",
              sep="\n")

    def ayuda(self, linea_comando=None):
        "Muestra los comandos disponibles o la ayuda para un comando particular"
        if linea_comando is None or len(linea_comando) == 1:
            SANGRADO = 36
            FORMATO = "%-{}s%s".format(SANGRADO - 1)
            ayuda = ["Comandos disponibles:"]
            for cmd in self.comandos.values():
                if len(cmd.sintaxis) < SANGRADO:
                    cmd_ayuda = " " \
                        + util.envolver_y_sangrar(cmd.ayuda, 72, SANGRADO).lstrip()
                else:
                    cmd_ayuda = "\n" \
                        + util.envolver_y_sangrar(cmd.ayuda, 72, SANGRADO)
                ayuda.append(FORMATO % (cmd.sintaxis, cmd_ayuda))
            ayuda = "\n".join(ayuda)
            if linea_comando is None:
                print(ayuda)
                ayuda = ""
        elif len(linea_comando) == 2:
            try:
                comando = self.comandos[linea_comando[1]]
            except KeyError:
                ayuda = "Error: Comando desconocido: " + linea_comando[1]
            else:
                ayuda = [comando.ayuda, "  " + comando.sintaxis]
                if comando.descripcion != "":
                    ayuda.extend(
                        ["", util.envolver_y_sangrar(comando.descripcion)] )
                ayuda = "\n".join(ayuda)
        else:
            return Resultado("Error: Sintaxis inválida: "
                + str(self.comandos["ayuda"]), self, tipo_error="Sintaxis")
        return Resultado(ayuda, self)

    def salir(self, linea_comando=None):
        "Sale de la consola"
        return self.confirmar("Seguro que desea salir?")

    def cambiar_contexto(self, nombre=None):
        "Cambia el contexto de comandos actual, sin más."
        if nombre is None:
            nombre = "principal"
        self.contextos.actual = nombre
        self.comandos = self.contextos[nombre]

    def leer_argumentos(self, nombres, mensajes, linea_comando=None):
        """Lee argumentos de la línea de comandos y del usuario.

        Acepta dos secuencias de texto y devuelve un diccionario
        de todos los argumentos del comando, cuyas claves son
        los nombres dados como parámetro.

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

    def confirmar(self, mensaje):
        "Solicita confirmación.  El mensaje no debe contener ' (S/N): '"
        confirmacion = input(mensaje + " (S/N): ")
        if confirmacion in ("S", "s"):
            return True
        print("Operación cancelada")
        return False

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
