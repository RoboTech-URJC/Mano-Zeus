/*###########################################
## Author's github:    madport             ##
#############################################
*/
#include "ServoM.h"
#include "Arduino.h"

/* States of turn */ 
enum
{
  FORWARD = 0,
  BACKWARD = 1,
};

ServoM::ServoM(float time_turn, int min_pos, int max_pos)
{
  timeTurn_ = time_turn;
  min_pos_ = min_pos;
  max_pos_ = max_pos;
}

void ServoM::Forward()
{
if (! acelerated_)
  {
    long mills = millis();    
    
    for (int i = 1; i <= STEP_ ; i++)
    {
      if (millis() <= (TACEL_ * i) + timef_){ this->write(LEFT_ - i + 1); }
      if (millis() <= (TACEL_ * STEP_) + timef_){ acelerated_ = true; }
    }
  }
}

void ServoM::Backward()
{
  if (! acelerated_)
  {
    long mills = millis();    
    
    for (int i = 1; i <= STEP_ ; i++)
    {
      if (millis() <= (TACEL_ * i) + timef_){ this->write(RIGHT_ + i - 1); }
      if (millis() <= (TACEL_ * STEP_) + timef_){ acelerated_ = true; }
    }
  }
}

void ServoM::Stop(){ this->write(STOP_); acelerated_ = false;}

double ServoM::check_grades(double grades)
{
   /* Limit forward*/
   if (pos_ + grades > max_pos_){ grades = max_pos_ - pos_; }
  
   /* Limit backward and changes mode */
   if (grades < 0 && (pos_ + grades) < min_pos_){ grades = min_pos_- pos_; }  

    return grades;
}

void ServoM::turn(double grades)
{
  long actual_millis = millis();
  grades = check_grades(grades);
  if (grades > 0){ mode = FORWARD ;}
  if (grades < 0){ mode = BACKWARD ; grades *= -1; }

  if (! turning_ && grades != 0)
  {
    int mode = FORWARD;
    time0_ = millis();
    timef_ = ((grades/180)*timeTurn_) + time0_;
    target_ = grades;
    turning_ = true;
  }

  if (! acelerated_ && turning_)
  {
    if (mode == FORWARD) { pos_ += grades; Forward() ;}
    if (mode == BACKWARD) { pos_ -= grades; Backward(); }
  }
  
  if (timef_ <= actual_millis)
  {
    Stop();
    target_ = 0;
    turning_ = false;
  }
}

void ServoM::goTo(double grades)
{
  grades -= pos_;
  if (turning_){grades = 0;}
  
  turn(grades);
}