from . import XiaoduDevice

class XiaoduSocket(XiaoduDevice):

    def __init__(self, entity_id) -> None:
        super().__init__(entity_id)