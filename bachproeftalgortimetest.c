//testAlgortime


#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct{
	int basis;
	int collector;
	int emitter;
	char* type;		//pnp of npn
} BJT;


void chose_config(char* configuratie, int pin) {
	if(!strcmp(configuratie, "Open")){				//in 3 if's ter beveiliging
		//schakel de switch aan voor de pin
	}
	if(!strcmp(configuratie, "Vcc")){
		//hang de pin aan de voedingsspanning
	}
	if(!strcmp(configuratie, "Ground")){
		//hang de pin aan de ground
	}
}

bool locate_base(int* pinList, BJT* transistor){						//bepaalt of de transistor npn of pnp is, en de locatie van de basis. returnt false als er geen basis te vinden is
	char* configLijst[3] = {"Open", "Vcc", "Ground"};
	int permuLijst1[6] = {1, 2, 0, 2, 0, 1};
	int permuLijst2[6] = {2, 1, 2, 0, 1, 0};
	int i, j, w, b=0;
	
	bool eersteInGevonden = false;
	bool eersteUitGevonden = false;
	int inBewaar, uitBewaar;

	int metingLijst[6][3];				//array van 6 arrays met 3 metingen. -1 is stroom uit de pin, +1 is stroom in de pin, 0 is geen stroom
	while(i<6){					// 18 elementen moeten opgevuld worden
		//instellen voor iedere permutatie
		
		chose_config(configLijst[b], pinList[0]);
		chose_config(configLijst[permuLijst1[i]], pinList[1]);
		chose_config(configLijst[permuLijst2[i]], pinList[2]);
		
	
		metingLijst[i][0]= stroom_door_pin(pinList[0]);			//metingen inschrijven
		metingLijst[i][1] = stroom_door_pin(pinList[1]);
		metingLijst[i][2] = stroom_door_pin(pinList[2]);
		
		
		i++;
		b = i/2;			//omdat j een int is, zal het programma i/2 afronden naar ofwel 0, 1 of 2
		/*mogelijks een wachtlus nodig zadot de meting niet verstoord wordt
		for(w=0;w<1000;w++){}
		*/
	}
	//metinglijst is nu volledig opgesteld. bij npn zal stroom in de basis lopen op 2x dezelfde pin
	//bij pnp zal stroom uit de basis lopen op 2x dezelfde pin
	
	for(i=0;i<6;i++){
		for(j=0;j<3;j++){
			if(metingLijst[i][j] == 1){
				if(!eersteInGevonden){
					inBewaar = j;
					eersteInGevonden = true;
				}
				else {
					if(inBewaar == j){
						transistor->basis = pinList[j];
						transistor->type = "NPN";
						return true;
					}
				}	
			}
			
			if(metingLijst[i][j] == -1){
				if(!eersteUitGevonden){
					uitBewaar = j;
					eersteUitGevonden = true;
				}
				else{
					if(uitBewaar == j){
						transistor->basis = pinList[j];
						transistor->type = "PNP";
						return true;
					}
				}
			}
			
		}
		
	}
	if(transistor->basis == -1 || strcmp(transistor->type, "Onbepaald") ){
		return false;		
	}

}


int stroom_door_pin(int pin){							
	int stroom = 0;
	
	return stroom;
}

void locate_collector_Emitter(){ 
	
}

int main(){
	int pinlist[3] = {0, 1, 2};			// {B, C, E}
	BJT transistor = {-1, -1, -1, "Onbepaald"};		
	if(!locate_base(pinlist, &transistor)){
		printf("yes!");
	}
	return 0;
}
