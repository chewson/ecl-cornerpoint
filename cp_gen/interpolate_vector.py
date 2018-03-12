from scipy.interpolate import interp2d
from math import sqrt
import csv
from heapq import nsmallest


class InterpretMapValues(object):

    def __init__(self):

        self.fault_line_file = 'fault_line.csv'
        self.fault_elevation_file = 'fault_depth.csv'
        self.res_file = 'combined.csv'
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

    def check_fault_side(self, new_e, new_n):
        easting, northing, value = self.read_csv_file(self.fault_line_file)
        distance = self.distance_between_pts(new_e, new_n, easting, northing)

        f_eidx = distance.index(min(distance))

        f_e = easting[f_eidx]

        if (f_e - new_e) < 0:
            self.file_name = self.res_file
        elif (f_e - new_e) > 0:
            self.file_name = self.fault_elevation_file
        else:
            self.file_name = self.fault_elevation_file

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
                if chosen_values.count(value[i]) > 1:
                    pass
                else:
                    chosen_values.append(value[i])
                    chosen_easting.append(easting[i])
                    chosen_northing.append(northing[i])
            else:
                break

        interp_func = interp2d(chosen_easting, chosen_northing, chosen_values)

        self.new_value = interp_func(new_e,new_n)