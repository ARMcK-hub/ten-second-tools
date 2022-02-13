from dataclasses import dataclass
from typing import Dict, List


@dataclass
class User:
    repoHost: str
    accountName: str
    yourName: str
    linkedInAccount: str
    email: str
    portrait: str


@dataclass
class Repository:
    name: str
    title: str
    link: str
    image: str
    description: str
    body: str
    features: List[str]
    technologies: List[Dict[str, str]]
    acknowledgements: List[Dict[str, str]]


@dataclass
class Config:
    user: User
    repositories: List[Repository]
