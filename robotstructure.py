
class RSValue:
    # interface_settings = {'header_text':'','display_round':None,}
    def __init__(self, id, value=None, interface_settings=None):
        self.id = id
        self.value = value

        if interface_settings:
            self.interface_settings = {'header_text':'','display_round':None,}

    def update(self, nval):
        self.value = nval


class RoboStructure:
    def __init__(self, values=[]):
        self.values = values

    def update

