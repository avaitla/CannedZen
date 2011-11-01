from Utils.Base_Utilities import default_app_path
from Engines import EngineRegistrar
import os.path.exists as exists

class InteractsRegistrarObject(object):
    def __init__(self):
        self.custom_pairs = dict()
    
    # For the Time Being We will only permit one interaction
    # type between two deployment engines, we may remove this restriction later
    def registerInteract(self, interaction, engine1_as_str, engine2_as_str):
        # Just in case a User sends in the actual engine object
        # We will try our best to cast them into Strings
        engine1_as_str = str(engine1_as_str)
        engine2_as_str = str(engine2_as_str)
        
        assert (engine1, engine2) not in self.custom_pairs, "Interaction between Engines %s and %s Exists" % (engine1_as_str, engine2_as_str)
        self.custom_pairs[(engine1, engine2)] = self.custom_pairs[(engine1, engine2)] = interaction

    def getInteraction(self, engine1_as_str, engine2_as_str):
        engine1_as_str = str(engine1_as_str)
        engine2_as_str = str(engine2_as_str)

        return self.custom_pairs.get((engine1_as_str, engine2_as_str), None)

InteractRegistrar = InteractsRegistrarObject()



def registerInteract(cls):
    InteractRegistrar.registerInteract(cls, cls.engine1name, cls.engine2name)
    return cls

class RegisterEngine(type):
    def __init__(cls, name, bases, dct):
        obj = super(RegisterEngine, cls).__init__(name, bases, dct)
        if(name != "BaseEngine"): registerEngine(cls)
        return obj

class RegisterInteract(type):
    def __init__(cls, name, bases, dct):
        obj = super(RegisterInteract, cls).__init__(name, bases, dct)
        if(name != "BaseInteract"): registerInteract(cls)
        return obj

# In general when inheriting this class use the 
# following naming convention: Apache_ModWsgi(BaseInteract):
# where the first name is engine1, and the second name is engine2.
# I would recommend that we choose engine1 and engine2 alphabetically.
class BaseInteract(object):
    __metaclass__ = RegisterInteract

    # Authors will Need to Fill in these details
    engine1name = ""
    engine2name = ""

    def __init__(engine1path, engine2path):
        assert engine1name != "", "engine1name is not specified"
        assert engine2name != "", "engine2name is not specified"
        self.engine1path = engine1path
        self.engine2path = engine2path
        assert(exists(self.engine1path)), "engineone path does not exist"
        assert(exists(self.engine2path)), "enginetwo path does not exist"

    def install_interaction(self):
        raise NotImplementedError

    def uninstall_interaction(self):
        raise NotImplementedError
