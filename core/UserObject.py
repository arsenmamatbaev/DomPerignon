from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    name: str
    username: str


@dataclass
class DataUser(User):
    updated_at: str
    register_date: str

