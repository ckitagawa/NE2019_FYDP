#include "interrupt.h"

#include "stm32f4xx_interrupt.h"

void interrupt_init(void) {
  stm32f4xx_interrupt_init();
}
