/* MQTT, send sample (esp8266)
*/
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>

//*******************************************************************************
//* 定数、変数
//*******************************************************************************
//サーボ関連
#define ServoCH 4
Servo myservo[ServoCH];         //サーボ構造体


SoftwareSerial mySerial(4, 5); /* RX:D4, TX:D5 */
const char* ssid = "myssid";
const char* password = "mypass";


//String mAPI_KEY=" ";
const char* mClient_id = "cliennt-1";
const char* mqtt_server = "ec2-xx-xx-xx-xx.us-west-2.compute.amazonaws.com";

char mTopicIn[]="item-kuc/device-1/test1";

WiFiClient espClient;
PubSubClient client(espClient);

//ポート設定
 #define ServoCH1 14
 #define ServoCH2 12
 #define ServoCH3 13
 #define ServoCH4 15

//
//------------------------------
// IO初期化
//------------------------------
void setup_io(void) {
  //init servo
  myservo[0].attach(ServoCH1);   // attaches the servo on GIO4 to the servo object
  myservo[1].attach(ServoCH2);   // attaches the servo on GIO5 to the servo object
  myservo[2].attach(ServoCH3);   // attaches the servo on GI12 to the servo object
  myservo[3].attach(ServoCH4);   // attaches the servo on GI13 to the servo object
}

void setup() {
  setup_io();
  Serial.begin(9600);
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

//
void callback(char* topic, byte* payload, unsigned int length) {
  String sTopi=String( mTopicIn );
  String sTopi_in =String( topic );
  String sCRLF="\r\n";  
  if( sTopi.equals( sTopi_in ) ){
    for (int i=0;i<length;i++) {
      String sPay= String( (char)payload[i] );
      Serial.println("sPay= "+ sPay);
      if(sPay=="1" ){
        myservo[2].write(90+45);
      }else if(sPay == "0"){
        myservo[2].write(90-45);
      }
    }
   }
}

//
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect( mClient_id )) {
      Serial.println("connected");
      client.subscribe(mTopicIn);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

//
void loop() {
   if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
}

