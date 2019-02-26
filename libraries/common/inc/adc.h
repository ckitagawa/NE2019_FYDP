// adc.h
// Copyright (C) 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
// Distributed under terms of the MIT license.

#ifndef ADC_H
#define ADC_H

#include <stdint.h>

void adc_init(void);

uint16_t adc_read(uint8_t channel);

#endif  // ADC_H
