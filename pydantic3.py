# Model validator

from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional, Dict, List

class Patient(BaseModel): #passing BaseModel --> base class for pydantic model
    name : Annotated[str, Field(max_length=30, title='Name of the patient', description='Give the name of the patient in less than 30 characters', examples=['Dobee', 'Aditi'])]
    age : int = Field(gt = 0)
    hobbies : Optional[List[str]] = None # none here indicates default value for hobbies
    contact_details : Dict[str, str]

    @model_validator(mode='after')
    def emergency_contact_validator(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('person older than 60 years must have an emergency contact number')
        else:
            return model

def InsertPatientData(patient : Patient):
    print(patient.name)
    print(patient.age)
    print("Data inserted successfully")


patient1_info = {'name' : 'Akshita', 'age' : 30, 'hobbies' : ['cricket', 'chess'], 'contact_details' : {'phone' : '909004349', 'email' : 'aksh@xyz'}}

patient1 = Patient(**patient1_info)
InsertPatientData(patient1)

