from typing import Type, TypeVar
from dataclasses import  fields

T = TypeVar('T')

def dict_to_dataclass(d: dict, cls: Type[T]) -> T:
    '''
    Helper function for mapping dictionaries to dataclasses
    :param d:
    :param cls:
    :return: T -> dataclass mapped from dictionary
    '''
    allowed = {f.name for f in fields(cls)}
    filtered = {k: v for k, v in d.items() if k in allowed}
    return cls(**filtered)

def dataclass_to_dict(obj: T) -> dict:
    '''
    Helper function for mapping dataclasses to dictionaries
    :param obj: dataclass instance
    :return: dict -> dictionary mapped from dataclass
    '''
    return {f.name: getattr(obj, f.name) for f in fields(obj) if getattr(obj, f.name) is not None}