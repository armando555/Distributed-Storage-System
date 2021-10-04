# Distribuited-Storage
Proyecto de topicos de telemática

Integrantes: 

Armando Ríos Gallego

Julian Ríos Vasquez

Este proyecto se uso socket para conectar todas las máquinas con el servidor y mantener una concurrencia. Y para gestionar todo el tratamiento de archivos en BYTES entre máquina y servidor
se usa protocolo HTTP a través de peticiones y respuestas. Siendo el cliente el servidor en este protocolo y el cliente conectado a través de socket se comporta como
servidor HTTP. Por lo cuál es una red P2P centralizada en donde hay un servidor que comunica a todos clientes y gestiona todas las peticiones de guardar y descargar imagenes.



Para ejecutar la aplicación se debe ejecutar primero el archivo server.py el cual desplegará 2 comandos SAVE Y DOWNLOAD. El comando SAVE es para guardar una imagen local
en el sistema de almacenamiento distribuido. Su eso es de:

escribes el comando

SAVE

input data to search

"escribes el nombre de la imagen"



Para descagar una imagen previamente guardada se ejecuta el comando DOWNLOAD a la máquina local

escribes el comando

DOWNLOAD

input data to download

"escribes el nombre de la imagen"
