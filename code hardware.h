//header for code hardware
#include <iostream>
#include <wiringPi.h>
#include <wiringPiSPI.h>

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

int t = 0;

typedef struct {
	int channel;
	int pin;		//pin-nummer op 40-pins connector
	int gpio;		//gpio pin-nummer
	int speed;		//CLk Speed in Hz
	int mode;		//MODE1-4
} spi_device_id;

static spi_device_id spi_devices [AANTAL_SPI_DEVICES] = {
	{RESET,		-1,		-1,		-1,			-1},
	{DAC,		7,		7,		1000000,	SPI_MODE_0},
	{DigiPot1,	35,		24,	 	1000000, 	SPI_MODE_0},
	{DigiPot2,	33,		23,	 	1000000, 	SPI_MODE_0},
	{DigiPot3,	31,		22,		1000000, 	SPI_MODE_0},
	{ADC,		29,		21,		1000000, 	SPI_MODE_0},
	{LCD,		0,		0,		1000000,	SPI_MODE_0},
	{TOUCHPAD,	0,		0,		1000000,	SPI_MODE_0}
};

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

int set_spi (int );

int send_data(int, unsigned char[], int);

int setup_hardware();

int set_dac_value(unsigned char, int);

int set_dac_voltage(int, double);

int get_adc_value(int);

double get_adc_voltage(int);

double get_current(int);

int set_digipot(int, unsigned char);

int set_switch(int, bool);


