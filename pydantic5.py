# Nested model
# Better organization of related data (eg. vitals, address, insurance)
# Reusability : use vitals in multiple models (eg. patient, medical record)
# Readability : Easier for developers or API consumers to understand
# Validation : nested models are validated automatically ..no extra work needed
from pydantic import BaseModel, Field

class Address(BaseModel):
    city : str
    state : str
    pincode : str = Field(max_length=6)

class Patient(BaseModel):
    name : str
    age : int = Field(gt = 0)
    address : Address

address_dict = {'city' : 'jaipur', 'state' : 'Rajasthan', 'pincode' : '303030'}
address1 = Address(**address_dict)

patient1_info = {'name' : 'Zoobie', 'age' : '18', 'address' : address1}
patient1 = Patient(**patient1_info)

print(patient1)
print(patient1.address.city)