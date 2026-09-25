#include "config.h"
#include "parser.h"

// Bufor danych
const int buffer_size = 64;
static char line_buffer[buffer_size];
static uint8_t buffer_idx = 0;

void setup() {
    Serial.begin(BAUD_RATE);
    while (!Serial) { ; }
    Serial.println(F("DIY Pen Plotter Ready"));
}

void loop() {
    while (Serial.available() > 0) {
        char character = Serial.read();
        
        if (character == '\r') {
            continue;
        }
        
        if (character == '\n') {
            line_buffer[buffer_idx] = '\0';
            if (buffer_idx > 0){
                GCodeStructure cmd;
                if (parse_gcode_line(line_buffer, cmd)) {
                    // Miejsce na wywołanie modułu motion w Kroku 1.3
                    Serial.println(F("ok"));
                } else {
                    Serial.println(F("error: invalid command"));
                }
            }
            buffer_idx = 0;
        } else {
            if (buffer_idx < sizeof(line_buffer) - 1) {
                line_buffer[buffer_idx++] = character;
            } else {
                Serial.println(F("error: buffer overflow"));
                buffer_idx = 0;
            }
        }
    }
    
}