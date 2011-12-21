
class ZoneEntry:
    
    # name, ipaddress, updateType
    def __init__(self, *args):
        if len(args) < 2 or len(args) > 4:
            return None
        if len(args) > 1:
            self.name = args[0]
            self.host = args[1]
        if len(args) > 2:
            self.updateType = args[2]
        if len(args) > 3:
            self.old_value = args[3]