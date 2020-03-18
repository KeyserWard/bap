//header file
#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int* start_up_chipSelect();

int* start_up_switch();

void shut_down(int*, int*);

int set_up_channel(int, int*);

int* spi_communication(int, int*, int);
