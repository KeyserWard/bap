//aansturing pinnen & SPI
#include "TransistorTester_V3.1.h"

bool startUp = 0;

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
	int pin;		//pin-nummer op 40-pins connector
	int gpio;		//gpio pin-nummer
} pin;

static pin busy = {15, 3};
static pin convst = {16, 4};

//zet correcte Chip Select laag
//params: int device
//return: bool error
bool set_spi (int device) {
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
bool send_data(int device, unsigned char data[], int length) {
	bool e = 1;
	e &= set_spi(device);
	wiringPiSPIDataRW(0, data, length);
	e &= set_spi(RESET);

	return e;
}

//set value from dac
//params: uchar channel(1-4,ALL), int value(0-1023)
//return: bool error
int set_dac_value(unsigned char channel, int value) {
	if (DEBUG) {printf("set DAC channel %d to %d\n", channel, value);}
	bool e = 1;
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

	if (!e) {return -1;} 
	return value;
}

//set voltage from dac
//params: int channel(1-4,ALL), double value(0V-10V)
//return: bool error
double set_dac_voltage(int channel, double voltage) {	
	double value = voltage * 4096 / 2 / 5;

	set_dac_value(channel, value);
	return (value * 5 * 2) / 4096;						//afrondingsfouten voorkomen
}

//set voltage from dac
//params: int channel(1-4,ALL), double value(-5Vtot+5V)
//return: bool error
double set_dac_voltage_offset(int channel, double voltage) {	
	double value = (voltage + 5);
	value = set_dac_voltage(channel, value);
	
	return value;						//afrondingsfouten voorkomen
}

//get value from adc
//params: int channel(1-4,ALL), bool testpunt: hoog zetten als je de spanning op de DUT wil meten 
//			& laag voor diff over de digipot (standaard)
//return: integer value(0-1023)
int get_adc_value(int channel, bool testpunt) {
	bool e = 1;
	channel &= 0b00000011;					//beveiliging tegen verkeerde input
	unsigned char c[2];
	if(testpunt) {
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
	
	int value = (c[0] << 4) + (c[1] >> 4);
	if(!testpunt) {
		if (value >= 2048) {
			value -= 4096;
		}
	}
	if (DEBUG) {
		if ( testpunt) {printf("ADC DUT %d value returned %d\n", channel, value);}
		if (!testpunt) {printf("ADC channel %d value returned %d\n", channel, value);}
	}
	return value;
}

//get voltage from adc
//params: int channel(1-4,ALL), bool testpunt: hoog zetten als je de spanning op de DUT wil meten 
//			& laag voor diff over de digipot (standaard)
//return: double value(0V-10V)
double get_adc_voltage(int channel, bool testpunt) {
	double voltage = get_adc_value(channel, testpunt);
	if(testpunt) {
		voltage = voltage * 10 / 4096;
	}
	else {
		voltage = voltage * 20 / 4096;
	}
	
	return voltage;
}

//get current from adc
//params: int channel(1-4,ALL)
//return: double cuurent
double get_current(int channel) {
	double current = get_adc_voltage(channel, FALSE) / ((DigiPot_value[channel] * 10000 / 256) + 150);
	
	if (DEBUG) {printf("ADC channel %d current returned %fmA\n", channel, current * 1000);}
	return current;
}

//set value for DigiPots
//params: int channel(1-3), uchar value(0-255)
//return: -1 error anders value
int set_digipot(int channel, unsigned char value) {
	if(DEBUG) {printf("set DigiPot channel %d to %d\n", channel, value);}
	bool e = 1;
	channel &= 0b00000011;						//beveiliging tegen verkeerde input => fout er zijn maar drie kanalen
	DigiPot_value[channel] = value;
	e &= send_data(DigiPot1 + channel, &value, 1);

	if(!e) { return -1; }
	return value;
}

//set resistor for DigiPots
//params: int channel(1-3), uchar value(0-Ohm-10KOhm)
//return: -1 error anders value
int set_digipot_resistance(int channel, int R) {
	bool e = 1;
	double value = (R - 3*50) * 256 / 10000;
	if(R > 10150) { value = 255; }
	else if (R < 0) { value = 0; }
	e &= set_digipot(channel, (unsigned char)value);

	if(!e) { return -1; }
	return (int)value;
}

//set switch open/close
//params: int channel(1-3), bool value(0,1)
//return: bool value
bool set_switch(int channel, bool value) {
	if (channel == ALL_CHANNELS) {						//om alle kanalen in 1 keer open of gesloten te zetten
		for(int i = 0; i<3; i++) {
			set_switch(i,!value);						//recursief alle drie de kanalen overlopen
		}
	}
	else {
		digitalWrite(switches[channel].gpio, !value);	//kanaal per kanaal gaan bedienen
	}													
	
	if(DEBUG) {printf("Switch channel %d set to %d\n", channel, (int)value);}
	return value;
}

//setup, zet de juiste instellingen, steeds gebruiken na opstart!
//params:
//return: bool error
bool setup_hardware() {
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
	get_adc_value(CHANNEL1, FALSE);		//na startup eerst dummy opvragen
	get_adc_value(CHANNEL2, FALSE);
	get_adc_value(CHANNEL3, FALSE);

	return 1;
}
