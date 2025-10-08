**Comunicación RF entre Raspberry Pi Pico y ESP32**

Este repositorio se basa el desarrollo de un sistema de señalización ferroviaria, basado en comunicación por radiofrecuencia entre una Raspberry Pi Pico (a la cual va conectada un transmisor) y una ESP32 ( a la cuel se conecta un receptor). El objetivo es simular el estado de vías (LIBRE, PRECAUCIÓN, OCUPADO).

**¿Por qué se borró esta carpeta varias veces?**

Durante el proceso de testeo se realizaron varias modificaciones del código para la RASPBERRY y se elimino esta carpeta algunas veces. La razon principal es que pasamos de usar comunicacion entre una Raspberry en la locomotora y otra en la via, a cuna comunicacion usando una ESP32 en la locomotora y una Raspberry en la via y usando sensores RF433MHZ, por lo que los viejos codigos quedaron desactualizados 

Este README se creo con la finalidad de explicar porque se borro la carpeta varias veces y se eliminaron varios codigos. Esta carpeta contiene la libreria que se uso, los cambios importantes se realizaran en el codigo llamado main.py. La siguiente actualizacion en ese codigo se hara para incluir 2 transmisores y 2 receptores en la Raspberry. 
