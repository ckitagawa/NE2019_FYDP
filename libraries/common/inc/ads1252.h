// ads1252.h
// Copyright (C) 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
// Distributed under terms of the MIT license.

#ifndef ADS1252_H
#define ADS1252_H

#include <stdint.h>

#include "gpio.h"

typedef struct ADS1252Config {
  GpioAddress sclk;  // PA8 PA10
  GpioAddress data;  // PA9 PA11
} ADS1252Config;

void ads1252_init(const ADS1252Config *cfg);

void ads1252_enable(const ADS1252Config *cfg);

void ads1252_reset(const ADS1252Config *cfg);

void ads1252_read(const ADS1252Config *cfg, int32_t *buf);

#endif  // ADS1252_H
