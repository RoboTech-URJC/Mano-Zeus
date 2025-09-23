/*###########################################
## Author's github:    madport             ##
#############################################
*/
#include "ServoM.h"
#include "Arduino.h"


ServoM::ServoM(float time_turn, int min_pos, int max_pos)
{
  this->write(STOP_);
}

void ServoM::moveServoTo() {
  if (!turning_) return; // No hacer nada si no se está moviendo

  unsigned long currentMillis = millis(); // Tiempo actual

  if (currentMillis - moveStartTime < moveTime) {
    // Si todavía no hemos alcanzado el tiempo necesario, mantenemos el movimiento
    if (targetPos > currentPos) {
        this->write(RIGHT_); // Girar a la derecha
    } else if (targetPos < currentPos) {
        this->write(LEFT_); // Girar a la izquierda
      }
  } else {
    // El tiempo de movimiento ha terminado, detener el servo
    this->write(STOP_);
    currentPos = targetPos; // Actualizar la posición actual
    turning_ = false;       // Finalizar el movimiento
  }
}

unsigned long ServoM::estimateMoveTime(int start, int end) {
  int angleDifference = abs(end - start);
  return map(angleDifference, 0, 180, 0, 500); // Suponemos que tarda 500 ms en moverse 180 grados
}

void ServoM::turn() {
  moveTime = estimateMoveTime(currentPos, targetPos); // Calcula el tiempo necesario para el movimiento
  turning_ = true;
  moveServoTo();                                   // Activa el estado de movimiento
}

void ServoM::goTo(double grades) {
  if (!turning_) {
    targetPos = grades;
    moveStartTime = millis();
  }
  turn(); // Inicia el movimiento hacia la posición objetivo

}