import dataclasses
from json import JSONEncoder, JSONDecoder


class EnhancedJSONEncoder(JSONEncoder):

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
