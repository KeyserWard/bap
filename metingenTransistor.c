//metingen




void meting_IC_VCE(Transistor* trans, double IB, double*** data, int dataLen){		//dataLen zijn het aantal coordinaten, double data[dataLen][2]
	double VCE, IC;										//VCE kan niet groter worden dan 4!
	int RB, i;
	double punt[2] = {0,0};
	for(i=0;i<dataLen;i++){
	
	 	VCE = (double)i / 4;
		RB = (int)VCE / IB;								//VBE = VCE
	
		//VCE inverteren als de bjt een pnp is
		if(!strcmp(trans->type, "PNP"))
			VCE *= -1;
		IC = (double) VCE / 2,5;  							//IC in mA
		//weerstanden instellen
		
		Weerstand(trans->collectorDrainChannel, 2500);	//bij VCE = 10V mag I max = 5mA => R moet minimaal 2000ohm zijn
		Weerstand(trans->emitterSourceChannel, 2500); //moet dit?
		
		if(IC <= 5 && IC >= -5){				// -5 <= IC <= 5
			set_dac_voltage_offset(trans->collectorDrainChannel, VCE);
			set_dac_voltage_offset(trans->emitterSourceChannel, 0);
		
			//IB instellen
			Weerstand(trans->basisGateChannel, RB);
			set_dac_voltage_offset(trans->basisGateChannel, VCE);	//VBE = VCE
			
			//IC opmeten
			punt[0] = (double)get_adc_voltage(trans->collectorDrainChannel, true) - get_adc_voltage(trans->emitterSourceChannel, true); //VCE controle
			punt[1] = (double)get_current(trans->collectorDrainChannel);		
		} else {
			punt[0] = VCE;
			punt[1] = 0;
		}
		
		*data[i] = punt;
		punt[0] = 0;
		punt[1] = 0;
	}
	

}


void meting_beta_IC(Transistor* trans, double*** data, int dataLen){  //dataLen zijn het aantal coordinaten, double data[dataLen][2]
	double punt[2] = {0,0};
	int RC, RB, VCE, i;
	double Ic;		//Ic in mA
	for(i=0;i<dataLen;i++){
		Ic = i / 4;
		
		//bepaling npn of pnp
		if(!strcmp(trans->type, "PNP"))
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



