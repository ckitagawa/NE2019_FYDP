#include "wait.h"

#include "stm32f4xx.h"

void wait(void) {
  __WFI();
}
