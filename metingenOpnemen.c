//metingen


#include "TransistorPinnen.h"
#include "code hardware.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define METINGAANTAL 21 //0 tem 20 punten



double* meting_IC_VCE(Transistor* trans, int xWaarde, double IB){
	double* punt = (double*)malloc(sizeof(double)*2);
	double VCE = xWaarde / 4;
	int RB = (int)VCE / IB;				//VBE = VCE
	float IC;
	//VCE inverteren als de bjt een pnp is
	if(!strcmp(trans->type, "pnp"))
		VCE *= -1;
	IC = (float) VCE / 2,5;  //IC in mA
	//weerstanden instellen
	
	Weerstand(trans->collectorDrainChannel, 2500);	//bij VCE = 10V mag I max = 5mA => R moet minimaal 2000ohm zijn
	Weerstand(trans->emitterSourceChannel, 2500); //moet dit?
	
	if(IC <= 5 && IC >= -5){				// -5 <= IC <= 5
		set_dac_voltage(trans->collectorDrainChannel, VCE);
		set_dac_voltage(trans->emitterSourceChannel, 0);
	
		//IB instellen
		Weerstand(trans->basisGateChannel, RB);
		set_dac_voltage(trans->basisGateChannel, VCE);	//VBE = VCE
		
		//IC opmeten
		punt[0] = get_adc_voltage(trans->collectorDrainChannel) - get_adc_voltage(trans->emitterSourceChannel); //VCE controle
		punt[1] = (float)get_current(trans->collectorDrainChannel) / 1000;		
	} else {
		punt[0] = VCE;
		punt[1] = 0;
	}
	
	
	return punt;		//punt[x,y] in [V, mA]
}

double* meting_IB_VBE(Transistor* trans, int xWaarde){
	double* punt = (double*)malloc(sizeof(double)*2);
	
	
	punt[0] = get_adc_voltage(trans->basisGateChannel);
	punt[1] = get_current(trans->basisGateChannel);
	return punt;
}

double* meting_beta_IC(Transistor* trans, int xWaarde){
	double* punt = (double*)malloc(sizeof(double)*2);
	int RC, RB;
	double Ic = xWaarde / 4;		//Ic in mA
	int VCE;
	
	//bepaling npn of pnp
	if(!strcmp(trans->type, "pnp"))
		Ic *= -1;
	
	//Ic op het bord zetten en punt invullen
	if(Ic >= 5 || Ic == 0){
		punt[0] = Ic;
		punt[1] = 0;
	} 
	else{
		if(Ic > 0 && Ic <= 2,5) {
			VCE = 2000 * Ic;
			Weerstand(trans->collectorDrainChannel, 2000);
		}
		else if(Ic > 2,5 && Ic < 5){
			VCE = 1000 * Ic;
			Weerstand(trans->collectorDrainChannel, 2000);
		}
		set_dac_voltage(trans->collectorDrainChannel, VCE);
		set_dac_voltage(trans->basisGateChannel, VCE);
		punt[0] = get_current(trans->collectorDrainChannel);
		punt[1] = punt[0] / get_current(trans->basisGateChannel);
	}
	
	return punt;
}

double** data_graph(Transistor* trans, bool IC, bool beta, double IB){ //IC = true, IC tov VCE. IC = False, IB tov VCE. beta = true, beta tov IC
	int i;
	double** coorArr= (double**)malloc(sizeof(double*)*METINGAANTAL);
	for(i=0;i<METINGAANTAL;i++){
	//	coorArr[i] = (double*)malloc(sizeof(double)*2);
		if(IC && !beta){
			coorArr[i] = meting_IC_VCE(trans, i, IB);
			
		}
		else if(!IC && !beta){
			coorArr[i] = meting_IB_VBE(trans, i);
		}
		else if(!IC && beta){
			coorArr[i] = meting_beta_IC(trans, i);	
		}
		else{
			printf("foute parameters");
		}
	}
	return coorArr;
	
}

void free_data(double** data){
	int i;
	for(i=0;i<METINGAANTAL;i++)
		free(data[i]);
	free(data);
}


int main(){		//testomgeving
	Transistor trans = {CHANNEL1, CHANNEL2, CHANNEL3, "npn", "BJT"};
	bool IC = true;
	bool beta = false;
	double IB = 0.005 //5mA
	double** coorArr = data_graph(&trans, IC, beta, IB);
	free_data(coorArr);
	
	return 0;
}
