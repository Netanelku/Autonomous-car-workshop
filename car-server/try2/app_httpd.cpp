#include "server.h"
extern String WiFiAddr;

void WheelAct(int nLf, int nLb, int nRf, int nRb);

void stopCar() {
    WheelAct(LOW, LOW, LOW, LOW); // Stop the car
    Serial.println("Stop");
}

httpd_handle_t car_httpd = NULL;

static size_t jpg_encode_stream(void * arg, size_t index, const void* data, size_t len){
    jpg_chunking_t *j = (jpg_chunking_t *)arg;
    if(!index){
        j->len = 0;
    }
    if(httpd_resp_send_chunk(j->req, (const char *)data, len) != ESP_OK){
        return 0;
    }
    j->len += len;
    return len;
}

esp_err_t capture_handler(httpd_req_t *req) {
    Serial.println("capture request");
    camera_fb_t *fb = NULL;
    esp_err_t res = ESP_OK;
    int64_t fr_start = esp_timer_get_time();
    sleep(500);
    fb = esp_camera_fb_get(); // get fresh image
    if (!fb) {
        // Serial.println("Camera capture failed");
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }
    httpd_resp_set_type(req, "image/jpeg");
    httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");

    size_t fb_len = 0;
    if (fb->format == PIXFORMAT_JPEG) {
        fb_len = fb->len;
        res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
    } else {
        jpg_chunking_t jchunk = {req, 0};
        res = frame2jpg_cb(fb, 80, jpg_encode_stream, &jchunk) ? ESP_OK : ESP_FAIL;
        httpd_resp_send_chunk(req, NULL, 0);
        fb_len = jchunk.len;
    }

    esp_camera_fb_return(fb);
    int64_t fr_end = esp_timer_get_time();
    // Serial.printf("JPG: %uB %ums\n", (uint32_t)(fb_len), (uint32_t)((fr_end - fr_start) / 1000));
    return res;
}




esp_err_t index_handler(httpd_req_t *req) {
    // Content to be displayed at the root URL
    const char *html_response = "<html><body><h1>Welcome to My ESP Web Server</h1></body></html>";
    
    // Set the HTTP response headers
    httpd_resp_set_type(req, "text/html");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*"); // Add CORS header if needed
    
    // Send the HTML content as the response
    httpd_resp_send(req, html_response, HTTPD_RESP_USE_STRLEN);
    
    return ESP_OK;
}

static esp_err_t go_handler(httpd_req_t *req)
{
    char direction[10] = {0}; // Buffer to store direction value
    char delay_str[10] = {0}; // Buffer to store delay value
    int delay_length = 1000; // Default delay length

    // Get the query parameter string
    stopCar();
    size_t buf_len = httpd_req_get_url_query_len(req) + 1;
    char *buf = (char *)malloc(buf_len);
    if (!buf)
    {
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }
    if (httpd_req_get_url_query_str(req, buf, buf_len) == ESP_OK)
    {
        // Parse the query parameters to get the direction and delay values
        if (httpd_query_key_value(buf, "dir", direction, sizeof(direction)) == ESP_OK &&
            httpd_query_key_value(buf, "delay", delay_str, sizeof(delay_str)) == ESP_OK)
        {
            // Convert delay value to integer
            delay_length = atoi(delay_str);

            // Check the direction value and perform the corresponding action
            if (strcmp(direction, "forward") == 0)
            {
                // Perform action for forward direction
                WheelAct(HIGH, LOW, HIGH, LOW); // Move forward
            }
            else if (strcmp(direction, "backward") == 0)
            {
                // Perform action for backward direction
                WheelAct(LOW, HIGH, LOW, HIGH); // Move backward
            }
            else if (strcmp(direction, "left") == 0)
            {
                // Perform action for left direction
                WheelAct(HIGH, LOW, LOW, HIGH); // Turn left
            }
            else if (strcmp(direction, "right") == 0)
            {
                // Perform action for right direction
                WheelAct(LOW, HIGH, HIGH, LOW); // Turn right
            }
            // Add more conditions for other directions as needed
            else
            {
                // Invalid direction value
                httpd_resp_send(req, "Invalid direction",20);
                free(buf);
                return ESP_FAIL;
            }

            // Delay to allow the car to complete the movement
            delay(delay_length); // Adjust delay as needed
            stopCar();
            httpd_resp_set_type(req, "text/html");
            httpd_resp_send(req, "OK", 2);
            free(buf);
            return ESP_OK;
        }
    }
    free(buf);
    httpd_resp_send(req, "Direction or delay parameter missing",50);
    return ESP_FAIL;
}

static esp_err_t back_handler(httpd_req_t *req)
{
    WheelAct(LOW, HIGH, LOW, HIGH);
    Serial.println("Back");
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, "OK", 2);
}

static esp_err_t captureFrame_handler(httpd_req_t *req)
{
    Serial.println("capture request");
    camera_fb_t *fb = NULL;
    esp_err_t res = ESP_OK;
    int64_t fr_start = esp_timer_get_time();
    fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Camera capture failed");
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }
    esp_camera_fb_return(fb);
    fb = NULL;
    fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Camera capture failed");
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }
    esp_camera_fb_return(fb);
    fb = NULL;
    fb = esp_camera_fb_get();
    
    if (!fb) {
        Serial.println("Camera capture failed");
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }

    int64_t capture_time = esp_timer_get_time() - fr_start;
    // Serial.println("Frame capture time: %lld us\n", capture_time);

    httpd_resp_set_type(req, "image/jpeg");
    httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");

    size_t fb_len = 0;
    if (fb->format == PIXFORMAT_JPEG) {
        fb_len = fb->len;
        res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
    } else {
        jpg_chunking_t jchunk = {req, 0};
        res = frame2jpg_cb(fb, 80, jpg_encode_stream, &jchunk) ? ESP_OK : ESP_FAIL;
        httpd_resp_send_chunk(req, NULL, 0);
        fb_len = jchunk.len;
    }

    esp_camera_fb_return(fb);
    int64_t fr_end = esp_timer_get_time();
    // Serial.println("JPG: %uB %ums\n", (uint32_t)(fb_len), (uint32_t)((fr_end - fr_start) / 1000));

    return res;
}

static esp_err_t right_handler(httpd_req_t *req)
{
    WheelAct(LOW, HIGH, HIGH, LOW);
    Serial.println("Right");
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, "OK", 2);
}

static esp_err_t stop_handler(httpd_req_t *req)
{
    WheelAct(LOW, LOW, LOW, LOW);
    Serial.println("Stop");
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, "OK", 2);
}

static esp_err_t ledon_handler(httpd_req_t *req)
{
    digitalWrite(gpLed, HIGH);
    Serial.println("LED ON");
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, "OK", 2);
}
static esp_err_t ledoff_handler(httpd_req_t *req)
{
    digitalWrite(gpLed, LOW);
    Serial.println("LED OFF");
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, "OK", 2);
}

void startCameraServer()
{
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.server_port = 80;
    httpd_uri_t go_uri = {
        .uri = "/manualDriving",
        .method = HTTP_GET,
        .handler = go_handler,
        .user_ctx = NULL};

    httpd_uri_t back_uri = {
        .uri = "/back",
        .method = HTTP_GET,
        .handler = back_handler,
        .user_ctx = NULL};

    httpd_uri_t stop_uri = {
        .uri = "/stop",
        .method = HTTP_GET,
        .handler = stop_handler,
        .user_ctx = NULL};

    httpd_uri_t captureFrame_uri = {
        .uri = "/captureFrame",
        .method = HTTP_GET,
        .handler = captureFrame_handler,
        .user_ctx = NULL};

    httpd_uri_t right_uri = {
        .uri = "/right",
        .method = HTTP_GET,
        .handler = right_handler,
        .user_ctx = NULL};

    httpd_uri_t ledon_uri = {
        .uri = "/ledon",
        .method = HTTP_GET,
        .handler = ledon_handler,
        .user_ctx = NULL};

    httpd_uri_t ledoff_uri = {
        .uri = "/ledoff",
        .method = HTTP_GET,
        .handler = ledoff_handler,
        .user_ctx = NULL};

    httpd_uri_t index_uri = {
        .uri = "/",
        .method = HTTP_GET,
        .handler = index_handler,
        .user_ctx = NULL};
    httpd_uri_t capture_uri = {
    .uri       = "/capture",
    .method    = HTTP_GET,
    .handler   = capture_handler,
    .user_ctx  = NULL
    };

    if (httpd_start(&car_httpd, &config) == ESP_OK)
    {
        httpd_register_uri_handler(car_httpd, &index_uri);
        httpd_register_uri_handler(car_httpd, &go_uri);
        httpd_register_uri_handler(car_httpd, &back_uri);
        httpd_register_uri_handler(car_httpd, &stop_uri);
        httpd_register_uri_handler(car_httpd, &captureFrame_uri);
        httpd_register_uri_handler(car_httpd, &right_uri);
        httpd_register_uri_handler(car_httpd, &ledon_uri);
        httpd_register_uri_handler(car_httpd, &ledoff_uri);
        httpd_register_uri_handler(car_httpd, &capture_uri);
    }

}

void WheelAct(int nLf, int nLb, int nRf, int nRb)
{
    digitalWrite(gpLf, nLf);
    digitalWrite(gpLb, nLb);
    digitalWrite(gpRf, nRf);
    digitalWrite(gpRb, nRb);
}
