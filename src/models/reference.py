from framework.model import BaseModel

class BaseRankModel(BaseModel):
    name: str
    description: str
    value: int
    example: str


class Severity(BaseRankModel, table=True):
    pass


class Likelihood(BaseRankModel, table=True):
    pass


class Detection(BaseRankModel, table=True):
    pass


class Impact(BaseRankModel, table=True):
    pass
