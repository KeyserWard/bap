//aansturing pinnen & SPI
#include <stdio.h>
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

#define R_SWITCH 8	//R-on switch 5-10 Ohm (nog te meten, volgens datasheet)

#define DEBUG TRUE

_Bool startUp = 0;

typedef struct {
	int channel;
	int pin;		//pin-nummer op 40-pins connector
	int gpio;		//gpio pin-nummer
	int speed;		//CLk Speed in Hz
	int mode;		//SPI MODE1-4
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

typedef struct {
	int pin;		//pin-nummer op 40-pins connector
	int gpio;		//gpio pin-nummer
} pin;

static pin busy = {15, 3};
static pin convst = {16, 4};

int DigiPot_value[3];

//zet correcte Chip Select laag
//params: int device
//return: bool error
_Bool set_spi (int device) {
	for (int i = 1; i < AANTAL_SPI_DEVICES; i++) {		//alle pinnen hoog zetten
		digitalWrite(spi_devices[i].gpio, HIGH);
	}
	digitalWrite(convst.gpio, HIGH);					//hangt samen met RD voor ADC
	
	if (0 <= device && device <= AANTAL_SPI_DEVICES) {	//actieve CS hoog zetten, tenzij RESET (=0)
		if (device == RESET) {return 1;}				//reset, niets anders laag zetten
		digitalWrite(spi_devices[device].gpio, LOW);	//devise_CS laag zetten
		if (device == ADC) {							//indien adc ook convst hangt samen met RD
			digitalWrite(convst.gpio, LOW);
		}
		return 1;
	}
	return 0;											//foutieve parameter device
}

//stuur data over SPI
//params: int device, uchar data, int lengte van data #bytes
//return: bool error
_Bool send_data(int device, unsigned char data[], int length) {
	_Bool e = 1;
	e &= set_spi(device);
	wiringPiSPIDataRW(0, data, length);
	e &= set_spi(RESET);
	
	return e;
}

//setup, zet de juiste instellingen, steeds gebruiken na opstart!
//params:
//return: bool error
_Bool setup_hardware() {
	wiringPiSetup();
	
	if (!startUp){
		wiringPiSPISetupMode(0, SPI_SPEED, SPI_MODE_0);
		startUp = 1;
	}
	
	for (int i = 1; i < AANTAL_SPI_DEVICES; i++) {		//CS pinnen instellen
		pinMode(spi_devices[i].gpio, OUTPUT);
		digitalWrite(spi_devices[i].gpio, HIGH);		//standaard hoog zetten, allemaal uit
	}
	
	// set up DAC en set to 0V
	unsigned char c1[3] = {0b01100000 | ALL_CHANNELS, 0b00000000, 0b00000000};	//select internal ref for al DAC's
	send_data(DAC, c1, 3);
	unsigned char c2[3] = {0b00110000 | ALL_CHANNELS, 0b00000000, 0b00000000};	//write 0 to and update all DAC registers
	send_data(DAC, c2, 3);

	// set up DigiPot en set to 10kOhm
	unsigned char c3 = 0b11111111;
	DigiPot_value[CHANNEL1] = c3;				//255 = 10kOhm
	send_data(DigiPot1, &c3, 1);
	unsigned char c4 = 0b11111111;
	DigiPot_value[CHANNEL2] = c4;				//255
	send_data(DigiPot2, &c4, 1);	
	unsigned char c5 = 0b11111111;
	DigiPot_value[CHANNEL3] = c5;				//255
	send_data(DigiPot3, &c5, 1);
	
	
	for (int i = 0; i < 3; i++) {						//controle pinnen voor switch instellen
		pinMode(switches[i].gpio, OUTPUT);
		digitalWrite(switches[i].gpio, LOW);			//standaard laag zetten, alle switches open (beveiliging)
	}
	
	//setup adc
	pinMode(busy.gpio, INPUT);
	pinMode(convst.gpio, OUTPUT);
	digitalWrite(convst.gpio, HIGH);
		
	return 1;
}

//set value from dac
//params: uchar channel(1-4,ALL), int value(0-1023)
//return: bool error
int set_dac_value(unsigned char channel, int value) {
	_Bool e = 1;
	channel &= 0b00001111;								//beveiliging tegen verkeerde input
	channel |= 0b00110000;								//command + kanaal
	unsigned char data_msb = value>>4;					//12bit data opdelen in twee bytes
	unsigned char data_lsb = (value & 0b1111)<<4;
	unsigned char data[3] = {							//samenvoegen & in 1 maal versturen
		channel,
		data_msb,
		data_lsb
	};
	e &= send_data(DAC, data, 3);
	
	if (DEBUG) {printf("DAC channel %d set to %d", channel, value);}

	if (!e) {return -1;} 
	return value;
}

//set voltage from dac
//params: int channel(1-4,ALL), double value(0V-10V)
//return: bool error
double set_dac_voltage(int channel, double voltage) {	
	int value = voltage * 4096 / 2 / 5;
	set_dac_value(channel, value);
	
	return value * 5 * 2 / 4096;						//afrondingsfouten voorkomen
}

//set voltage from dac
//params: int channel(1-4,ALL), double value(-5Vtot+5V)
//return: bool error
double set_dac_voltage_offset(int channel, double voltage) {	
	int value = (voltage + 5) * 4096 / 2 / 5;
	set_dac_value(channel, value);
	
	return (value - 5) * 5 * 2 / 4096;						//afrondingsfouten voorkomen
}

//get value from dac
//params: int channel(1-4,ALL), bool testpunt: hoog zetten als je de spanning op de DUT wil meten 
//			& laag voor diff over de digipot (standaard)
//return: integer value(0-1023)
int get_adc_value(int channel, _Bool testpunt) {
	_Bool e = 1;
	channel &= 0b00000011;					//beveiliging tegen verkeerde input
	unsigned char c[2];
	if(testpunt == 1) {
		c[0] = 0b11001100;
		c[0] += (channel<<4);
		c[1] = 0b00000000;
	}
	else {					
		c[0] = 0b00000100;
		c[0] += (channel<<4);
		c[1] = 0b00000000;
	}				
	
	e &= send_data(ADC, c, 2);
	while(!digitalRead(busy.gpio)) {}
	c[0] = 0x00;
	c[1] = 0x00;	
	e &= send_data(ADC, c, 2);				
	
	int i = (c[0] << 4) + (c[1] >> 4);
	if (i >= 2048) {
		i -= 4096;
	}
	if (DEBUG) {
		if ( testpunt) {printf("ADC DUT %d value returned %d", channel, i);}
		if (!testpunt) {printf("ADC channel %d value returned %d", channel, i);}
	}
	return i;
}

//get voltage from dac
//params: int channel(1-4,ALL), bool testpunt: hoog zetten als je de spanning op de DUT wil meten 
//			& laag voor diff over de digipot (standaard)
//return: double value(0V-10V)
double get_adc_voltage(int channel, _Bool testpunt) {
	double d = get_adc_value(channel, testpunt);
	if(testpunt) {
		d = d * 10 / 4096;
	}
	else {
		d = d * 20 / 4096;
	}
	
	if (DEBUG) {
		if ( testpunt) {printf("ADC DUT %d voltage returned %f", channel, d);}
		if (!testpunt) {printf("ADC channel %d voltage returned %f", channel, d);}
	}
	return d;
}

//get current from dac
//params: int channel(1-4,ALL)
//return: double cuurent
double get_current(int channel) {
	double current = get_adc_voltage(channel, FALSE) / ((DigiPot_value[channel] * 10000 / 256) + 150);
	
	//if (DEBUG) {std::cout << "channel " << channel << "  data current returned: " << current << "\n";}
	return current;
}

//set value for DigiPots
//params: int channel(1-3), uchar value(0-255)
//return: -1 error anders value
int set_digipot(int channel, unsigned char value) {
	_Bool e = 1;
	channel &= 0b00000011;						//beveiliging tegen verkeerde input => fout er zijn maar drie kanalen
	DigiPot_value[channel] = value;
	e &= send_data(DigiPot1 + channel, &value, 1);

	if(DEBUG) {printf("DigiPot channel %d set to %d", channel, value);}
	if(!e) { return -1; }
	return value;
}

//set resistor for DigiPots
//params: int channel(1-3), uchar value(0-Ohm-10KOhm)
//return: -1 error anders value
int set_digipot_resistance(int channel, int R) {
	_Bool e = 1;
	int value = (R - 3*50) * 256/10000;
	DigiPot_value[channel] = value;
	e &= set_digipot(channel, value);

	if(!e) { return -1; }
	return value;
}

//set switch open/close
//params: int channel(1-3), bool value(0,1)
//return: bool value
_Bool set_switch(int channel, _Bool value) {
	if (channel == ALL_CHANNELS) {						//om alle kanalen in 1 keer open of gesloten te zetten
		for(int i = 0; i<3; i++) {
			set_switch(i,!value);						//recursief alle drie de kanalen overlopen
		}
	}
	else {
		digitalWrite(switches[channel].gpio, !value);	//kanaal per kanaal gaan bedienen
	}													
	
	if(DEBUG) {printf("Switch channel %d set to %d", channel, (int)value);}
	return value;
}



/*
int main(int argc, char **argv) {
	setup_hardware();

	while(1){
		//test digipots
		
		set_digipot(CHANNEL1, 255);
		set_digipot(CHANNEL2, 255);
		set_digipot(CHANNEL3, 255);

		//delay(100);
		
		
		//test switch
		
		set_switch(CHANNEL1, TRUE);
		set_switch(CHANNEL2, TRUE);
		set_switch(CHANNEL3, TRUE);
		
		delay(2500);
		set_switch(CHANNEL1, FALSE);
		set_switch(CHANNEL2, FALSE);
		set_switch(CHANNEL3, FALSE);
		delay(2500);
		
		
		//test DAC
		
		set_dac_value(CHANNEL1, 3072);
		set_dac_value(CHANNEL2, 2048);
		set_dac_value(CHANNEL3, 1024);
		
		
		//test ADC
		
		get_adc_voltage(CHANNEL1, FALSE);
		get_adc_voltage(CHANNEL2, FALSE);
		get_adc_voltage(CHANNEL3, FALSE);
		get_adc_voltage(CHANNEL1, TRUE);
		get_adc_voltage(CHANNEL2, TRUE);
		get_adc_voltage(CHANNEL3, TRUE);
		get_current(CHANNEL1);
		get_current(CHANNEL2);
		get_current(CHANNEL3);
		delay(250);
		
	}
}
*/
