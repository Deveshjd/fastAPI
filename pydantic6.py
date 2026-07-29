# Serialization

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

temp1 = patient1.model_dump()
temp2 = patient1.model_dump(include='name') # similarly we have another parameters like exclude, exclude_unset
print(temp1)
print(temp2)
print(type(temp1))