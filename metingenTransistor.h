//metingenTransistor header

#ifndef METINGENTRANSISTOR_H
#define METINGENTRANSISTOR_H

#include "TransistorPinnen.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

double meting_VBE(Transistor, double, int)

void meting_IC_VCE(Transistor*, double, double*, double*, int);

void meting_beta_IC(Transistor*, double***, int);

#endif
