/*###########################################
## Author's github:    madport             ##
## Author's github:    vbarcena2020        ##
#############################################
*/

#include "ServoM.h"

enum
{
  LPINSERVO1 = 2,
  LPINSERVO2 = 3,
  LPINSERVO3 = 4,
  LPINSERVO4 = 5,
  LPINSERVO5 = 6,
  LPINSERVO6 = 7,
  
  RPINSERVO1 = 8,
  RPINSERVO2 = 9,
  RPINSERVO3 = 10,
  RPINSERVO4 = 11,
  RPINSERVO5 = 12,
  RPINSERVO6 = 13,

  NUMINVALUES = 12,
  DIGITSPERVAL = 1,
};

int acel = 200;
ServoM lservo1 = ServoM(acel, -180, 180);
ServoM lservo2 = ServoM(acel, -180, 180);
ServoM lservo3 = ServoM(acel, -180, 180);
ServoM lservo4 = ServoM(acel, -180, 180);
ServoM lservo5 = ServoM(acel, -180, 180);
ServoM lservo6 = ServoM(acel*2, -180, 180);

ServoM rservo1 = ServoM(acel, -180, 180);
ServoM rservo2 = ServoM(acel, -180, 180);
ServoM rservo3 = ServoM(acel, -180, 180);
ServoM rservo4 = ServoM(acel, -180, 180);
ServoM rservo5 = ServoM(acel, -180, 180);
ServoM rservo6 = ServoM(acel*2, -180, 180);

int valsIn[NUMINVALUES];
int stringLenght = NUMINVALUES * DIGITSPERVAL + 1;
int counter = 0;
bool counterStart = false;
String recivedString;

void setup() 
{
  Serial.begin(9600);
  
  lservo1.attach(LPINSERVO1);
  lservo2.attach(LPINSERVO2);
  lservo3.attach(LPINSERVO3);
  lservo4.attach(LPINSERVO4);
  lservo5.attach(LPINSERVO5);
  lservo6.attach(LPINSERVO6);
  
  rservo1.attach(RPINSERVO1);
  rservo2.attach(RPINSERVO2);
  rservo3.attach(RPINSERVO3);
  rservo4.attach(RPINSERVO4);
  rservo5.attach(RPINSERVO5);
  rservo6.attach(RPINSERVO6);
}

void receiveData()
{
  while(Serial.available())
  {
    char c = Serial.read();

    if (c=='$') {counterStart = true; }
    
    if (counterStart)
    {
      if (counter < stringLenght)
      {
        recivedString = String(recivedString+c);
        counter++;
      }
      if (counter >= stringLenght){

        for (int i = 0; i < NUMINVALUES ; i++){
          int num = (i*DIGITSPERVAL) + 1;
          valsIn[i] = recivedString.substring(num,num + DIGITSPERVAL).toInt();
        }
        recivedString = "";
        counter = 0;
        counterStart = false;
        
      }
    }
  }
}

void loop() 
{
  receiveData();
  if (valsIn[0] == 1){lservo1.goTo(180); }
  else {lservo1.goTo(0); }
  
  if (valsIn[1] == 1){lservo2.goTo(180); }
  else {lservo2.goTo(0); }
  
  if (valsIn[2] == 1){lservo3.goTo(180); }
  else {lservo3.goTo(0); }
  
  if (valsIn[3] == 1){lservo4.goTo(180); }
  else {lservo4.goTo(0); }
  
  if (valsIn[4] == 1){lservo5.goTo(180); }
  else {lservo5.goTo(0); }

  if (valsIn[5] == 1){lservo6.goTo(180); }
  else {lservo6.goTo(0); }

  if (valsIn[6] == 1){rservo1.goTo(180); }
  else {rservo1.goTo(0); }
  
  if (valsIn[7] == 1){rservo2.goTo(180); }
  else {rservo2.goTo(0); }
  
  if (valsIn[8] == 1){rservo3.goTo(180); }
  else {rservo3.goTo(0); }
  
  if (valsIn[9] == 1){rservo4.goTo(180); }
  else {rservo4.goTo(0); }
  
  if (valsIn[10] == 1){rservo5.goTo(180); }
  else {rservo5.goTo(0); }

  if (valsIn[11] == 1){rservo6.goTo(180); }
  else {rservo6.goTo(0); }
}
