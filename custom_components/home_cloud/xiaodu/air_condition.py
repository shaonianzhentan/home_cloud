from . import XiaoduDevice

class XiaoduAirCondition(XiaoduDevice):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)