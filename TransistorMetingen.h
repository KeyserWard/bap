//metingenTransistor header

#ifndef TRANSISTORMETINGEN_H
#define TRANSISTORMETINGEN_H

#include "TransistorPinnen.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

double meting_VBE(Transistor, double, int);

void meting_IC_VCE(Transistor*, double, double*, double*, int);

void meting_beta_IC(Transistor*, double*, double*, int);

void meting_IC_VBE(Transistor*, double, double*, double *, int);


#endif
