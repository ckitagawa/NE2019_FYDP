// adc.c
// Copyright (C) 2019 ckitagawa <ckitagawa@edu.uwaterloo.ca>
// Distributed under terms of the MIT license.

#include "adc.h"

#include <stdint.h>
#include "stm32f4xx_adc.h"
#include "stm32f4xx_rcc.h"

void adc_init(void) {
  ADC_InitTypeDef init = {
    .ADC_Resolution = ADC_Resolution_12b,
    .ADC_ScanConvMode = DISABLE,
    .ADC_ContinuousConvMode = DISABLE,
    .ADC_ExternalTrigConvEdge = ADC_ExternalTrigConvEdge_None,
    .ADC_ExternalTrigConv = ADC_ExternalTrigConv_T2_TRGO,
    .ADC_DataAlign = ADC_DataAlign_Right,
    .ADC_NbrOfConversion = 1,
  };
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);
  ADC_DeInit();
  ADC_Init(ADC1, &init);
  ADC_Cmd(ADC1, ENABLE);
}

uint16_t adc_read(uint8_t channel) {
  ADC_RegularChannelConfig(ADC1, channel, 1, ADC_SampleTime_15Cycles);
  ADC_SoftwareStartConv(ADC1);
  while (ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC) == RESET) {
  }
  return ADC_GetConversionValue(ADC1);
}
