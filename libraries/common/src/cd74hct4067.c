// cd74hct4067.c
// Copyright (C) 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
// Distributed under terms of the MIT license.

#include "cd74hct4067.h"

void cd74hct4067_init(const CD74HCT4067Config *cfg) {
  GpioSettings settings = {
    .direction = GPIO_DIR_OUT,
    .state = GPIO_STATE_LOW,
    .resistor = GPIO_RES_NONE,
    .alt_function = GPIO_ALTFN_NONE,
  };
  for (uint16_t i = 0; i < NUM_CD74HCT4067_CONTROL_PINS; ++i) {
    gpio_init_pin(&cfg->s[i], &settings);
  }
}

StatusCode cd74hct4067_set_output(const CD74HCT4067Config *cfg, uint8_t value) {
  if (value >= 16) {
    return status_code(STATUS_CODE_INVALID_ARGS);
  }
  for (uint16_t i = 0; i < NUM_CD74HCT4067_CONTROL_PINS; ++i) {
    if (value & (0x01) << i) {
      gpio_set_state(&cfg->s[i], GPIO_STATE_HIGH);
    } else {
      gpio_set_state(&cfg->s[i], GPIO_STATE_LOW);
    }
  }
  return STATUS_CODE_OK;
}
