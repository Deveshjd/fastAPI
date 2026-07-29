# Computed field

from pydantic import BaseModel, Field, computed_field

class Patient(BaseModel):
    name : str
    age : int = Field(gt = 0)
    height : float #mtr
    weight : float #kg

    @computed_field
    @property
    def bmi_calculator(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

def InsertPatientData(patient : Patient):
    print(patient.name)
    print(f"Height : {patient.height}mtr, Weight : {patient.weight}kg")
    print(f" BMI : {patient.bmi_calculator}")

patient1_info = {'name' : 'Akshita', 'age' : 30, 'height' : 1.8, 'weight' : 60.4}

patient1 = Patient(**patient1_info)
InsertPatientData(patient1)