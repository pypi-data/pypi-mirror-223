import pika        # Allows to interact with RabbitMQ
import json        # To work with the JSON data format
import traceback   # Functions to get information  about exceptions that are thrown during execution

class BugReports:
    def __init__(self, idProyect="", area="", title=""):
        # Constructor of the class that initializes the idProject, area and title attributes.
        self.__idProyect = idProyect
        self.__area = area
        self.__title = title
        self.__rabbitmq_user = None
        self.__rabbitmq_password = None
        self.__rabbitmq_host = None
        self.__rabbitmq_queue = None

    def setRabbitmqCredentials(self, username, password, host, queue):
        # Method to set RabbitMQ credentials.
        # Set the __rabbitmq_user, __rabbitmq_password, __rabbitmq_host and __rabbitmq_queue attributes
        self.__rabbitmq_user = username
        self.__rabbitmq_password = password
        self.__rabbitmq_host = host
        self.__rabbitmq_queue = queue

    def bugReports(self):
        # Method to report a bug type incident.
        try:
            # Check to make sure RabbitMQ credentials have been established before attempting to send a message
            if not self.__rabbitmq_user or not self.__rabbitmq_password or not self.__rabbitmq_host or not self.__rabbitmq_queue:
                # If RabbitMQ credentials have not been previously set, raise a ValueError exception
                raise ValueError("RabbitMQ credentials not set. Call set_rabbitmq_credentials() first")

            # Establish connection to RabbitMQ
            credentials = pika.PlainCredentials(self.__rabbitmq_user , self.__rabbitmq_password)
            parameters = pika.ConnectionParameters(host=self.__rabbitmq_host, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Declare the queue 'error_queue' to send the error message
            channel.queue_declare(queue=self.__rabbitmq_queue, durable=True)

            # Get the more detailed description of the exception
            description = traceback.format_exc()
            description = f"Descripcion:\n{description}"

            # Prepare the error message to send to RabbitMQ
            body = {
                "idProyecto": self.__idProyect,
                "area": self.__area,
                "titulo": self.__title,
                "description": description
                }
            
            # Send the error message to RabbitMQ
            channel.basic_publish(exchange='', routing_key=self.__rabbitmq_queue, body=json.dumps(body))

            # Close the connection to RabbitMQ
            connection.close()

        except Exception as e:
                # If an error occurs while sending the message, just print the error message
                print(f"Error al enviar el mensaje a RabbitMQ: {e}")
