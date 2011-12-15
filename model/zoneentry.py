
class ZoneEntry:
    
    # name, ipaddress, updateType
    def __init__(self, *args):
        if len(args) < 2 or len(args) > 3:
            return None
        if len(args) > 1:
            self.name = args[0]
            self.ip = args[1]
        if len(args) > 2:
            self.updateType = args[2]