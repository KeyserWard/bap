#include "TransistorPinnen.h"

#define R_W 50		//in ohm
#define R_AB 10000	//in ohm

bool chose_config(const char* configuratie, int channel) {	// returnt true als de cofiguratie correct is doorgegeven
	if(!strcmp(configuratie, "Open")) {				
		set_switch(channel, true);
		set_dac_voltage_offset(channel, 0);		//Ground = 5V
		return true;
	} 		
	else if(!strcmp(configuratie, "Vcc")) {
		set_switch(channel, true);
		set_dac_voltage_offset(channel, 4);		//Vcc = 9V
		return true;
	}	
	else if(!strcmp(configuratie, "Ground")) {
		set_switch(channel, true);
		set_dac_voltage_offset(channel, 0);		//Ground = 5V
		return true;
	} 
	else { return false; }

}

int stroom_door_pin(int channel) { //channel van de gevraagde digipot
	double current = get_current(channel);
	if (current > 0)
		return 1;
	else if (current < 0)
		return -1;
	else return 0;
}

bool locate_base(Transistor* trans) {
	const char* const configLijst[3] = {"Open", "Vcc", "Ground"};
	const int permuLijst1[6] = {1, 2, 0, 2, 0, 1};
	const int permuLijst2[6] = {2, 1, 2, 0, 1, 0};
	int metingLijst[6][3];					//{{b0, b1, b2}{b1, e1, c1}...}
	int i=0, j=0;
	bool eersteInGevonden = false;
	bool eersteUitGevonden = false;
	int inBewaar, uitBewaar;

	//eerst alle mogelijke permutaties uitmeten
	
	while(i<6){
		
		//configuratie kiezen
		chose_config(configLijst[j], switches[0].channel);						// 0 0 1 1 2 2 
		chose_config(configLijst[permuLijst1[i]], switches[1].channel);			// 1 2 0 2 0 1
		chose_config(configLijst[permuLijst2[i]], switches[2].channel);			// 2 1 2 0 1 0
		
		
		//meten
		metingLijst[i][0]= stroom_door_pin(switches[0].channel);			
		metingLijst[i][1] = stroom_door_pin(switches[1].channel);
		metingLijst[i][2] = stroom_door_pin(switches[2].channel);
		
		i++;
		j = i/2;
		//mogelijks een wachtlus nodig zodat de meting niet verstoord wordt
		int w;
		for(w=0;w<1000;w++){}
		
	}
	//zoeken naar de basis
		for(i=0;i<6;i++){
		for(j=0;j<3;j++){
			if(metingLijst[i][j] == 1){
				if(!eersteInGevonden){
					inBewaar = j;
					eersteInGevonden = true;
				}
				else {
					if(inBewaar == j){
						trans->basisGateChannel = switches[j].channel;
						trans->type = "NPN";
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
						trans->basisGateChannel = switches[j].channel;
						trans->type = "PNP";
						return true;
					}
				}
			}
		}	
	}
	if(trans->basisGateChannel == -1 || strcmp(trans->type, "Onbepaald") ){
		if (DEBUG) {printf("transistor onbepaald: defect");}
		return false;																	//false wanneer de geen basis of type gevonden is, dus transistor is defect
	}
	return false;
}

void locate_collector_emitter(Transistor* transistor){
	int i, basisIndex, emitterIndex, collectorIndex;
	double meting;
	int channels[3] = {CHANNEL1, CHANNEL2 ,CHANNEL3};
													
	for(i=0; i<3; i++){		
		set_digipot_resistance(channels[i], 5000);
		if(channels[i] == transistor->basisGateChannel)
			basisIndex = i;
	}
	collectorIndex = (basisIndex + 1) %3;
	emitterIndex = 	(basisIndex + 2) %3;											
	if(strcmp(transistor->type,"NPN"))
		chose_config("Vcc", transistor->basisGateChannel);	
	else
		chose_config("Ground", transistor->basisGateChannel);	
	
	chose_config("Vcc", channels[collectorIndex]);		
	chose_config("Ground", channels[emitterIndex]);		
	meting = get_current(channels[emitterIndex]); 	
														
	chose_config("Ground", channels[collectorIndex]);		
	chose_config("Vcc", channels[emitterIndex]);		
	
	if((meting >  get_current(channels[emitterIndex])) && (strcmp(transistor->type,"NPN") || meting >  get_current(channels[emitterIndex])) && (strcmp(transistor->type,"PNP"))) {
		//de 2 GES met elkaar vergelijken
		transistor->collectorDrainChannel = channels[collectorIndex];		//GES in eerste situatie
		transistor->emitterSourceChannel = channels[emitterIndex];	

	} else {
		transistor->collectorDrainChannel = channels[emitterIndex];			//GES in tweede situatie
		transistor->emitterSourceChannel = channels[collectorIndex];
	}
	
}
/*
int main(int argc, char **argv) {
	setup_hardware();
	
	Transistor T;
	locate_base(&T);
	locate_collector_emitter(&T);
	if (DEBUG) {printf("%s transistor, basis at pin %d\n",T.type, T.basisGateChannel);}
	if (DEBUG) {printf("\tcollecter at pin %d\n\temitter at pin %d\n", T.collectorDrainChannel, T.emitterSourceChannel);}

}
*/
