#include "gpio_it.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "gpio.h"
#include "interrupt_def.h"
#include "status.h"
#include "stm32f4xx.h"
#include "stm32f4xx_interrupt.h"
#include "stm32f4xx_syscfg.h"

typedef struct GpioItInterrupt {
  GpioAddress address;
  GpioItCallback callback;
  void *context;
} GpioItInterrupt;

static GpioItInterrupt s_gpio_it_interrupts[GPIO_PINS_PER_PORT];

void gpio_it_init(void) {
  GpioItInterrupt empty_interrupt = { { 0 } };
  for (int16_t i = 0; i < GPIO_PINS_PER_PORT; i++) {
    s_gpio_it_interrupts[i] = empty_interrupt;
  }
}

// Pins 0-1 are mapped to IRQ Channel 5, 2-3 to 6 and 4-15 to 7;
static uint8_t prv_get_irq_channel(uint8_t pin) {
  switch (pin) {
    case 0:
      return EXTI0_IRQn;
    case 1:
      return EXTI1_IRQn;
    case 2:
      return EXTI2_IRQn;
    case 3:
      return EXTI3_IRQn;
    case 4:
      return EXTI4_IRQn;
    case 5:
    case 6:
    case 7:
    case 8:
    case 9:
      return EXTI9_5_IRQn;
    case 10:
    case 11:
    case 12:
    case 13:
    case 14:
    case 15:
      return EXTI15_10_IRQn;
    default:
      return 0;
  }
}

StatusCode gpio_it_register_interrupt(const GpioAddress *address, const InterruptSettings *settings,
                                      InterruptEdge edge, GpioItCallback callback, void *context) {
  if (address->port >= NUM_GPIO_PORTS || address->pin >= GPIO_PINS_PER_PORT) {
    return status_code(STATUS_CODE_INVALID_ARGS);
  }
  // Try to register on NVIC and EXTI. Both must succeed for the callback to be set.
  s_gpio_it_interrupts[address->pin].address = *address;
  s_gpio_it_interrupts[address->pin].callback = callback;
  s_gpio_it_interrupts[address->pin].context = context;

  SYSCFG_EXTILineConfig(address->port, address->pin);
  StatusCode status = stm32f4xx_interrupt_exti_enable(address->pin, settings, edge);
  // If the operation failed clean up by removing the callback and pass the error up the stack.
  if (!status_ok(status)) {
    s_gpio_it_interrupts[address->pin].callback = NULL;
    return status;
  }
  status = stm32f4xx_interrupt_nvic_enable(prv_get_irq_channel(address->pin), settings->priority);
  // If the operation failed clean up by removing the callback and pass the error up the stack.
  if (!status_ok(status)) {
    s_gpio_it_interrupts[address->pin].callback = NULL;
    return status;
  }

  return STATUS_CODE_OK;
}

StatusCode gpio_it_trigger_interrupt(const GpioAddress *address) {
  if (address->port >= NUM_GPIO_PORTS || address->pin >= GPIO_PINS_PER_PORT) {
    return status_code(STATUS_CODE_INVALID_ARGS);
  }

  return stm32f4xx_interrupt_exti_trigger(address->pin);
}

// Callback runner for GPIO which runs callbacks based on which callbacks are associated with an IRQ
// channel. The function runs the callbacks which have a flag raised in the range [lower_bound,
// upperbound].
static void prv_run_gpio_callbacks(uint8_t lower_bound, uint8_t upper_bound) {
  uint8_t pending = 0;
  for (int i = lower_bound; i <= upper_bound; i++) {
    stm32f4xx_interrupt_exti_get_pending(i, &pending);
    if (pending && s_gpio_it_interrupts[i].callback != NULL) {
      s_gpio_it_interrupts[i].callback(&s_gpio_it_interrupts[i].address,
                                       s_gpio_it_interrupts[i].context);
    }
    stm32f4xx_interrupt_exti_clear_pending(i);
  }
}

// IV Handler for pins 0.
void EXTI0_IRQHandler(void) {
  prv_run_gpio_callbacks(0, 0);
}

// IV Handler for pins 1.
void EXTI1_IRQHandler(void) {
  prv_run_gpio_callbacks(1, 1);
}

// IV Handler for pins 1.
void EXTI2_IRQHandler(void) {
  prv_run_gpio_callbacks(2, 2);
}

// IV Handler for pins 3.
void EXTI3_IRQHandler(void) {
  prv_run_gpio_callbacks(3, 3);
}

// IV Handler for pins 3.
void EXTI4_IRQHandler(void) {
  prv_run_gpio_callbacks(4, 4);
}

// IV Handler for pins 3.
void EXTI9_5_IRQHandler(void) {
  prv_run_gpio_callbacks(5, 9);
}

// IV Handler for pins 3.
void EXTI15_10_IRQHandler(void) {
  prv_run_gpio_callbacks(10, 15);
}

StatusCode gpio_it_mask_interrupt(const GpioAddress *address, bool masked) {
  if (address->port >= NUM_GPIO_PORTS || address->pin >= GPIO_PINS_PER_PORT) {
    return status_code(STATUS_CODE_INVALID_ARGS);
  }
  return stm32f4xx_interrupt_exti_mask_set(address->pin, masked);
}
