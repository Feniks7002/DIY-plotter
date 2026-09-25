#ifndef MOTION_H
#define MOTION_H

#include "parser.h"

void motion_init();
void motion_execute(const GCodeStructure& cmd); 
void motion_emergency_stop();

#endif