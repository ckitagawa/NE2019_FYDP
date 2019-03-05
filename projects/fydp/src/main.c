// Example program for STM32F072 Controller board or Discovery Board.
// Blinks the LEDs sequentially.
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#include "adc.h"
#include "ads1252.h"
#include "cd74hct4067.h"
#include "common_misc.h"  // Various helper functions/macros.
#include "delay.h"
#include "gpio.h"  // General Purpose I/O control.
#include "interrupt.h"
#include "soft_timer.h"
#include "stm32f4xx_rcc.h"

#define DISCARD 7
#define SAMPLES DISCARD + 7

// Depending on which board you are working with you will need to (un)comment
// the relevant block of GPIO pins. Generally these would be in a configuration file somewhere and
// we normally write configurations only for the controller board. Controller board LEDs static
// const GpioAddress leds[] = {
//   { .port = GPIO_PORT_A, .pin = 0 },  //
//   { .port = GPIO_PORT_A, .pin = 1 },  //
//   { .port = GPIO_PORT_A, .pin = 2 },  //
//   { .port = GPIO_PORT_A, .pin = 3 },  //
// };

int main(void) {
  // Enable various peripherals
  interrupt_init();
  soft_timer_init();
  gpio_init();
  printf("Booting\n");

  // DEBUG LED TEST
  //
  // GpioSettings led_settings = {
  //   .direction = GPIO_DIR_OUT,        // The pin needs to output.
  //   .state = GPIO_STATE_HIGH,         // Start in the "on" state.
  //   .alt_function = GPIO_ALTFN_NONE,  // No connections to peripherals.
  //   .resistor = GPIO_RES_NONE,        // No need of a resistor to modify floating logic levels.
  // };

  // // Init all of the LED pins
  // for (size_t i = 0; i < SIZEOF_ARRAY(leds); i++) {
  //   gpio_init_pin(&leds[i], &led_settings);
  // }

  // // Keep toggling the state of the pins from on to off with a 50 ms delay between.
  // while (true) {
  //   for (size_t i = 0; i < SIZEOF_ARRAY(leds); i++) {
  //     gpio_toggle_state(&leds[i]);
  //     for (volatile uint32_t i = 0; i < 1000000; ++i) {
  //     }
  //   }
  // }

  // MULTIPLEXER TEST
  //
  // LED Test code
  // CD74HCT4067Config config = { .s = { { .port = GPIO_PORT_C, .pin = 4 },
  //                                     { .port = GPIO_PORT_C, .pin = 5 },
  //                                     { .port = GPIO_PORT_C, .pin = 6 },
  //                                     { .port = GPIO_PORT_C, .pin = 7 } } };
  // cd74hct4067_init(&config);
  // while (true) {
  //   for (size_t i = 0; i < 16; ++i) {
  //     cd74hct4067_set_output(&config, i);
  //     for (volatile uint32_t i = 0; i < 1000000; ++i) {
  //     }
  //   }
  // }

  // ADS1252 TEST
  // ADS1252Config cfg = { .data = { .port = GPIO_PORT_A, .pin = 11 },
  //                       .sclk = { .port = GPIO_PORT_A, .pin = 10 } };
  // ads1252_init(&cfg);
  // ads1252_reset(&cfg);
  // volatile int32_t res = 0;

  // adc_init();
  // while (true) {
  //   ads1252_read(&cfg, &res);
  //   // res = adc_read(0);
  //   delay_ms(500);
  //   printf("%ld\n", res);
  // }

  ADS1252Config adc2 = { .data = { .port = GPIO_PORT_A, .pin = 9 },
                         .sclk = { .port = GPIO_PORT_A, .pin = 8 } };
  ADS1252Config adc1 = { .data = { .port = GPIO_PORT_A, .pin = 11 },
                         .sclk = { .port = GPIO_PORT_A, .pin = 10 } };
  ads1252_init(&adc1);
  ads1252_reset(&adc1);
  ads1252_init(&adc2);
  ads1252_reset(&adc2);
  ads1252_enable(&adc1);
  ads1252_enable(&adc2);
  CD74HCT4067Config pd1 = { .s = { { .port = GPIO_PORT_C, .pin = 4 },
                                   { .port = GPIO_PORT_C, .pin = 5 },
                                   { .port = GPIO_PORT_C, .pin = 6 },
                                   { .port = GPIO_PORT_C, .pin = 7 } } };
  CD74HCT4067Config pd2 = { .s = { { .port = GPIO_PORT_C, .pin = 0 },
                                   { .port = GPIO_PORT_C, .pin = 1 },
                                   { .port = GPIO_PORT_C, .pin = 2 },
                                   { .port = GPIO_PORT_C, .pin = 3 } } };
  CD74HCT4067Config led1 = { .s = { { .port = GPIO_PORT_C, .pin = 8 },
                                    { .port = GPIO_PORT_C, .pin = 9 },
                                    { .port = GPIO_PORT_C, .pin = 10 },
                                    { .port = GPIO_PORT_C, .pin = 11 } } };
  CD74HCT4067Config led2 = { .s = { { .port = GPIO_PORT_C, .pin = 12 },
                                    { .port = GPIO_PORT_C, .pin = 13 },
                                    { .port = GPIO_PORT_C, .pin = 14 },
                                    { .port = GPIO_PORT_C, .pin = 15 } } };
  cd74hct4067_init(&pd1);
  cd74hct4067_init(&led1);
  cd74hct4067_init(&pd2);
  cd74hct4067_init(&led2);
  cd74hct4067_set_output(&led2, 11);
  cd74hct4067_set_output(&pd2, 11);

  // cd74hct4067_set_output(&led1, 0);
  // cd74hct4067_set_output(&pd1, 0);
  // int32_t z = 0;
  // while (true) {
  //   ads1252_read(&adc1, &z);
  //   printf("%ld\n", z);
  //   delay_ms(500);
  // }

  // Calibrate
  printf("Callibrating\n");
  int32_t callibrations[20] = { 0 };
  int32_t x = 0;
  int32_t acc = 0;
  for (uint16_t i = 0; i < 10; ++i) {
    acc = 0;
    cd74hct4067_set_output(&pd1, i);
    cd74hct4067_set_output(&led1, i);
    delay_us(500);
    for (uint16_t j = 0; j < SAMPLES; ++j) {
      ads1252_read(&adc1, &x);
      if (j >= DISCARD) {
        acc += x;
      }
    }
    callibrations[i] = acc / (SAMPLES - DISCARD);
  }
  cd74hct4067_set_output(&led1, 11);
  cd74hct4067_set_output(&pd1, 11);
  for (uint16_t i = 0; i < 10; ++i) {
    acc = 0;
    cd74hct4067_set_output(&pd2, i);
    cd74hct4067_set_output(&led2, i);
    delay_us(500);
    for (uint16_t j = 0; j < SAMPLES; ++j) {
      ads1252_read(&adc2, &x);
      if (j >= DISCARD) {
        acc += x;
      }
    }
    callibrations[i + 10] = acc / (SAMPLES - DISCARD);
  }
  cd74hct4067_set_output(&led2, 11);
  cd74hct4067_set_output(&pd2, 11);

  // Read
  int32_t reading = { 0 };
  printf("Running\n");
  while (true) {
    for (uint16_t i = 0; i < 10; ++i) {
      cd74hct4067_set_output(&pd1, i);
      cd74hct4067_set_output(&led1, i);
      delay_us(500);
      printf("0,%d,%ld", i, callibrations[i]);
      for (uint16_t j = 0; j < SAMPLES; ++j) {
        ads1252_read(&adc1, &reading);
        if (j >= DISCARD) {
          printf(",%ld", reading);
        }
      }
      printf("\n");
    }
    cd74hct4067_set_output(&led1, 11);
    cd74hct4067_set_output(&pd1, 11);
    delay_ms(250);

    for (uint16_t i = 0; i < 10; ++i) {
      cd74hct4067_set_output(&pd2, i);
      cd74hct4067_set_output(&led2, i);
      delay_us(500);
      printf("1,%d,%ld", i, callibrations[i + 10]);
      for (uint16_t j = 0; j < SAMPLES; ++j) {
        ads1252_read(&adc2, &reading);
        if (j >= DISCARD) {
          printf(",%ld", reading);
        }
      }
      printf("\n");
    }
    cd74hct4067_set_output(&led2, 11);
    cd74hct4067_set_output(&pd2, 11);
    delay_ms(250);
  }

  return 0;
}
