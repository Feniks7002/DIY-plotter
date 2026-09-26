#include <Arduino.h>

#include "parser.h"
#include <stdlib.h>
  
struct CommandPair {
    char type;
    int code;
};

const CommandPair supported_commands[] = {
    {'G', 0}, {'G', 1}, {'G', 4}, {'G', 21}, {'G', 90},
    {'M', 2}, {'M', 112}
};


bool parse_gcode_line(const char* line, GCodeStructure& cmd) {
    cmd.type = 0;
    cmd.code = 0;
    cmd.has_x = false;
    cmd.x = 0;
    cmd.has_y = false;
    cmd.y = 0;
    cmd.has_z = false;
    cmd.z = 0;
    cmd.has_f = false;
    cmd.f = 0;
    cmd.has_p = false;
    cmd.p = 0;

    if (line[0] == '\0') {
        return false;
    }

    if (line[0] != 'G' && line[0] != 'M') {
        return false;
    }

    cmd.type = line[0];
    int i = 1;
    if (line[i] < '0' || line[i] > '9') {
        return false;
    }

    int code = 0;
    while (line[i] >= '0' && line[i] <= '9') {
        code = code * 10 + (line[i] - '0');
        i++;
    }

    cmd.code = code;

    bool supported = false;
    int count = sizeof(supported_commands) / sizeof(supported_commands[0]);
    for (int j = 0; j < count; j++) {
        if (supported_commands[j].type == cmd.type && supported_commands[j].code == cmd.code) {
            supported = true;
            break;
        }
    }

    if (!supported) {
        return false;
    }

    char param_letter;
    float value;
    int value_z;
    char* end;
    const char* number_start;
    while (line[i] != '\0') {
        if (line[i] == ' ') {
            i++;
            continue;
        } else {
            param_letter = line[i];
            i++;

            number_start = &line[i];
            if (param_letter != 'Z') {
                value = strtod(number_start, &end);
            } else {
                value_z = strtod(number_start, &end);
            }
            
            
            if (end == number_start) {
                return false;
            }

            i = end - line;
        }

        switch (param_letter) {
            case 'X' :
                cmd.has_x = true;
                cmd.x = value;
                break;
            case 'Y' :
                cmd.has_y = true;
                cmd.y = value;
                break;
            case 'Z' :
                cmd.has_z = true;
                cmd.z = value_z;
                break;
            case 'F' :
                cmd.has_f = true;
                cmd.f = value;
                break;
            case 'P' :
                cmd.has_p = true;
                cmd.p = value;
                break;
            default:
                return false;
        }
    }

    return true;
}
