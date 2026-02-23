![portada](./Doc/fig/portada_ze.png)
# :robot: Zeus' Hand

This repo contains all the necessary hardware and software for our Zeus' Hand. It also contains all the information about the current status of the project. 

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About](#about)
- [Mechanics](#mechanics)
- [Electronics](#electronics)
- [Software](#software)
- [Authors](#authors)

## About

This project is made by the association of RoboTech from the Rey Juan Carlos University, in Madrid, Spain. Association formed mainly by students of the robotics software engineering degree, although there are also telecommunications and aerospace students.

The main idea behind this project is inspired on the InMoov project, but we are only going to make a simplyfied solution of the hands and arms parts described on the original project for now.

If enough progress is made, the objective will be expanded to the rest of the body or new ideas linked to what has already been developed will be developed, such as the method of implementing hand movement (with visual recognition or with gloves with pressure sensors).

## Mechanics

<!--- <img width=400px src="Doc/images/Explode.png" alt="explode"></a> --->

The robot structure is made out of 3D printed parts. Anctually, you can find those parts as well as files for construction in the [3D model section](3D_model).

You can find the left and right hands and arms printed and also the right bicep.

And a list of the progress of impresion in the [3D Model List](Doc/3D_Model_List.md).



<!---                   FOTOS
<img width=500px src="/Doc/fig/Open_Hand.png" alt="Generic version"></a>
<img width=500px src="/Doc/fig/Closed_Hand.png" alt="Generic version"></a>
 <img width=500px src="images/../Doc/images/robot_generic.png" alt="Generic version"></a>
 <img width=670px src="images/../Doc/images/noah_generic_2.jpg" alt="Generic version2"></a>
- [Assembly file Noah version](Doc/assembly_noah.md).  
<img width=500px src="images/../Doc/images/robot_noah.png" alt="Noah version"></a>
<img width=390px src="images/../Doc/images/robot_noah2.png" alt="Noah version2"></a>
--->

## Software

In the software part we have developed a code that allows the movement of one of the hands at the same time. You can find it in the [Servo Move](src/ServoM)

On the other hand, we have developed hand tracking to detect the right hand and, knowing its positions, follow it and replicate its movement. You can find it in the [Hand tracking](src/handTracking)

## Electronics

<!---
<img src="Doc/images/PCB_finished.png" alt="pcb_finished"></a>

The main PCB is in charge of controlling all the peripherals of the robot. You can see in the pictures a all the connectors available. Several modules were provided:

- NEO6VM - GPS
- GY91 - IMU + Compass + Barometer + Temperature sensor
- ESP07 - Wifi module
- TB6612FGN - Dual full H bridge.

At the bottom there are 4 SMPS modules installed. They are capable of delivering up to 5A per channel.

The PCB was designed with Kicad. Take a look to the [PCB section](./noah-hardware\Doc\PCB).
--->

## Authors

- [InMoov Members](https://inmoov.fr/) - Idea & Initial work# Mano-Zeus
### Members 

