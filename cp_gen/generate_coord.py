

class GenerateCOORD(object):

    def __init__(self, grid_vector, grid_interpolate):

        self.grid_vector = grid_vector
        self.grid_interpolate = grid_interpolate

        self.nx = self.grid_vector.nx
        self.ny = self.grid_vector.ny

        self.coord_vector = list()
        self.print_file = 'COORD.in'

    def calc_elevation(self, easting, northing, height=False):

        self.grid_interpolate.check_fault_side(easting, northing, height)
        self.grid_interpolate.find_new_pts(easting, northing)

        return float(self.grid_interpolate.new_value)

    def generate_coord_vector(self):

        for j in range(self.ny + 1):
            for i in range(self.nx + 1):
                idx = (self.nx*j) + i
                coordinates = self.grid_vector.grid_vector[idx]
                x1 = coordinates[0]
                y1 = coordinates[1]
                z1 = self.calc_elevation(x1,y1)

                x2 = x1
                y2 = y1
                h = self.calc_elevation(x1,y1, height=True)
                if h < 0:
                    h = 0
                z2 = z1 + h
                self.coord_vector.append([x1,y1,z1,x2,y2,z2])

    def print_coord_vector(self):

        header = 'COORD \n'

        f = open(self.print_file,'w')

        f.writelines(header)

        for rows in self.coord_vector:
            for vals in rows:
                f.write(str(vals) + ' ')

            f.write('\n')

        f.write('/')