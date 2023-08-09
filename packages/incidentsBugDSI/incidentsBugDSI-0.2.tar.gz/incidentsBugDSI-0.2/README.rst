GestionIncidenciasTipoBug
=========================

Este repositorio contiene el código fuente para una aplicación de
gestión de incidencias tipo bug.

Descripción
-----------

GestionIncidenciasTipoBug es una funcion que te brinda la capacidad de
reportar y gestionar incidencias y errores en tu código de manera
efectiva y colaborativa. Esta funcion está diseñada para agilizar y
optimizar el proceso de detección y seguimiento de bugs en los proyectos
de software.

Características
---------------

-  Comunicación Asíncrona con Rabbit MQ: GestionIncidenciasTipoBug
   utiliza una comunicación asincrónica a través de Rabbit MQ, lo que
   permite un flujo constante y fluido de información entre los miembros
   del equipo.

-  Reporte Rápido y Preciso: La aplicación proporciona un proceso de
   reporte de bugs sencillo e intuitivo.

-  Seguimiento de Incidencias en Tiempo Real: GestionIncidenciasTipoBug
   ofrece una vista en tiempo real de todas las incidencias registradas.

-  Notificaciones Personalizadas: GestionIncidenciasTipoBug permite
   configurar notificaciones personalizadas para mantener a todos los
   miembros del equipo informados sobre las actualizaciones de
   incidencias importantes.

Requisitos
----------

Antes de ejecutar la aplicación, es importante asegurarte de que tengas
instalados los siguientes componentes y bibliotecas en tu entorno de
desarrollo:

-  Python 3

Bibliotecas de Python:
~~~~~~~~~~~~~~~~~~~~~~

-  pika: Permite interactuar con RabbitMQ.

.. code:: python

   pip install pika

Para obtener más información sobre RabbitMQ y cómo usar la biblioteca
``pika``, puedes consultar la documentación oficial y tutoriales:

-  `RabbitMQ Documentation <https://www.rabbitmq.com/>`__
-  `pika Documentation <https://pypi.org/project/pika/>`__

Consideraciones
===============

Obtener el ID del proyecto en Jira:
===================================

La URL ``https://dsinno.atlassian.net/rest/api/latest/project/<CLAVE>``
se utiliza para acceder a la API de Jira y obtener información sobre un
proyecto específico. La en la URL debe reemplazarse con la clave única
del proyecto que deseas consultar. Al hacer una solicitud GET a esta URL
remplazando , obtendrás un conjunto de datos JSON que incluye
información sobre el proyecto, incluido su “id”.

Utilizar el ID del proyecto en tu código:
=========================================

Una vez que has obtenido el ID del proyecto, En el ejemplo
proporcionado, el ID del proyecto se asigna a la variable idProyect.
Esto te permite rastrear la fuente de los errores y asociarlos con el
proyecto correcto en Jira

Uso de la Función ReportBug
===========================

Sintaxis
--------

.. code:: python

      bugReportsInstance = BugReports(idProyecto="123456", area="desarrollo", título="Error en la función `foo()`")
      bugReportsInstance.setRabbitmqCredentials(username="tu_usuario", password="tu_contraseña", host="dirección_del_servidor", queue="nombre_de_la_cola")
      bugReportsInstance.bugReports()

Ejemplo
~~~~~~~

\```python from incidentsBugDSI.bugReports import BugReports

::

   try:
       resultado = 10 / 0
   except Exception as e:
       idProyecto = "123456"
       area = "desarrollador"
       title = str(e)

       bugReportsInstance = BugReports(idProyecto, area, title)
       bugReportsInstance.setRabbitmqCredentials(username="tu_usuario", password="tu_contraseña", host="dirección_del_servidor", queue="nombre_de_la_cola")
       bugReportsInstance.bugReports()
   ```

Excepciones
~~~~~~~~~~~

Si hay algún error al reportar el bug, la función ``bugReports()``
arrojará una excepción.
