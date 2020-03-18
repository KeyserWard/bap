//aansturing pinnen & SPI


#include "SPI-GPIO.h"

#define SPEED 1000000
#define chipSelectArrayLength 5

int* start_up_chipSelect(){ //maakt de array aan waarin de gpio pinnen staan voor de SPI chip select
	wiringPiSetup();
	int* chipSelectArray = (int*)malloc(5*sizeof(int)); 
	
	chipSelectArray[0] = 4; 	
	chipSelectArray[1] = 19; 	
	chipSelectArray[2] = 13;  
	chipSelectArray[3] = 6;  
	chipSelectArray[4] = 5;
	/* De array bevat de GPIO nummers vanop de RPI, dus in de commandolijn moet -g gebruikt worden*/
	for(i=0; i<chipSelectArrayLength; i++){
		pinMode(chipSelectArray[i], OUPUT);
	}
	return chipSelectArray;
}

int* start_up_switch(){
	int* switchArray = (int*)malloc(3*sizeof(int));
	/* gpio : s1 = 16, s2 = 26, s3 = 20 */
	switchArray[0] = 16;
	switchArray[1] = 26;
	switchArray[2] = 20;
	/*De array bevat de GPIO pinnen voor de switches van de transistoren open of dicht te zetten*/
	return switchArray;
}

void shut_down(int* chipSelectArray, int* SwitchArray){ //geeft alle arrays vrij
	free(chipSelectArray);
	free(SwitchArray);
}

int set_up_channel(int chipSelectIndex, int* chipSelectArray){ //zet de spi klaar met de gekozen snelheid en chip
	wiringPiSetup();
	int fd = wiringPiSPISetup(0, SPEED);
	int i;
	for(i=0; i<chipSelectArrayLength; i++){
		digitalWrite(chipSelectArray[i], HIGH);
	}
	digitalWrite(chipSelectArray[chipSelectIndex], LOW);
	return fd;
}

int* spi_communication(int chipSelectIndex, int* chipSelectArray, int len){
	unsigned char* data = (unsigned char*)malloc(len*sizeof(unsigned char));
	int fd = set_up_channel(chipSelectIndex, chipSelectArray);
	
	//onafgewerkt voorlopig
}

