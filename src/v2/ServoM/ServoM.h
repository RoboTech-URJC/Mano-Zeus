/*###########################################
## Author's github:    madport             ##
#############################################
*/

#include <Servo.h>

#ifndef SERVOM_H_INCLUDED
#define SERVO_H_INCLUDED

class ServoM : public Servo {

  public:
    ServoM(float time_turn, int min_pos, int max_pos); // Construct
    
    void turn();
    void goTo(double grades);
    double get_pos() { return currentPos;}
    
  private:
    Servo servo_; 
    int currentPos = 180;    // Variable que representa la posición actual estimada del servo (en grados)
    int targetPos = 180;
    bool turning_= false;
    
    /* Pulse width values */
    const static int TACEL_ = 50;
    const static int LEFT_ = 85;  /* Decrease value to increase velocity */
    const static int RIGHT_ = 100;  /* Increase value to increase velocity */  
    const static int STOP_ = 90;
    
    unsigned long moveTime, moveStartTime = 0;  // Tiempo estimado para moverse
    

    /* Private methods*/ 
    unsigned long estimateMoveTime(int start, int end);  // Estimar el tiempo de movimiento
    void moveServoTo();
};

#endif