from framework.model import BaseDescriptorModel


class Failure(BaseDescriptorModel, table=True):
    pass


class Cause(BaseDescriptorModel, table=True):
    pass


class Effect(BaseDescriptorModel, table=True):
    pass
