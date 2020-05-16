//TransistorPinnen.h

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
//#include "SPI-GPIO.h"

typedef struct{
	int basisGateChannel;
	int collectorDrainChannel;
	int emitterSourceChannel;
	char* type;		//pnp of npn
	char* structuur; //MOSFET of BJT
} Transistor;


bool chose_config(const char*, int);

bool locate_base(Transistor*);

double Weerstand(int, int);

int stroom_door_pin(int);

void locate_collector_emitter(Transistor*);
