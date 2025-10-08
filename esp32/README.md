**Comunicación RF entre Raspberry Pi Pico y ESP32**

Este repositorio se basa el desarrollo de un sistema de señalización ferroviaria, basado en comunicación por radiofrecuencia entre una Raspberry Pi Pico (a la cual va conectada un transmisor) y una ESP32 ( a la cuel se conecta un receptor). El objetivo es simular el estado de vías (LIBRE, PRECAUCIÓN, OCUPADO).


**¿Por qué se borró esta carpeta varias veces?^**

Durante el proceso de testeo se realizaron varias modificaciones del código para la ESP32 y se elimino esta carpeta algunas veces. Algunas razones son:

- Se pasó de una estructura básica de recepción a una más modular, con codificación de velocidad e ID.
- El receptor RF original con el que lo probamos tenía fallas, lo que llevó a problemas en la recepción y ajustes innecesarios en el código.
-  Se eliminaron versiones redundantes, pines mal asignados y funciones que no se usaban en la prueba actual.
- La ultima razon es que los codigos originales se hicieron para que la ESP32 y la raspberry se comunicaran por WIFI, pero la gracia es que se manden los datos por los transmisores y receptores de 433MHZ para poder usarlos como baliza y sensar el paso del tren cuando pasa por la via, y que la raspberry se comunique con WIFI y poder mostrar toda la informacion que tienen las señales conectadas  a las raspberrys en la pagina web     


Este README sirve se creo con la finalidad de responder a esa pregunta. A partir de ahora se añadiran las librerias que se usaron y como probar el codigo, pero los cambios importantes se realizaran en el codigo llamado main.py.
El codigo que main.py que esta a fecha de creado este Readme se hizo de esta manera para probar un transmisor en la Raspberry y un receptor en la ESP32. El siguiente cambio que se hara en el codigo sera para que el ESP32 tenga un transmisor y un receptor y la Raspberry tenga 2 transmisores y 2 receptores

