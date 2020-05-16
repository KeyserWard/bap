from cffi import FFI
ffi = FFI()

ffi.cdef("""
        typedef struct {
            int basisGateChannel;
            int collectorDrainChannel;
            int emitterSourceChannel;
            char* type;		//pnp of npn
            char* structuur; //MOSFET of BJT
        } Transistor;

        bool locate_base(Transistor*);
        void locate_collector_emitter(Transistor*);
        """
    )

TransistorPin = ffi.dlopen("TransistorPinnen.so")

def getStructTransistor():
    global ffi
    
    Transistor = ffi.new("struct Transistor *")
    return Transistor

def getPinLayout(Transistor):
    global TransistorPin

    layout = []

    defect = TransistorPin.locate_base(Transistor)
    if(defect):
        return layout

    TransistorPin.locate_collector_emitter(Transistor)

    if(ffi.string(Transistor.structuur) == "BJT"):
        layout[Transistor.basisGateChannel] = "B"
        layout[Transistor.collectorDrainChannel] = "C"
        layout[Transistor.emitterSourceChannel] = "E"
    else:
        layout[Transistor.basisGateChannel] = "G"
        layout[Transistor.collectorDrainChannel] = "D"
        layout[Transistor.emitterSourceChannel] = "S"

    return layout

def getType(Transistor):
    return Transistor.structuur + " " + Transistor.type
