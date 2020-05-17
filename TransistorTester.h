//header for code hardware
#include <stdio.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <stdbool.h>

#define SPI_SPEED 1000000
#define SPI_MODE_0 0
#define SPI_MODE_1 1
#define SPI_MODE_2 2
#define SPI_MODE_3 3

#define RESET 0
#define DAC 1
#define DigiPot1 2
#define DigiPot2 3
#define DigiPot3 4
#define ADC 5
#define LCD 6
#define TOUCHPAD 7
#define AANTAL_SPI_DEVICES 8

#define CHANNEL1 0b00000000		//0
#define CHANNEL2 0b00000001		//1
#define CHANNEL3 0b00000010		//2
#define CHANNEL4 0b00000011		//3
#define ALL_CHANNELS 0b00001111

#define R_SWITCH 8

#define DEBUG FALSE

typedef struct {
	int channel;	
	int pin;		//pin-nummer op 40-pins connector
	int gpio;		//gpio pin-nummer
} switch_id;

static switch_id switches[3] = {	//actief laag
	{CHANNEL1,	36,		27},
	{CHANNEL2,	37,		25},
	{CHANNEL3,	38,		28}
};

int DigiPot_value[3];



bool set_spi (int );

bool send_data(int, unsigned char[], int);

int set_dac_value(unsigned char, int);

double set_dac_voltage(int, double);

double set_dac_voltage_offset(int, double);

int get_adc_value(int, bool);

double get_adc_voltage(int, bool);

double get_current(int);

int set_digipot(int, unsigned char);

int set_digipot_resistance(int, int);

bool set_switch(int, bool);

bool setup_hardware();
