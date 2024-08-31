#ifndef SERVER_H
#define SERVER_H

#include "esp_camera.h"
#include "esp_http_server.h"
#include "esp_timer.h"
#include "img_converters.h"
#include "Arduino.h"
#include <string.h> 
#include "fb_gfx.h"
#include "soc/soc.h" //disable brownout problems
#include "soc/rtc_cntl_reg.h"  //disable brownout problems

#define PART_BOUNDARY "123456789000000000000987654321"


//directions
#define FORWARD 1
#define BACKWARD 2
#define LEFT 3
#define RIGHT 4
#define STOP 5

const int gpLb = 2;
const int gpLf = 14;  // Left forward
const int gpRb = 15;  // Right forward
const int gpRf = 13;  // Right backward
const int gpLed = 4;  // LED pin

// Define the PWM channels for controlling the motors
#define PWM_CHANNEL_LEFT  1
#define PWM_CHANNEL_RIGHT 0


typedef struct {
        httpd_req_t *req;
        size_t len;
} jpg_chunking_t;

static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char* _STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";
static const char* _STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";
extern int carSpeed;  // Declare the global carSpeed variable
extern int carDirection;

// Function to control wheel actions with PWM


//handler functions for controlling the car
static esp_err_t forward_handler(httpd_req_t *req);
static esp_err_t backward_handler(httpd_req_t *req);
static esp_err_t captureFrame_handler(httpd_req_t *req);
static esp_err_t right_handler(httpd_req_t *req);
static esp_err_t lights_handler(httpd_req_t *req);
static esp_err_t index_handler(httpd_req_t *req);
static esp_err_t set_speed_handler(httpd_req_t* req);
static esp_err_t capture_handler(httpd_req_t *req);
static esp_err_t stop_handler(httpd_req_t *req);
static esp_err_t go_handler(httpd_req_t *req);
static esp_err_t ledoff_handler(httpd_req_t *req);
static esp_err_t ledon_handler(httpd_req_t *req);
static esp_err_t back_handler(httpd_req_t *req);

// httpd_handle_t variables without initialization
extern httpd_handle_t set_speed_httpd;
extern httpd_handle_t capture_httpd;
extern httpd_handle_t index_httpd;
extern httpd_handle_t lights_httpd ;
extern httpd_handle_t stop_httpd ;
extern httpd_handle_t backward_httpd ;
extern httpd_handle_t forward_httpd;
extern httpd_handle_t captureFrame_httpd ;
extern httpd_handle_t right_httpd ;


// Initialize the camera server
void startCameraServer();
static size_t jpg_encode_stream(void * arg, size_t index, const void* data, size_t len);
String getValue(String data, String key);
#endif // SERVER_H
