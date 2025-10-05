#include "SPI.h"
#include "TFT_eSPI.h"
#include <WiFi.h>
#include <TJpg_Decoder.h>
#include <pgmspace.h>

uint16_t  PROGMEM dmaBuffer1[32*32]; // Toggle buffer for 32*32 MCU block, 1024bytes
uint16_t  PROGMEM dmaBuffer2[32*32]; // Toggle buffer for 32*32 MCU block, 1024bytes
uint16_t* dmaBufferPtr = dmaBuffer1;
bool dmaBufferSel = 0;

TFT_eSPI tft = TFT_eSPI(); 

char* ssid     = "orangepi";            //填写你的wifi名字
char* password = "orangepi";            //填写你的wifi密码
int httpPort   = 9090;                  //设置上位机端口
WiFiServer server;                      //初始化一个服务端对象

uint8_t buff[5000]      PROGMEM = {0};  //每一帧的临时缓存
uint8_t img_buff[60000] PROGMEM = {0};  //用于存储tcp传过来的图片
uint16_t size_count = 0;                //计算一帧的字节大小
uint16_t read_count = 0;                //读取buff的长度
uint8_t pack_size[2];                   //用来装包大小字节
uint16_t frame_size;                    //帧大小

bool tft_output(int16_t x, int16_t y, uint16_t w, uint16_t h, uint16_t* bitmap)
{
  if ( y >= tft.height() ) return 0;
 
  // Double buffering is used, the bitmap is copied to the buffer by pushImageDMA() the
  // bitmap can then be updated by the jpeg decoder while DMA is in progress
  if (dmaBufferSel) dmaBufferPtr = dmaBuffer2;
  else dmaBufferPtr = dmaBuffer1;
  dmaBufferSel = !dmaBufferSel; // Toggle buffer selection
  //  pushImageDMA() will clip the image block at screen boundaries before initiating DMA
  tft.pushImageDMA(x, y, w, h, bitmap, dmaBufferPtr); // Initiate DMA - blocking only if last DMA is not complete
  return 1;
}

void setup(void) {

  Serial.begin(115200);
  
  tft.begin();
  tft.initDMA();
  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);

  tft.drawString("HELLO",30,64,2);

  WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Can't connect!");
    tft.drawString("Wait...",30,64,2);
    delay(2000);                              //等一下就好
  }

  if (WiFi.status() == WL_CONNECTED)          //判断如果wifi连接成功
  { 
    Serial.println("wifi is connected!");
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);
    server.begin(httpPort);                   //服务器启动监听端口号
    server.setNoDelay(true);
  }
  TJpgDec.setJpgScale(1);
  TJpgDec.setSwapBytes(true);
  TJpgDec.setCallback(tft_output);            //解码成功回调函数
}



void loop() {

  WiFiClient client = server.available();     //尝试建立客户对象

  if(client){
    Serial.println("[New Client!]");
    client.write("ok");                       //向上位机发送下一帧发送指令
    while (client.connected()) {
      while (client.available()) {            //检测缓冲区是否有数据
        if(read_count==0)
            {
              client.read(pack_size,2);       //读取帧大小
              frame_size=(pack_size[0]<<8)+(pack_size[1]);
           }
        while(size_count<frame_size)
            {
              read_count=client.read(buff,5000);
              memcpy(&img_buff[size_count],buff,read_count);
              size_count=size_count+read_count;
            }
        tft.startWrite();
        TJpgDec.drawJpg(0,0,img_buff, sizeof(img_buff));
        tft.endWrite();
        size_count=0;
        read_count=0;
        client.write("ok");
      }
    }
  }
}
