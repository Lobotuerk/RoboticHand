#include <Servo.h>

Servo servo_menique;
Servo servo_anular;
Servo servo_mayor;
Servo servo_indice;
Servo servo_pulgar;

void setup() {
  Serial.begin(9600);
servo_menique.attach(4);
servo_anular.attach(5);
servo_mayor.attach(6);
servo_indice.attach(7);
servo_pulgar.attach(8);
}

int count = 0;
int servo[5] = {0,0,0,0,0};

void loop()
{
  String temp;
   if(Serial.available()>=1)
   {
    if (count == 5)
    {
      count = 0;
      }
    
    temp=Serial.readStringUntil(',');
    servo[count] = (int) temp.toFloat();
    Serial.print("I recieved ");
    Serial.println(servo[count]);
    count++;
   }
   servo_pulgar.write(servo[0]);   
  servo_indice.write(servo[1]);  
  servo_mayor.write(servo[2]);
   servo_anular.write(servo[3]);  
  servo_menique.write(servo[4]);
   
}
