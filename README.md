![portada](./Doc/fig/portada_ze.png)

Este repositorio contiene el hardware, el software y la documentación necesarios para el proyecto **Mano de Zeus**, incluyendo información sobre su estado y progreso actuales.

---

## Sobre el proyecto

Mano de Zeus es un proyecto OpenSource desarrollado por la asociación **RoboTech de la URJC**. 

El proyecto está inspirado en **[InMoov](https://inmoov.fr/hand-and-forarm/)**, pero Mano Zeus es una adaptación propia, ajustada a nuestros recursos y a nuestros objetivos educativos. Igual que la mano humana se mueve gracias a músculos y tendones, Mano de Zeus utiliza motores y hilos que imitan esa misma forma de generar movimiento en una mano robótica impresa en 3D.

---

## Hardware y Software

La estructura del robot está compuesta por piezas impresas en 3D, lo que hace que el proyecto sea accesible. Los archivos necesarios para su construcción pueden encontrarse en la sección **[3D_model](https://github.com/RoboTech-URJC/Mano-Zeus/tree/main/3D_model)**.

El sistema de control se divide en dos partes principales:
- **Control de servomotores en Arduino**: código que controla el movimiento de los dedos, permitiendo moverlos de forma individual o todos a la vez. **[ServoMove](src/v2/ServoM)**
- **Seguimiento de mano con Python**: usamos la cámara para seguir el movimiento de una mano real y enviar esa información al Arduino, que se encarga de mover la mano robótica para que haga lo mismo. **[Hand Tracking](src/v2/handTracking)**

De esta manera, el software interpreta el movimiento y el hardware lo ejecuta físicamente.

---
## Demostración
*Haz click en la imagen para ver nuestro avance actual* (25/02/2026)

<p align="center">
  <a href="https://youtube.com/shorts/6KSZLjYA9YE?si=bSkOJxbSDhfmJuYE">
    <img src="https://github.com/user-attachments/assets/1434d1c4-fd05-4bd6-be03-d4d676ada2ac" width="400">
  </a>
</p>
