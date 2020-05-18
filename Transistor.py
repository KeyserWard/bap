import os
from cffi import FFI
ffi = FFI()

print(os.getcwd() + "/TransistorBreadboard.png")

ffi.cdef(
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

TransistorSO = ffi.dlopen(os.path.abspath("TransistorMetingen.so"))
Transistor = ffi.new("Transistor *")

def getPinLayout():
    global Transistor
    global TransistorSO

    layout = 3*[None]

    defect = TransistorSO.locate_base(Transistor)
    if(defect):
        return layout

    TransistorSO.locate_collector_emitter(Transistor)
    print(ffi.string(Transistor.structuur).decode('UTF-8'))

    if(ffi.string(Transistor.structuur).decode('UTF-8') == "BJT"):
        print("Basis: ")
        print(Transistor.basisGateChannel)
        print("Collector: ")
        print(Transistor.collectorDrainChannel)
        print("Emitter: ")
        print(Transistor.emitterSourceChannel)
        layout[Transistor.basisGateChannel] = "B"
        layout[Transistor.collectorDrainChannel] = "C"
        layout[Transistor.emitterSourceChannel] = "E"
    else:
        layout[Transistor.basisGateChannel] = "G"
        layout[Transistor.collectorDrainChannel] = "D"
        layout[Transistor.emitterSourceChannel] = "S"

    return layout


def getType():
    global Transistor
    return ffi.string(Transistor.type).decode('UTF-8')

def getStructuur():
    global Transistor
    return ffi.string(Transistor.structuur).decode('UTF-8')

def meting_Beta_IC(data_IC, data_Beta, dataLen):
    global Transistor
    global TransistorSO

    C_IC = ffi.cast("double *", (data_IC).ctypes.data)
    C_Beta = ffi.cast("double *", (data_Beta).ctypes.data)

    TransistorSO.meting_Beta_IC(Transistor, C_IC, C_Beta, dataLen)


def meting_IC_VCE(IB, data_IC, data_VCE, dataLen):
    global Transistor
    global TransistorSO
    
    C_IC = ffi.cast("double *", (data_IC).ctypes.data)
    C_VCE = ffi.cast("double *", (data_VCE).ctypes.data)

    TransistorSO.meting_IC_VCE(Transistor, IB, C_IC, C_VCE, dataLen)


def meting_IC_VBE(VCB, data_IC, data_VBE, dataLen):
    global Transistor
    global TransistorSO

    C_IC = ffi.cast("double *", (data_IC).ctypes.data)
    C_VBE = ffi.cast("double *", (data_VBE).ctypes.data)

    TransistorSO.meting_IC_VBE(Transistor, VCB, C_IC, C_VBE, dataLen)
    