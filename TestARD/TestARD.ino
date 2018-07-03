#include <Servo.h>

Servo servo_menique;
Servo servo_anular;
Servo servo_mayor;
Servo servo_indice;
Servo servo_pulgar;

#define pinRojo 9
#define pinVerde 10
#define pinAzul 11
#define pinNegRojo 17
#define pinNegVerde 18
#define pinNegAzul 19

void setup() {
  Serial.begin(9600);
servo_menique.attach(2);
servo_anular.attach(3);
servo_mayor.attach(4);
servo_indice.attach(5);
servo_pulgar.attach(6);
  pinMode(pinRojo,OUTPUT);
  pinMode(pinVerde,OUTPUT);
  pinMode(pinAzul,OUTPUT);
  pinMode(pinNegRojo,OUTPUT);
  pinMode(pinNegVerde,OUTPUT);
  pinMode(pinNegAzul,OUTPUT);
  escribir_RGB(255,255,255);
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
   servo_pulgar.write(170 - servo[0]);   
  servo_indice.write(170 - servo[1]);  
  servo_mayor.write(170 - servo[2]);
   servo_anular.write(170 - servo[3]);  
  servo_menique.write(170 - servo[4]);
   
}

void escribir_RGB(int Rojo,int Verde,int Azul){
  analogWrite(pinRojo,Rojo);
  analogWrite(pinVerde,Verde);
  analogWrite(pinAzul,Azul);
  digitalWrite(pinNegRojo,(1-(Rojo/255)));
  digitalWrite(pinNegVerde,(1-(Verde/255)));
  digitalWrite(pinNegAzul,(1-(Azul/255)));
}

