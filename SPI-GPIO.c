//aansturing pinnen & SPI


#include "SPI-GPIO.h"

#define SPEED 1000000
#define chipSelectArrayLength 5

int* start_up(){ //maakt de array aan waarin de gpio pinnen staan voor de SPI chip select
	int* chipSelectArray = (int*)malloc(5*sizeof(int)); 
	int i;
	
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

void shut_down(int* chipSelectArray){ //geeft alle arrays vrij
	 free(chipSelectArray);
}

int set_up_channel(int chipSelectIndex, int* chipSelectArray){ //zet de spi klaar met de gekozen snelheid en chip
	int fd = wiringPiSPISetup(0, SPEED);
	int i;
	for(i=0; i<chipSelectArrayLength; i++){
		digitalWrite(chipSelectArray[i], HIGH);
	}
	digitalWrite(chipSelectArray[i], LOW);
	return fd;
}

