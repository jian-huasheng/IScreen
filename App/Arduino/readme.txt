1.需要修改TFT_eSPI下User_Setup.h文件里的屏幕大小，屏幕驱动和IO引脚
#define TFT_WIDTH  172
#define TFT_HEIGHT 320

#define ST7789_DRIVER

#define TFT_MOSI  27  
#define TFT_SCLK  14  
#define TFT_CS    33     
#define TFT_DC    26     
#define TFT_RST   25

2.需要修改WIFI名称和密码
char* ssid          = "orangepi"; //填写你的wifi名字
char* password = "orangepi"; //填写你的wifi密码