//TransistorMetingen
#include "TransistorMetingen.h"

double meting_VBE(Transistor *trans, double VB, int RB) {
	set_dac_voltage_offset(trans->emitterSourceChannel, 0);
	set_digipot_resistance(trans->basisGateChannel, RB);
	set_dac_voltage_offset(trans->basisGateChannel, VB);
	int w;
	for(w=0;w<1000000;w++){}
	double VBE = get_adc_voltage(trans->basisGateChannel, 1) - get_adc_voltage(trans->emitterSourceChannel, 1);
	return VBE;
}

void meting_IC_VCE(Transistor *trans, double IB, double *data_IC, double *data_VCE, int dataLen)
					//IB in mA
{					//dataLen zijn het aantal coordinaten, double data[dataLen][2]
	double VCE, IC; //VCE kan niet groter worden dan 4!
	//test
	double RB, VB, VBE;
	if (IB <= 0.01) {		//IB stroom tss 10uA en 1uA
		RB = 10 / IB;
		VBE = meting_VBE(trans, 0.6, RB);
		VB = 0.1 + VBE;
	}			
	else if (IB <= 0.05) {	//IB stroom tss 10uA en 50uA
		RB = 100 / IB;
		VBE = meting_VBE(trans, 0.6, RB);
		VB = 0.1 + VBE;
	}		
	else if (IB <= 0.5) {	//IB stroom tss 50uA en 500uA
		RB = 500 / IB;
		VBE = meting_VBE(trans, 1.1, RB);
		VB = 0.5 + VBE;
	}
	else  {					//IB stroom tss 500uA en 5mA
		RB = 4000 / IB;
		VBE = meting_VBE(trans, 4.6, RB);
		VB = 4 + VBE;
	}
	printf("VBE = %fmV\n",VBE*1000);
	
	//IB instellen
	set_digipot_resistance(trans->basisGateChannel, (int)RB);
	set_dac_voltage_offset(trans->basisGateChannel, VB);
	
	//weerstanden instellen
	set_digipot_resistance(trans->collectorDrainChannel, 500); //bij VCE = 4V mag I max = 5mA => R moet minimaal 800ohm zijn
	set_digipot_resistance(trans->emitterSourceChannel, 500);  //moet dit?
	
	set_dac_voltage_offset(trans->emitterSourceChannel, 0);
		
	int i;
	for (i = 0; i < dataLen; i++)
	{
		VCE = (double)(i * 4.0) / dataLen;		
		
		//VCE inverteren als de bjt een pnp is
		if (!strcmp(trans->type, "PNP")) { VCE *= -1; }
		
		//IC in mA (RE + RC = 4KOhm)
		IC = VCE / 1.000; 
		
		if (IC <= 5 && IC >= -5)	//beveiliging (theoretisch)
		{ // -5 <= IC <= 5
			set_dac_voltage_offset(trans->collectorDrainChannel, VCE);	
			
			int w;
			for(w=0;w<1000000;w++){}
			
			//IB controleren
			double ib = get_current(trans->basisGateChannel);
			printf("IB = %fmA\t",ib*1000);

			
			//IC opmeten
			data_VCE[i] = (double)get_adc_voltage(trans->collectorDrainChannel, 1) - get_adc_voltage(trans->emitterSourceChannel, 1); //VCE controle
			data_IC[i] = (double)get_current(trans->collectorDrainChannel);	
			printf("VCE = %fV\n",data_VCE[i]);
		}
		else
		{
			data_VCE[i] = VCE;
			data_IC[i] = 0;
		}

		//data_VCE[i] = 0;
		//data_IC[i] = 0;
	}
}

void meting_beta_IC(Transistor *trans, double ***data, int dataLen)
{ //dataLen zijn het aantal coordinaten, double data[dataLen][2]
	double punt[2] = {0, 0};
	int RC, RB, VCE, i;
	double Ic; //Ic in mA
	for (i = 0; i < dataLen; i++)
	{
		Ic = i / 4;

		//bepaling npn of pnp
		if (!strcmp(trans->type, "PNP"))
			Ic *= -1;

		//Ic op het bord zetten en punt invullen
		if (Ic >= 5 || Ic == 0)
		{
			punt[0] = Ic;
			punt[1] = 0;
		}
		else
		{
			if (Ic > 0 && Ic <= 2.5)
			{
				VCE = 2000 * Ic;
				set_digipot_resistance(trans->collectorDrainChannel, 2000);
			}
			else if (Ic > 2.5 && Ic < 5)
			{
				VCE = 1000 * Ic;
				set_digipot_resistance(trans->collectorDrainChannel, 2000);
			}
			set_dac_voltage_offset(trans->collectorDrainChannel, VCE);
			set_dac_voltage_offset(trans->basisGateChannel, VCE);
			set_dac_voltage_offset(trans->emitterSourceChannel, 0);
			punt[0] = get_current(trans->collectorDrainChannel);
			punt[1] = punt[0] / get_current(trans->basisGateChannel);
		}
		*data[i] = punt;
		punt[0] = 0;
		punt[1] = 0;
	}
}

int main(int argc, char **argv){		//testomgeving
	setup_hardware();

	Transistor T;
	locate_base(&T);
	locate_collector_emitter(&T);
	printf("transistor:\n\tcollector:\t%d\n\temitor:\t\t%d\n\tbasis:\t\t%d\n\ttype:\t\t%s\n", T.collectorDrainChannel, T.emitterSourceChannel, T.basisGateChannel, T.type);
	double IC[100];
	double VCE[100];
	double IB = 0.025; //10uA
	printf("press key to continue\n");
	getchar();
	meting_IC_VCE(&T, IB, IC, VCE, 100);
	for(int a = 0; a<100;a++){
		printf("%d,%f,%f\n", a, IC[a], VCE[a]);
	}
	IB = 0.075; //5uA
	printf("press key to continue\n");
	getchar();
	meting_IC_VCE(&T, IB, IC, VCE, 100);
	for(int a = 0; a<100;a++){
		printf("%d,%f,%f\n", a, IC[a], VCE[a]);
	}
	IB = 0.150; //10uA
	printf("press key to continue\n");
	getchar();
	meting_IC_VCE(&T, IB, IC, VCE, 100);
	for(int a = 0; a<100;a++){
		printf("%d,%f,%f\n", a, IC[a], VCE[a]);
	}
}

/*
//metingen

#include "metingenOpnemen.h"


#define METINGAANTAL 21 //0 tem 20 punten

double* meting_IC_VCE(Transistor* trans, int xWaarde, double IB){		//IB in A
	double* punt = (double*)malloc(sizeof(double)*2);
	double VCE = xWaarde / 4;
	int RB = (int)VCE / IB;				//VBE = VCE
	double IC;
	//VCE inverteren als de bjt een pnp is
	if(!strcmp(trans->type, "pnp"))
		VCE *= -1;
	IC = (double)VCE / 2.5;  //IC in mA
	//weerstanden instellen
	
	set_digipot_resistance(trans->collectorDrainChannel, 2500);	//bij VCE = 10V mag I max = 5mA => R moet minimaal 2000ohm zijn
	set_digipot_resistance(trans->emitterSourceChannel, 2500); //moet dit?
	
	if(IC <= 5 && IC >= -5){				// -5 <= IC <= 5
		set_dac_voltage(trans->collectorDrainChannel, VCE);
		set_dac_voltage(trans->emitterSourceChannel, 0);

		//IB instellen
		set_digipot_resistance(trans->basisGateChannel, RB);
		set_dac_voltage(trans->basisGateChannel, VCE);	//VBE = VCE

		//IC opmeten
		punt[0] = get_adc_voltage(trans->collectorDrainChannel, 0) - get_adc_voltage(trans->emitterSourceChannel, 0); //VCE controle
		punt[1] = get_current(trans->collectorDrainChannel);	
			
	} else {
		punt[0] = VCE;
		punt[1] = 0;
	}
	
	
	return punt;		//punt[x,y] in [V, mA]
}
//nog niet af!
double* meting_IB_VBE(Transistor* trans, int xWaarde){
	double* punt = (double*)malloc(sizeof(double)*2);
	
	
	punt[0] = get_adc_voltage(trans->basisGateChannel, 0);
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
		if(Ic > 0 && Ic <= 2.5) {
			VCE = 2000 * Ic;
			set_digipot_resistance(trans->collectorDrainChannel, 2000);
		}
		else if(Ic > 2.5 && Ic < 5){
			VCE = 1000 * Ic;
			set_digipot_resistance(trans->collectorDrainChannel, 2000);
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


int main(int argc, char **argv){		//testomgeving
	Transistor trans = {CHANNEL1, CHANNEL2, CHANNEL3, "npn", "BJT"};
	bool IC = true;
	bool beta = false;
	double IB = 0.005; //5mA
	double** coorArr = data_graph(&trans, IC, beta, IB);
	free_data(coorArr);
	
}
*/
