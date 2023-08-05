import uuid

class Utils():
    
    @classmethod
    def get_guid(self):
        Guid = uuid.uuid4().hex
        return Guid