//metingen


#include "TransistorPinnen.h"
#include "code hardware.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdbool.h>

#define METINGAANTAL 21 //0 tem 20 punten


double* meting_IC_VCE(Transistor* trans, int xWaarde, double IB){
	double* punt = (double*)malloc(sizeof(double)*2);
	double VCE;
	int RB;
	//VCE instellen afhankelijk van x waarde
	VCE = xWaarde / 4;
	Weerstand(trans->collectorDrainChannel, 5000);
	Weerstand(trans->emitterSourceChannel, 5000); //moet dit?
	set_dac_voltage(trans->collectorDrainChannel, VCE);
	set_dac_voltage(trans->emitterSourceChannel, 0);
	/*mogelijke controle?
	VCE = get_adc_voltage(trans->collectorDrainChannel) - get_adc_voltage(trans->emitterSourceChannel);
	*/
	punt[0] = VCE;
	//IB instellen
	RB = 
	Weerstand(trans->basisGateChannel, (int)RB);
	set_dac_voltage(trans->basisGateChannel, IB*RB);
	
	//IC opmeten
	punt[1] = get_current(trans->collectorDrainChannel);
	
	return punt;
}

double* meting_IB_VCE(Transistor* trans, int xWaarde){
	double* punt = (double*)malloc(sizeof(double)*2);
	
	return punt;
}

double* meting_beta_IC(Transistor* trans, int xWaarde){
	double* punt = (double*)malloc(sizeof(double)*2);
	
	return punt;
}

double** data_graph(Transistor* trans, bool IC, bool beta){ //IC = true, IC tov VCE. IC = False, IB tov VCE. beta = true, beta tov IC
	int i;
	double** coorArr= (double**)malloc(sizeof(double*)*METINGAANTAL);
	for(i=0;i<METINGAANTAL;i++){
	//	coorArr[i] = (double*)malloc(sizeof(double)*2);
		if(IC && !beta){
			coorArr[i] = meting_IC_VCE(trans, i);
			
		}
		else if(!IC && !beta){
			coorArr[i] = meting_IB_VCE(trans, i);
			
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

