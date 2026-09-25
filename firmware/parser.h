// Początek
#ifndef PARSER_H
#define PARSER_H

#include <Arduino.h>

// Struktura przechowująca sparsowane parametry polecenia G-code
struct GCodeStructure {
    char type;          // Typ polecenia: 'G' lub 'M' (np. dla G1 -> 'G', dla M112 -> 'M')
    int code;           // Numer polecenia (np. 1 dla G1, 4 dla G4, 112 dla M112)
    
    bool has_x;         // Czy parametr X wystąpił w linii? (true / false)
    float x;            // Odczytana wartość osi X
    
    bool has_y;
    float y;            // Odczytana wartość osi Y
    
    bool has_z;
    float z;            // Odczytana wartość osi Z
    
    bool has_f;
    float f;            // Wartość posuwu (feedrate)
    
    bool has_p;
    float p;            // Czas pauzy w sekundach

};

// Wywołanie funkcji bool która, przyjmuje i pracuje na strukturze GCodeStructure 
bool parse_gcode_line(const char* line, GCodeStructure& cmd);

// Koniec
#endif