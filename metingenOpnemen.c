//metingen


#include "TransistorPinnen.h"
#include "code hardware.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdbool.h>

#define METINGAANTAL 21 //0 tem 20 punten


double* meting_IC_VCE(Transistor* trans, int xWaarde, double IB){
	double* punt = (double*)malloc(sizeof(double)*2);
	double VCE = xWaarde / 4;		//VCE zal max tot (METINGAANTAL - 1) / 4 gaan => 5V
	int RB = (int)VCE / IB
	//VCE instellen afhankelijk van x waarde
	
	Weerstand(trans->collectorDrainChannel, 2000);	//bij VCE = 5V mag I max = 5mA => 1k 
	Weerstand(trans->emitterSourceChannel, 2000); //moet dit?
	set_dac_voltage(trans->collectorDrainChannel, VCE);
	set_dac_voltage(trans->emitterSourceChannel, 0);


	//IB instellen
	Weerstand(trans->basisGateChannel, RB);
	set_dac_voltage(trans->basisGateChannel, VCE);	//VBE = VCE
	
	//IC opmeten
	punt[0] = get_adc_voltage(trans->collectorDrainChannel) - get_adc_voltage(trans->emitterSourceChannel); //VCE controle
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

double** data_graph(Transistor* trans, bool IC, bool beta, double IB){ //IC = true, IC tov VCE. IC = False, IB tov VCE. beta = true, beta tov IC
	int i;
	double** coorArr= (double**)malloc(sizeof(double*)*METINGAANTAL);
	for(i=0;i<METINGAANTAL;i++){
	//	coorArr[i] = (double*)malloc(sizeof(double)*2);
		if(IC && !beta){
			coorArr[i] = meting_IC_VCE(trans, i, IB);
			
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


int main(){		//testomgeving
	Transistor trans = {CHANNEL1, CHANNEL2, CHANNEL3, "npn", "BJT"};
	bool IC = true;
	bool beta = false;
	double IB = 0.005 //5mA
	double** coorArr = data_graph(&trans, IC, beta, IB);
	free_data(coorArr);
	
	return 0;
}
