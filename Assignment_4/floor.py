FLOOR_MAPPING = {
    'w1': ['w2', 'o1', 'o2', 'o4', 'o5'],
    'w2': ['w1', 'w3', 'o2', 'o3'],
    'w3': ['w2', 'w4', 'o3'],
    'w4': ['w3', 'o4', 'o5', 'o6'],
    'o1': ['w1', 'o6'],
    'o2': ['w1', 'w2', 'o3', 'o4'],
    'o3': ['w2', 'w3', 'o2', 'o4'],
    'o4': ['w1', 'w4', 'o2', 'o3', 'o5' ],
    'o5': ['w1', 'w4', 'o4', 'o6'],
    'o6': ['w4', 'o1', 'o5']
}

class Floor:
    def __init__(self, locations):
        self.locations = locations

class Location:
    def __init__(self, loc_type, adjacents):
        self.loc_type = loc_type
