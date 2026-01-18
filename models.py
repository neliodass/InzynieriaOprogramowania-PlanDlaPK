from dataclasses import dataclass,field
from typing import List

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
    hour_index:int # 0 = 7:30-9:00, 1 = 9:15-10:45, ...
    label:str