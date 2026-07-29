# run the following command to start the port: uvicorn main:app --reload

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description='ID of Patient')]
    name : Annotated[str, Field(..., description='Name of the Patient')]
    city : Annotated[str, Field(..., description='City of Patient')]
    age : Annotated[int, Field(..., gt = 0, lt = 120, description='Age of Patient')]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of Patient')]
    height : Annotated[int, Field(..., gt = 0,  description='Height of Patient in meters')]
    weight : Annotated[int, Field(..., gt = 0,  description='Weight of patient')]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

class updatePatient(BaseModel):
    name : Annotated[Optional[str], Field(default = None)]
    city : Annotated[Optional[str], Field(default = None)]
    age : Annotated[Optional[int], Field(default = None)]
    gender : Annotated[Optional[str], Field(default = None)]
    height : Annotated[Optional[int], Field(default = None)]
    weight : Annotated[Optional[int], Field(default = None)]


def read_json():
    with open("patient.json", "r") as file:
        data = json.load(file)

    return data

def save_data(data):
    with open("patient.json", "w") as file:
        json.dump(data, file)

@app.get("/")
def read():
    return {"message" : "Heyyy Brooo"}

@app.get("/about")
def read_about():
    return {"message" : "Welcome to the about page!"}

@app.get("/view")
def view():
    data = read_json()
    return data

@app.get("/patient/{id}")
def get_patient(id:str = Path(..., description = 'ID of patient', example = 'POO1')):
    data = read_json()
    if id in data:
        return {id : data[id]}
    raise HTTPException(status_code= 404, detail= 'Patient not found')

@app.get('/sort')
def sort_patient(sort_by : str = Query(..., description='Sort by name, city or age'),
           order : str = Query('asc', description='order by asc or desc')):

    data = read_json()

    if sort_by not in ['city', 'name', 'age']:
        raise HTTPException(status_code=404, detail='invalid field')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail='choose either asc or desc')
    
    order_by = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by), reverse=order_by)
    return sorted_data


# POST request
@app.post('/create')
def create_data(patient : Patient):
    # Load exixting data
    data = read_json()

    # check if the patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient alredy exist')

    # if it's a new patient then create a new one
    data[patient.id] = patient.model_dump(exclude={'id'})

    # save to json
    save_data(data)

    # return json response for success
    return JSONResponse(status_code=200, content={'message' : 'Paitient created successfully'})

# PUT request
@app.put('/edit/{id}')
def updateData(patient_id : str, patient_info : updatePatient):
    data = read_json()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='patient not found')
    
    existing_patient_data = data[patient_id]

    updated_patient_info = patient_info.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_data[key] = value

    #existing_patient_data -> pydantic object -> patient class object

    existing_patient_data['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_data)
    existing_patient_data = patient_pydantic_object.model_dump(exclude=['id'])

    #add this dict to data
    data[patient_id] = existing_patient_data

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content='patient updated')

@app.delete('/delete/{patient_id}')
def deletePatient(patient_id : str):
    data = read_json()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)
    return JSONResponse(status_code=200, content='patient data deleted')