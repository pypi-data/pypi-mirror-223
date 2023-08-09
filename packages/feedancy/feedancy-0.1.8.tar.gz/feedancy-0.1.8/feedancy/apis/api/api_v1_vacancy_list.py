from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from feedancy.lib.base import BaseApi
from feedancy.lib.request import ApiRequest
from feedancy.lib import json
class Contact(BaseModel):
    data: str 
    id: int 
    name: typing.Optional[typing.Union[str, None]]  = None
    type: str 

class VacancyContact(BaseModel):
    contact: typing.Union[Contact, None] 

class Salary(BaseModel):
    currency: str 
    id: int 
    max_value: typing.Optional[typing.Union[int, None]]  = None
    min_value: typing.Optional[typing.Union[int, None]]  = None

class Vacancy(BaseModel):
    city: str 
    company: typing.Union[str, None] 
    contacts: typing.Union[typing.List[VacancyContact], None] 
    contract_type: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None
    employment_format: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None
    experience: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None
    external_id: str 
    has_insurance: typing.Optional[typing.Union[bool, None]]  = None
    has_portfolio: typing.Optional[typing.Union[bool, None]]  = None
    has_test_task: typing.Optional[typing.Union[bool, None]]  = None
    id: int 
    is_relocation_required: typing.Optional[typing.Union[bool, None]]  = None
    link: str 
    name: str 
    publicated_at: typing.Optional[typing.Union[datetime.datetime, None]]  = None
    raw_description: typing.Optional[typing.Union[str, None]]  = None
    requirement: typing.Optional[typing.Union[str, None]]  = None
    responsibility: typing.Optional[typing.Union[str, None]]  = None
    salary: typing.Union[Salary, None] 
    source: str 
    test_task_link: typing.Optional[typing.Union[str, None]]  = None
    work_format: typing.Optional[typing.Union[typing.Union[str, str, str], None]]  = None

class PaginatedVacancyList(BaseModel):
    count: typing.Optional[int]  = None
    next: typing.Optional[typing.Union[str, None]]  = None
    previous: typing.Optional[typing.Union[str, None]]  = None
    results: typing.Optional[typing.List[Vacancy]]  = None

def make_request(self: BaseApi,


    activity_sphere: str = ...,

    company_size: str = ...,

    employment_format: str = ...,

    has_insurance: bool = ...,

    is_accredited: bool = ...,

    is_relocation_required: bool = ...,

    page: int = ...,

    search: str = ...,

    work_format: str = ...,

) -> PaginatedVacancyList:
    

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/api/v1/vacancy/".format(
            
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
                "activity_sphere": activity_sphere,
            
                "company_size": company_size,
            
                "employment_format": employment_format,
            
                "has_insurance": has_insurance,
            
                "is_accredited": is_accredited,
            
                "is_relocation_required": is_relocation_required,
            
                "page": page,
            
                "search": search,
            
                "work_format": work_format,
            
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "200": {
            
                "application/json": PaginatedVacancyList,
            
        },
    
    }, m)