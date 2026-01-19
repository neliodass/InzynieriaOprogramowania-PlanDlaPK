from dataclasses import dataclass,field
from typing import List, Optional

@dataclass(frozen=True)
class Room:
    id: int
    name: str
    capacity: int

@dataclass(frozen=True)
class Teacher:
    id: int
    name: str
    unavailable_time_slots_ids: List[int] = field(default_factory=list)

@dataclass(frozen=True)
class Group:
    id: int
    name: str
    parent_group_id: Optional[int] = None

@dataclass
class CourseClass:
    id:int
    name:str
    group_id:int
    subject:str
    teacher_id:int
    student_count:int


@dataclass
class TimeSlot:
    id: int
    day: int
    hour_index:int
    label:str