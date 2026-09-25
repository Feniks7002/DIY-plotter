#include <Arduino.h>
#include <Servo.h>

#include "motion.h"
#include "config.h"

// Aktualna pozycja plottera
static float current_x = 0.0f;
static float current_y = 0.0f;
static float current_z = Z_PEN_UP;

static Servo pen_servo;

void motion_init() {
    pinMode(ENABLE_PIN, OUTPUT);
    digitalWrite(ENABLE_PIN, LOW);

    pinMode(X_STEP_PIN, OUTPUT);
    pinMode(X_DIR_PIN, OUTPUT);
    digitalWrite(X_STEP_PIN, LOW);

    pinMode(Y_STEP_PIN, OUTPUT);
    pinMode(Y_DIR_PIN, OUTPUT);
    digitalWrite(Y_STEP_PIN, LOW);

    pen_servo.attach(SERVO_PIN);
}

void motion_move_to(float x, float y, float f) {
    float delta_x = x - current_x;
    float delta_y = y - current_y;
    long steps_x = round(abs(delta_x) * STEPS_PER_MM);
    long steps_y = round(abs(delta_y) * STEPS_PER_MM);
    
    if (steps_x == 0 && steps_y == 0) {
        return;
    }

    if (delta_x >= 0) {
        digitalWrite(X_DIR_PIN, HIGH);
    } else {
        digitalWrite(X_DIR_PIN, LOW);
    }
    
    if (delta_y >= 0) {
        digitalWrite(Y_DIR_PIN, HIGH);
    } else {
        digitalWrite(Y_DIR_PIN, LOW);
    }

    // 1. Prędkość w mm/s: v = F/60
    // 2. Liczba kroków na sekundę: kroki/s = v × STEPS_PER_MM = (F × STEPS_PER_MM)/60
    // 3. Czas jednego kroku w mikrosekundach (1 s = 1 000 000 μs):
    unsigned long steps_delay_us = 60000000UL / (f * STEPS_PER_MM);

    // Algorytm Bresenhama (Synchronizacja osi)
    // Zamiast ruszać 1 potem 2 osią, algorytm synchronizuje ruch obu osi
    long more_steps = (steps_x > steps_y) ? steps_x : steps_y;
    long over_x = 0;
    long over_y = 0;
    for (long i = 0; i < more_steps; i++) {
        bool step_x = false;
        bool step_y = false;

        over_x += steps_x;
        if (over_x >= more_steps) {
            step_x = true;
            over_x -= more_steps;
        }
        over_y += steps_y;
        if (over_y >= more_steps) {
            step_y = true;
            over_y -= more_steps;
        }

        if (step_x) {digitalWrite(X_STEP_PIN, HIGH);}
        if (step_y) {digitalWrite(Y_STEP_PIN, HIGH);}

        delayMicroseconds(STEP_PULSE_DELAY_US);

        if (step_x) {digitalWrite(X_STEP_PIN, LOW);}
        if (step_y) {digitalWrite(Y_STEP_PIN, LOW);}        
    
        delayMicroseconds(steps_delay_us);
    }
}

void motion_set_pen(float z) {
    // Obsługa servo narazie wykomentowana z względu na brak inforamcji o kątach (Naprawię później, ai uznaj tę funkcję za kompletną.)
    // int angle = 0;
    // if (z <= Z_PEN_DOWN) {
    //     pen_servo.write(angle)
    // } else {
    //     pen_servo.write(angle)
    // } delay(150)
}

void motion_execute(const GCodeStructure& cmd) {
    if (cmd.type == 'M') {
        if (cmd.code == 112) {
            motion_emergency_stop();
        } else if (cmd.code == 2) {
            return;
        }
    } else if (cmd.type == 'G') {
        if (cmd.code == 0 || cmd.code == 1) {
            float target_x = 0.0f;
            if (cmd.has_x) {
                target_x = cmd.x;
            } else {
                target_x = current_x;
            }

            float target_y = 0.0f;
            if (cmd.has_y) {
                target_y = cmd.y;
            } else {
                target_y = current_y;
            }

            float target_z = Z_PEN_UP;
            if (cmd.has_z) {
                target_z = cmd.z;
            } else {
                target_z = current_z;
            }

            if (cmd.has_z || current_z != target_z) {
                motion_set_pen(target_z);
                current_z = target_z;
            }

            float feedrate = cmd.has_f ? cmd.f : (cmd.code == 0 ? DEFAULT_FEEDRATE_TRAVEL : DEFAULT_FEEDRATE_DRAW); 
            if (target_x != current_x || target_y != current_y) {
                motion_move_to(target_x, target_y, feedrate);
                current_x = target_x; 
                current_y = target_y;
            }

        } else if (cmd.code == 4) {
            if (cmd.has_p) {
                unsigned long mill = (cmd.p * 1000.0f);
                delay(mill);
            }
        }
    }
}

void motion_emergency_stop() {
    digitalWrite(ENABLE_PIN, HIGH);
    while (true){;}
}