from pydantic import BaseModel

class Geo(BaseModel):
    lat: str
    lng: str

class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo

class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str

class UserData(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company
