import random
import time

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
    def __init__(self, location_names):
        self.locations = []
        for loc_name in location_names:
            self.locations.append(Location(loc_name))
        self.name_to_loc_dict = {}
        self.set_adjacents(FLOOR_MAPPING)


    def set_adjacents(self, mapping):
        for loc in self.locations:
            self.name_to_loc_dict[loc.name] = loc

        for source_name, target_names in mapping.items():
            source = self.name_to_loc_dict[source_name]
            for target_name in target_names:
                source.adjacent_locs.append(self.name_to_loc_dict[target_name])

    def all_floors_adjusted(self):
        for loc in self.locations:
            if not loc.temp_changed or not loc.hum_changed:
                return False
        return True

    def set_values(self, encoding):
        for i in range(len(encoding)):
            encoding_val = encoding[i]
            loc = self.locations[i]
            loc.encoding = encoding_val
            if encoding_val == 0:
                loc.temp_changed = True
            elif encoding_val == 1:
                loc.hum_changed = True
            elif encoding_val == 2:
                loc.passed_through
            else:
                print('error: encoding is incorrect')

    def check_constraints(self):
        for loc in self.locations:
            for adj in loc.adjacent_locs:
                if loc.encoding == adj.encoding:
                    return False
                elif loc.encoding == -1:
                    return False
        return True

    def __str__(self):
        locs = self.locations
        encodings = [l.encoding for l in locs]
        for i in range(len(encodings)):
            if encodings[i] != -1:
                encodings[i] = ' ' + str(encodings[i])


        s = "+-------------------+---+\n" + \
            "|        {}         |{} |\n".format(encodings[0], encodings[4]) + \
            "+-------+---+-------+---+\n" + \
            "|       |{} |   |   |   |\n".format(encodings[5]) + \
            "|  {}   +---+{} |{} |{} |\n".format(encodings[1], encodings[7], encodings[8], encodings[9]) + \
            "|       |{} |   |   |   |\n".format(encodings[6]) + \
            "+-------+---+---+---+---+\n" + \
            "|    {}     |    {}     |\n".format(encodings[2], encodings[3]) + \
            "+-----------+-----------+\n"
        return(s)







class Location:
    ''' Either a warehouse or an office.
        name is something like o1 or w1
        adjacent_locs is a list that stores actual other location object instances'''
    def __init__(self, name):
        self.name = name
        if self.name[0] == 'w':
            self.loc_type = 'warehouse'
        else:
            self.loc_type = 'office'
        self.adjacent_locs = []
        self.temp_changed = False
        self.hum_changed = False
        self.passed_through = False
        self.encoding = -1

    def is_complete(self):
        if self.temp_changed and self.hum_changed:
            return True
        else:
            return False


def brute_force():
    location_names = ['w1', 'w2', 'w3', 'w4', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6']
    solutions = []
    floor = Floor(location_names)
    action_encoding = [0] * 10
    floor.set_values(action_encoding)

    # for performance metric
    t0 = time.time()

    if floor.check_constraints():
        solutions.append(floor)
#         return floor
    count = 1
    while True:
        count += 1
        floor = Floor(location_names)
        ternery_increment(action_encoding)
        floor.set_values(action_encoding)
        if floor.check_constraints():
            solutions.append(floor)
            print('Brute force: solution found at count {}'.format(count))
        if sum(action_encoding) == 20:
            break

    t1 = time.time()
    total_time = t1 - t0
    print('Brute force: checked {} possibilities'.format(count))
    print('Brute force: took {} seconds'.format(total_time))
    return solutions

def ternery_increment(ternery_arr):
    if sum(ternery_arr) == 20:
        print('max reached')
        return
    cur_idx = 0
    while True:
        if ternery_arr[cur_idx] == 2:
            ternery_arr[cur_idx] = 0
            cur_idx += 1
        elif ternery_arr[cur_idx] == 1:
            ternery_arr[cur_idx] += 1
            break
        elif ternery_arr[cur_idx] == 0:
            ternery_arr[cur_idx] += 1
            break
        else:
            print('error: should not be here')
            break

def minimum_conflicts():
    location_names = ['w1', 'w2', 'w3', 'w4', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6']
    floor = Floor(location_names)

    # for performance metrics
    count = 0
    t0 = time.time()
    while True:
        for loc in floor.locations:
            count += 1
            adjacent_encodings = [l.encoding for l in loc.adjacent_locs]
            temp_cons_num = len([e for e in adjacent_encodings if e == 0])
            hum_cons_num = len([e for e in adjacent_encodings if e == 1])
            pass_cons_num = len([e for e in adjacent_encodings if e == 2])

            encoding_counts = [temp_cons_num, hum_cons_num, pass_cons_num]

            mins_idx = [i for i in range(len(encoding_counts)) if encoding_counts[i] == min(encoding_counts)]
            num_mins = len(mins_idx)


            if num_mins == 1:
                action = encoding_counts.index(min(encoding_counts))
            else:
                action = mins_idx[random.randint(0, len(mins_idx) - 1)]

            if action == loc.encoding:
                if encoding_counts[loc.encoding] != 0:
                    encoding_counts[loc.encoding] = 999 # :P
                    action = encoding_counts.index(min(encoding_counts))

            loc.encoding = action
            if loc.encoding > 2:
                print('Error: somehow there are more than 3 elements in the encoding_counts list')
            if floor.check_constraints():
                t1 = time.time()
                total_time = t1 - t0
                return floor, count, total_time



def main():
    print('Running brute force . . .')
    answers = brute_force()

    print('Brute force answers:')
    for answer in answers:
        print(answer)

    print('\n\n')


    print('Running minimum conflicts optimized . . .')
    avg_count = 0
    avg_time = 0
    for i in range(10000):
        aMinConflict = minimum_conflicts()
        avg_count += aMinConflict[1]
        avg_time += aMinConflict[2]
    print('Answer from last minimum conflict run:')
    print(aMinConflict[0])
    print('Average number of location-action assignments: {}'.format(avg_count / 10000))
    print('Average time to find solution: {}'.format(avg_time / 10000))

if __name__ == '__main__':
    main()
