# Field Validator

from pydantic import BaseModel, EmailStr,field_validator

class Patient(BaseModel):
    name : str
    age : int
    emailID : str

    @field_validator('emailID')
    @classmethod
    def domain_validator(cls, value):
        valid_domains = ['gmail.com', 'yahoo.com']
        #abc@gmail.com or abc@yahoo.com ---> valid
        #adc@xyz.com ---> invalid

        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value

    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        if value[0] >= 'A' and value[0] <= 'Z':
            return value
        else:
            raise ValueError('First letter of name must be capital')

def InsertPatientData(patient : Patient):
    print(patient.name)
    print(patient.age)
    print("Data inserted successfully")

patient1_info = {'name' : 'Akshita', 'age' : 22, 'emailID' : 'akshita@gmail.com'} # valid data
# patient2_info = {'name' : 'Lakshita', 'age' : 23, 'emailID' : 'lakshita@xyz.com'} # invalid domain in email

patient1 = Patient(**patient1_info)
# patient2 = Patient(**patient2_info)

InsertPatientData(patient1)
# InsertPatientData(patient2)