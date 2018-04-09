from scipy.interpolate import interp2d
from math import sqrt
import csv
from heapq import nsmallest


class InterpretMapValues(object):

    def __init__(self, fault_line_file,fault_elevation_file,res_file,height_file,map_type):

        self.fault_line_file = fault_line_file
        self.fault_elevation_file = fault_elevation_file
        self.res_file = res_file
        self.height_file = height_file

        if map_type == 'open':
            self.num_repeats = 0
        elif map_type == 'closed':
            self.num_repeats = 1

        self.file_name = str()
        self.new_value = float()

    @staticmethod
    def distance_between_pts(new_e, new_n, easting, northing):
        distance = list()

        for idx,check_e in enumerate(easting):
            east_d = new_e - check_e
            north_d = new_n - northing[idx]
            d = sqrt(east_d**2 + north_d**2)
            distance.append(d)
        return distance

    @staticmethod
    def read_csv_file(filename):
        easting = list()
        northing = list()
        value = list()

        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                easting.append(float(row[0]))
                northing.append(float(row[1]))
                value.append(float(row[2]))

        return easting, northing, value

    def check_fault_side(self, new_e, new_n, height=False):
        easting, northing, value = self.read_csv_file(self.fault_line_file)
        distance = self.distance_between_pts(new_e, new_n, easting, northing)

        f_eidx = distance.index(min(distance))

        f_e = easting[f_eidx]
        if height:
            self.file_name = self.height_file
        else:
            if (f_e - new_e) < 0:
                self.file_name = self.res_file
            elif (f_e - new_e) > 0:
                self.file_name = self.fault_elevation_file
            else:
                self.file_name = self.fault_elevation_file

    def check_side(self, north, east, new_north, new_east):
        side = str()
        if north > new_north:
            side = side + 'top'
        if north < new_north:
            side = side + 'bottom'
        if east > new_east:
            side = side + 'right'
        if east < new_east:
            side = side + 'left'
        return side

    def find_new_pts(self, new_e, new_n):

        filename = self.file_name
        easting, northing, value = self.read_csv_file(filename)

        distance = self.distance_between_pts(new_e, new_n, easting, northing)

        chosen_values = list()
        chosen_easting = list()
        chosen_northing = list()
        smallest = nsmallest(len(distance), enumerate(distance), key=lambda x: x[1])

        for val_idx in smallest:
            i = val_idx[0]
            if len(chosen_northing) == 0:
                chosen_values.append(value[i])
                chosen_easting.append(easting[i])
                chosen_northing.append(northing[i])
            elif len(chosen_northing) < 4:
                if chosen_values.count(value[i]) > (self.num_repeats):
                    pass
                else:
                    chosen_values.append(value[i])
                    chosen_easting.append(easting[i])
                    chosen_northing.append(northing[i])
            else:
                break

        interp_func = interp2d(chosen_easting, chosen_northing, chosen_values)

        new_value = interp_func(new_e,new_n)

        if new_value < min(chosen_values):
            self.new_value = min(chosen_values)
        elif new_value > max(chosen_values):
            self.new_value = max(chosen_values)
        else:
            self.new_value = new_value