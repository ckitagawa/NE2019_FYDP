// cd74hct4067.h
// Copyright (C) 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
// Distributed under terms of the MIT license.

#ifndef CD74HCT4067_H
#define CD74HCT4067_H

#include <stdint.h>

#include "gpio.h"
#include "status.h"

#define NUM_CD74HCT4067_CONTROL_PINS 4

typedef struct CD74HCT4067Config {
  GpioAddress s[NUM_CD74HCT4067_CONTROL_PINS];
} CD74HCT4067Config;

void cd74hct4067_init(const CD74HCT4067Config *cfg);

StatusCode cd74hct4067_set_output(const CD74HCT4067Config *cfg, uint8_t value);

#endif  // CD74HCT4067_H
