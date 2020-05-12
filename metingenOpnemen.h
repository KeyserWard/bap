//metingenOpnemen header



#include "TransistorPinnen.h"
#include "code hardware.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define METINGAANTAL 21 //0 tem 20 punten

double* meting_IC_VCE(Transistor*, int, double);

double* meting_IB_VBE(Transistor*, int);

double* meting_beta_IC(Transistor* , int );

double** data_graph(Transistor*, bool, bool, double );

void free_data(double**);


