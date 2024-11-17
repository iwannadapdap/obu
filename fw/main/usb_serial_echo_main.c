/*
 * SPDX-FileCopyrightText: 2023 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/usb_serial_jtag.h"
#include "sdkconfig.h"
#include "esp_log.h"
#include "esp_check.h"
#include "driver/gpio.h"
#include <string.h>

#define BUF_SIZE (1024)
#define ECHO_TASK_STACK_SIZE (4096)
#define OPEN_GPIO_PIN 15       // GPIO for open control (adjust to your choice)
#define CLOSE_GPIO_PIN 16      // GPIO for close control (adjust to your choice)

static const char *TAG = "DSRC";

// Default times (in milliseconds)
static uint32_t open_time = 1000;  // Default open time: 1000 ms
static uint32_t close_time = 1000; // Default close time: 1000 ms

static void gpio_set_high_for_time(int gpio_num, uint32_t time_ms) {
    gpio_set_level(gpio_num, 1);  // Set GPIO to high
    vTaskDelay(pdMS_TO_TICKS(time_ms));  // Wait for the specified time
    gpio_set_level(gpio_num, 0);  // Set GPIO to low
}

static void parse_and_set_time(const char *cmd, uint32_t *time_var) {
    uint32_t value;
    if (sscanf(cmd, "%*s %lu", &value) == 1) {
        *time_var = value;
        ESP_LOGI(TAG, "Set time to %lu milliseconds", value);
    } else {
        ESP_LOGW(TAG, "Invalid time format");
    }
}

static void echo_task(void *arg)
{
    // Configure USB SERIAL JTAG
    usb_serial_jtag_driver_config_t usb_serial_jtag_config = {
        .rx_buffer_size = BUF_SIZE,
        .tx_buffer_size = BUF_SIZE,
    };

    ESP_ERROR_CHECK(usb_serial_jtag_driver_install(&usb_serial_jtag_config));

    // Initialize GPIOs
    gpio_set_direction(OPEN_GPIO_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(CLOSE_GPIO_PIN, GPIO_MODE_OUTPUT);

    // Configure a temporary buffer for the incoming data
    uint8_t *data = (uint8_t *) malloc(BUF_SIZE);
    if (data == NULL) {
        ESP_LOGE("usb_serial_jtag echo", "no memory for data");
        return;
    }
    ESP_LOGI(TAG, "Entering loop...");

    while (1) {
        // Read data from the UART
        int len = usb_serial_jtag_read_bytes(data, (BUF_SIZE - 1), 20 / portTICK_PERIOD_MS);

        if (len > 0) {
            data[len] = '\0';  // Null-terminate the received string
            ESP_LOGI(TAG, "Received: %s", (char *)data);

            // Check for specific commands
            if (strcmp((char *)data, "open\n") == 0) {
                gpio_set_high_for_time(OPEN_GPIO_PIN, open_time);  // Set open GPIO high for open_time
            }
            else if (strcmp((char *)data, "close\n") == 0) {
                gpio_set_high_for_time(CLOSE_GPIO_PIN, close_time);  // Set close GPIO high for close_time
            }
            else if (strncmp((char *)data, "open_time", 9) == 0) {
                parse_and_set_time((char *)data, &open_time);  // Set the open_time
            }
            else if (strncmp((char *)data, "close_time", 10) == 0) {
                parse_and_set_time((char *)data, &close_time);  // Set the close_time
            }
        }
    }

    while (1) {

        int len = usb_serial_jtag_read_bytes(data, (BUF_SIZE - 1), 20 / portTICK_PERIOD_MS);

        // Write data back to the USB SERIAL JTAG
        if (len) {
            usb_serial_jtag_write_bytes((const char *) data, len, 20 / portTICK_PERIOD_MS);
            data[len] = '\0';
            ESP_LOG_BUFFER_HEXDUMP("Recv str: ", data, len, ESP_LOG_INFO);
        }
    }
}

void app_main(void)
{
    ESP_LOGI(TAG, "Starting... ");
    xTaskCreate(echo_task, "USB SERIAL JTAG_echo_task", ECHO_TASK_STACK_SIZE, NULL, 10, NULL);
}
