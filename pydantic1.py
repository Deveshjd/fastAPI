# pydantic is used for data validation

from pydantic import BaseModel, Field # Field is used for metadata and constraints
from typing import List, Dict, Optional, Annotated


# By default all the fields in the pydantic class are mandatory... if you pass an argument in the function without all fields then it shows error so is you want to make any field optional then we just add a 'optional[data type]' in that field... as provided in the hobbies
class Patient(BaseModel): #passing BaseModel --> base class for pydantic model
    name : Annotated[str, Field(max_length=30, title='Name of the patient', description='Give the name of the patient in less than 30 characters', examples=['Devesh', 'Aditi'])]
    age : int = Field(gt = 0)
    hobbies : Optional[List[str]] = None # none here indicates default value for hobbies
    contact_details : Dict[str, str]
#Note : we used 'List' instead of 'list' ---> 'list' ensures that the hobbies is list but 'List[str]' ensures that the hobbies is list and also it contains string elements... inshort it is used for two level validation
#Note : we used 'Dict' instead of 'dict' ---> 'dict' ensures that the contact_details is dict but 'Dict[str, str]' ensures that the contact_details is dict and also it contains sring key & string value pair elements... inshort it is used for two level validation


patient1_info = {'name' : 'Akshita', 'age' : 2, 'hobbies' : ['cricket', 'chess'], 'contact_details' : {'phone' : '909004349', 'email' : 'aksh@xyz'}} # Valid Demo patient data
# patient2_info = {'name' : 'Akshita', 'age' : 'thirty', 'hobbies' : ['cricket', 'chess'], 'contact_details' : {'phone' : '909004349', 'email' : 'aksh@xyz'}} # Invalid Demo patient data because 'age' is string istead of int

def InsertPatientData(patient : Patient):
    print(patient.name)
    print(patient.age)
    print("Data inserted successfully")

patient1 = Patient(**patient1_info)
# patient2 = Patient(**patient2_info)

InsertPatientData(patient1)
# InsertPatientData(patient2) ----> this will show type error because it's having invalid type of data (age is str instead of int)