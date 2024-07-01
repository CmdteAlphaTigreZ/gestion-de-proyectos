# Sistema de gestión de proyectos

## Estructura

### <cli.py>    Interfaz en línea de comandos.

Implementa los comandos que interactúan con el usuario para
intercambiar información con él.  Actualmente también
realiza la gestión de proyectos propiamente dicha.

Depende de todos los demás módulos.

Las funciones fn_* son las que implementan los comandos.
Luego de definirse, debería construirse un objeto Comando,
como se define en consola.py, y guardarse en algún contexto.

El contexto se debe pasar al constructor de Consola.

### <proyectos.py>    Módulo abstracto de gestión de proyectos.

Contiene las definiciones de Proyecto y Tarea, y algunas
funciones para gestionarlos.  Debería proveer un Gestor
que realice parte del trabajo que ahora se hace en cli.py.

Depende de colecciones.py.

### <consola.py>    Módulo de consola genérico.

Define Comando, Resultado, Contexto, Consola

Para utilizarlo, se deben crear objetos Comando que traten
cada función que se quiera ofrecer al usuario.
Los comandos deben agruparse en un contexto, que es un
diccionario donde las claves son los nombres de los comandos.
Los contextos deben registrarse con sus nombres en un
contenedor Contextos, que será usado por la Consola para
mostrar distintos menúes según el contexto activo a través
de la función ayuda.

Las funciones que implementan los comandos deben tener por
parámetros la Consola y la línea de comandos (lista de str).

Los comandos deberían devolver sus resultados en un objeto
Resultado, que contiene la salida de texto para el usuario,
y metadatos de origen y posible condición de error.
A los comandos se les permite mostrar texto directamente
en la salida estándar, por ahora.  Si no se desea 'devolver'
ningún resultado, por ejemplo, porque ya se muestra por otro
medio, el comando igualmente debe devolver un Resultado,
pero puede estar vacío; en este caso no se muestra un salto
de línea vacío.

La Consola ofrece algunas funciones para mostrar una lista
de comandos y ayuda para un comando particular (método ayuda),
para confirmar una operación (método confirmar), para
cambiar el contexto actual (cambiar_contexto), para leer
argumentos de la línea de comando recibida (leer_argumentos)

La Consola limpia ligeramente la entrada y atrapa algunos
errores, simplificando la interacción programa-usuario.
Las funciones genéricas que podrían ser usadas por cualquier
comando bien podrían ser implementadas como métodos de Consola.

Depende de utilidades.py

### <colecciones.py>   Biblioteca de colecciones/estructuras de datos

Contiene colecciones algo concretas como una lista doblemente
enlazada y árboles binarios, y otras más abstractas como pilas
y colas.

Las clases poseen una variedad de métodos para
manipular las colecciones y simplificar las interacciones con
ellas.  En particular, varias permiten usar las siguientes
características de Python de manera integrada:

    len(coleccion)
    secuencia[indice]
    secuencia[indice] = valor
    del secuencia[indice]
    for elemento in secuencia:
        # Hacer algo
        pass
    str(secuencia)  # Algo un poco más significativo

Depende de utilidades.py

### <utilidades.py>    Biblioteca de utilidades de programación

Contiene funciones de programación generales que son susceptibles
de ser utilizadas en cualquier módulo, como conversiones de datos,
formato de texto, validaciones, etc.

Depende del datetime estándar de Python

### Notas

Los módulos consola.py, colecciones.py y utilidades.py deberían
mantenerse independientes de lo relacionado con la gestión de
proyectos, de manera que sea posible reutilizarlos a futuro en
otros programas.

## ¡Por hacer!

### Importante

- Árbol AVL
- Árbol n-ario
- Clase Empresa
- Gestión de empresa
- Leer el archivo de configuración
- Serializar y cargar los datos de archivos de estado
- Validar las fechas
    - fecha_inicio < fecha_vencimiento
    - Las fechas de las tareas deben estar dentro del rango
      de fechas del proyecto.  Igualmente las subtareas dentro
      de su tarea padre.
- Hacer que el estado tenga valores limitados
    - Recomendación: No iniciado, Detenido, En progreso, Completado
- Validar los porcentajes, 0 <= porcentaje <= 100
- Sincronizar los porcentajes con el estado: 100% -> Completado
- Permitir la selección de empresas/proyectos/tareas por otros
  criterios que solo ID
    - Se podría implementar solo en la consulta, para conseguir el ID
    - Se podría hacer en cualquier comando
    - Sería bueno un sistema de búsqueda/filtrado implementado
      en proyectos.py que devuelva una coleccion de
      coincidencias/resultados
- Hacer que la información se actualice en los archivos en cada
  paso

### Relevante

- Mover la parte de la funcionalidad presente en cli.py que debería
  estar en proyectos.py
- Modificar la Consola para que los comandos integrados se puedan
  ocultar opcionalmente
    - Recomendación: insertar los comandos en un contexto
      particular sólo si no están presentes unos con los mismos
      nombres
    - Recomendación: utilizar None como dato falso para evitar
      la inserción del comando integrado pero eliminarlo
      posteriormente para evitar errores con la ayuda
- No capturar ValueError en la consola, sino que cada comando
  tenga que tratar los errores de valor que se generen
    - La idea es dejar que los errores inesperados finalicen el
      programa
    - Alternativamente, mostrar los errores no dirigidos al usuario
      (los de programación) de otra manera más distintiva
- Validar los tipos de los argumentos en los constructores de clase
  en proyectos.py, preferiblemente con comprobar_tipos de
  utilidades.py

### Opcional

- Modificar la consola para que muestre más información acerca
  del contexto actual
    - Se podría mostrar siempre el contexto
    - Se podría guardar un mensaje de encabezado para cada contexto
      que se muestre con la ayuda
    - Se podría guardar un mensaje que se muestre en la señal
      de petición de entrada (el >>)
- Ajustar las llamadas a comprobar_tipos con un tuplas de un solo
  elemento para que se hagan sin las tuplas, aprovenchando el
  nuevo soporte y simplificando el código
- Escribir documentación para el usuario
