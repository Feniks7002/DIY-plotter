#ifndef CONFIG_H
#define CONFIG_H
#include <Arduino.h>

// --- PINOUT CNC SHIELD V3 (Arduino Uno) ---
#define X_STEP_PIN     2
#define X_DIR_PIN      5

#define Y_STEP_PIN     3
#define Y_DIR_PIN      6

#define ENABLE_PIN     8   // Wspólny pin Enable dla wszystkich osi (LOW = włączone, HIGH = odłączone cewki)

// Pin sterujący osią Z / pisakiem (D11 = Z+ na CNC Shield V3, obsługuje sprzętowy PWM dla serwa)
#define SERVO_PIN      11

// --- KINEMATYKA I MECHANIKA ---
// Silniki 200 kroków/obr, mikrokrok 1/2 (400 mikrokroków/obr), koło GT2 20T (skok 2mm -> 40mm/obr)
#define STEPS_PER_MM   10.0f

// Granice przestrzeni roboczej [mm]
#define X_MAX_MM       180.0f
#define Y_MAX_MM       280.0f

// Domyślne prędkości [mm/min]
#define DEFAULT_FEEDRATE_DRAW   1500.0f
#define DEFAULT_FEEDRATE_TRAVEL 3000.0f

// Pozycje pisaka (wysokość Z w mm lub kąt serwa)
#define Z_PEN_UP       5.0f
#define Z_PEN_DOWN     0.0f

// --- BEZPIECZEŃSTWO I TIMINGI STEROWNIKÓW TMC2209 ---
#define STEP_PULSE_DELAY_US    2    // Minimalny czas trwania impulsu STEP dla TMC2209 (min. 1-2 µs)
#define BAUD_RATE              115200

#endif // CONFIG_H