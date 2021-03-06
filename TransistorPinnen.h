//TransistorPinnen.h

#ifndef TRANSISTORPINNEN_H
#define TRANSISTORPINNEN_H

#include "TransistorTester.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct{
	int basisGateChannel;
	int collectorDrainChannel;
	int emitterSourceChannel;
	char* type;		//pnp of npn
	char* structuur; //MOSFET of BJT
} Transistor;

bool chose_config(const char*, int);

bool locate_base(Transistor*);

double measure_current(int);

void zet_potwaarde(int, int);

int stroom_door_pin(int);

void locate_collector_emitter(Transistor*);

#endif
