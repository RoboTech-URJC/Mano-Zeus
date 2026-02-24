![portada](./Doc/fig/portada_ze.png)

Este repositorio contiene el hardware, el software y la documentación necesarios para el proyecto **Mano de Zeus**, incluyendo información sobre su estado y progreso actuales.

---

## Sobre el proyecto

Mano de Zeus es un proyecto OpenSource desarrollado por la asociación RoboTech de la Universidad Rey Juan Carlos (Madrid, España). La asociación está formada principalmente por estudiantes del grado en Ingeniería de Robótica Software, aunque también participan estudiantes de Ingeniería de Telecomunicaciones, Aeroespacial y Biomédica, lo que aporta un enfoque multidisciplinar al desarrollo del proyecto.

El proyecto está inspirado en **[InMoov](https://inmoov.fr/hand-and-forarm/)**, pero Mano de Zeus es una propuesta propia adaptada a nuestros objetivos y recursos. Utilizamos piezas impresas en 3D, servomotores MG996R y un sistema de hilos que actúan como tendones artificiales, imitando la lógica de la mano humana, motores que tiran de “tendones” para generar el movimiento de los dedos.

---

## Mechanics

The robot structure is made out of 3D printed parts. Anctually, you can find those parts as well as files for construction in the [3D model section](3D_model).

You can find the left and right hands and arms printed and also the right bicep.

And a list of the progress of impresion in the [3D Model List](Doc/3D_Model_List.md).

---

## Software

In the software part we have developed a code that allows the movement of one of the hands at the same time. You can find it in the [Servo Move](src/ServoM)

On the other hand, we have developed hand tracking to detect the right hand and, knowing its positions, follow it and replicate its movement. You can find it in the [Hand tracking](src/handTracking)

---

## Authors

- [InMoov Members](https://inmoov.fr/) - Idea & Initial work
  
### Members 


<!--- <img width=400px src="Doc/images/Explode.png" alt="explode"></a> --->
<!---
## Electronics
<img src="Doc/images/PCB_finished.png" alt="pcb_finished"></a>
The main PCB is in charge of controlling all the peripherals of the robot. You can see in the pictures a all the connectors available. Several modules were provided:
- NEO6VM - GPS
- GY91 - IMU + Compass + Barometer + Temperature sensor
- ESP07 - Wifi module
- TB6612FGN - Dual full H bridge.
At the bottom there are 4 SMPS modules installed. They are capable of delivering up to 5A per channel.
The PCB was designed with Kicad. Take a look to the [PCB section](./noah-hardware\Doc\PCB).
--->
<!---                   FOTOS
<img width=500px src="/Doc/fig/Open_Hand.png" alt="Generic version"></a>
<img width=500px src="/Doc/fig/Closed_Hand.png" alt="Generic version"></a>
 <img width=500px src="images/../Doc/images/robot_generic.png" alt="Generic version"></a>
 <img width=670px src="images/../Doc/images/noah_generic_2.jpg" alt="Generic version2"></a>
- [Assembly file Noah version](Doc/assembly_noah.md).  
<img width=500px src="images/../Doc/images/robot_noah.png" alt="Noah version"></a>
<img width=390px src="images/../Doc/images/robot_noah2.png" alt="Noah version2"></a>
--->
