import os
from cffi import FFI


class Transistor:
    def __init__(self):
        self.ffi = FFI()
        self.ffi.cdef(
            """
            typedef struct {
                int basisGateChannel;
                int collectorDrainChannel;
                int emitterSourceChannel;
                char* type;		//pnp of npn
                char* structuur; //MOSFET of BJT
            } Transistor;

            bool locate_base(Transistor*);
            void locate_collector_emitter(Transistor*);
            void meting_Beta_IC(Transistor*, double*, double*, int);
            void meting_IC_VCE(Transistor*, double, double*, double*, int);
            void meting_IC_VBE(Transistor*, double, double*, double *, int);
            """
        )

        self.TransistorSO = self.ffi.dlopen(os.path.abspath("TransistorMetingen.so"))
        self.Transistor = self.ffi.new("Transistor *")
        self.defect = self.TransistorSO.locate_base(self.Transistor)
        self.layout = 3*[None]
        self.type = None
        self.structuur = None

        if(not self.defect):
            self.TransistorSO.locate_collector_emitter(self.Transistor)
            self.structuur = self.ffi.string(self.Transistor.structuur).decode('UTF-8')
            self.type = self.ffi.string(self.Transistor.type).decode('UTF-8')

            if(self.structuur == "BJT"):
                # print("Basis: ")
                # print(Transistor.basisGateChannel)
                # print("Collector: ")
                # print(Transistor.collectorDrainChannel)
                # print("Emitter: ")
                # print(Transistor.emitterSourceChannel)
                self.layout[self.Transistor.basisGateChannel] = "B"
                self.layout[self.Transistor.collectorDrainChannel] = "C"
                self.layout[self.Transistor.emitterSourceChannel] = "E"
            else:
                # print("Gate: ")
                # print(Transistor.basisGateChannel)
                # print("Drain: ")
                # print(Transistor.collectorDrainChannel)
                # print("Source: ")
                # print(Transistor.emitterSourceChannel)
                self.layout[Transistor.basisGateChannel] = "G"
                self.layout[Transistor.collectorDrainChannel] = "D"
                self.layout[Transistor.emitterSourceChannel] = "S"


    def isDefect(self):
        return self.defect

    def getPinLayout(self):
        return self.layout

    def getType(self):
        return self.type

    def getStructuur(self):
        return self.structuur

    def meting_Beta_IC(self, data_IC, data_Beta, dataLen):
        C_IC = self.ffi.cast("double *", (data_IC).ctypes.data)
        C_Beta = self.ffi.cast("double *", (data_Beta).ctypes.data)

        self.TransistorSO.meting_Beta_IC(self.Transistor, C_IC, C_Beta, dataLen)

    def meting_IC_VCE(self, IB, data_IC, data_VCE, dataLen):
        C_IC = self.ffi.cast("double *", (data_IC).ctypes.data)
        C_VCE = self.ffi.cast("double *", (data_VCE).ctypes.data)

        self.TransistorSO.meting_IC_VCE(self.Transistor, IB, C_IC, C_VCE, dataLen)

    def meting_IC_VBE(self, VCB, data_IC, data_VBE, dataLen):
        C_IC = self.ffi.cast("double *", (data_IC).ctypes.data)
        C_VBE = self.ffi.cast("double *", (data_VBE).ctypes.data)

        self.TransistorSO.meting_IC_VBE(self.Transistor, VCB, C_IC, C_VBE, dataLen)
