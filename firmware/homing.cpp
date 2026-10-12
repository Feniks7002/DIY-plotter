#include <Arduino.h>

#include "homing.h"
#include "config.h"

void homing_init() {
    pinMode(ESWITCH_PIN_X, INPUT_PULLUP);
    pinMode(ESWITCH_PIN_Y, INPUT_PULLUP);
}

static bool home_single_axis(int step_pin, int step_dir, int switch_pin, float max_workspace) {
    long max_steps = round(max_workspace * 1.2f * STEPS_PER_MM);
    long steps_to_do = round(abs(HOMING_OFFSET_MM * STEPS_PER_MM));
    unsigned long steps_delay_us = 60000000UL / (DEFAULT_FEEDRATE_DRAW * STEPS_PER_MM);
    
    // Ruch osi do krańcówki
    long current_pos = 0;
    digitalWrite(step_dir, LOW);
    while (digitalRead(switch_pin) == HIGH) {
        if (++current_pos >= max_steps) {return false;}
        digitalWrite(step_pin, HIGH);
        delayMicroseconds(STEP_PULSE_DELAY_US);
        digitalWrite(step_pin, LOW);
        delayMicroseconds(steps_delay_us);
    }

    // Odskok od krańcówki o 2mm
    digitalWrite(step_dir, HIGH);
    for (long i = 0; i < steps_to_do; i++) {
        digitalWrite(step_pin, HIGH);
        delayMicroseconds(STEP_PULSE_DELAY_US);
        digitalWrite(step_pin, LOW);
        delayMicroseconds(steps_delay_us);
    }

    return true;
}

bool homing() {
    if (!home_single_axis(X_STEP_PIN, X_DIR_PIN, ESWITCH_PIN_X,  X_MAX_MM)) {return false;} 
    if (!home_single_axis(Y_STEP_PIN, Y_DIR_PIN, ESWITCH_PIN_Y, Y_MAX_MM)) {return false;}

    return true;
}