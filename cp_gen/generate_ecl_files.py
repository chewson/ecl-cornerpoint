

class GenerateGridFiles(object):

    def __init__(self, grid_vector, grid_interpolate, east_bound, north_bound):

        self.grid_vector = grid_vector
        self.grid_interpolate = grid_interpolate

        self.nx = self.grid_vector.nx
        self.ny = self.grid_vector.ny
        self.nz = self.grid_vector.nz

        self.coord_vector = list()
        self.zcorn_vector = list()
        self.delta_z = list()

        self.coord_file = 'COORD.in'
        self.zcorn_file = 'ZCORN.in'
        self.actnum_file = 'ACTNUM.in'

        self.east_bound = east_bound
        self.north_bound = north_bound

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
                self.delta_z.append(h/self.ny)
                self.coord_vector.append([x1,y1,z1,x2,y2,z2])

    def print_coord_vector(self):

        header = 'COORD \n'

        f = open(self.coord_file, 'w')

        f.writelines(header)

        for rows in self.coord_vector:
            for vals in rows:
                f.write(str(vals) + ' ')

            f.write('\n')

        f.write('/')
        f.close()

    def generate_zcorn_vector(self):

        if len(self.delta_z) == 0:
            self.generate_coord_vector()

        for k in range(self.nz):

            # Top Surface
            for j in range(self.ny + 1):
                tmp_vector = list()
                for i in range(self.nx + 1):
                    idx = (self.nx*j) + i
                    if i < (self.nx):
                        z1 = self.coord_vector[idx][2] + (k * self.delta_z[idx])
                        z2 = self.coord_vector[idx+1][2] + (k * self.delta_z[idx+1])
                        tmp_vector.append(z1)
                        tmp_vector.append(z2)

                self.zcorn_vector.append(tmp_vector)
                if j == 0 or j == self.ny:
                    pass
                else:
                    self.zcorn_vector.append(tmp_vector)

            # Bottom Surface
            for j in range(self.ny + 1):
                tmp_vector = list()
                for i in range(self.nx + 1):
                    idx = (self.nx * j) + i
                    if i < (self.nx):
                        z1 = self.coord_vector[idx][2] + ((k + 1) * self.delta_z[idx])
                        z2 = self.coord_vector[idx + 1][2] + ((k + 1) * self.delta_z[idx + 1])
                        tmp_vector.append(z1)
                        tmp_vector.append(z2)

                self.zcorn_vector.append(tmp_vector)
                if j == 0 or j == self.ny:
                    pass
                else:
                    self.zcorn_vector.append(tmp_vector)

    def print_zcorn_vector(self):

        header = 'ZCORN \n'

        f = open(self.zcorn_file, 'w')

        f.writelines(header)

        row_counter = 0

        for rows in self.zcorn_vector:
            for vals in rows:
                f.write(str(vals) + ' ')
            f.write('\n')
            row_counter += 1

            if row_counter == (2*self.ny):
                f.write('\n')
                row_counter = 0

        f.write('/')
        f.close()

    def generate_actnum_vector(self):

        self.actnum = list()

        for k in range(self.nz):
            for j in range(self.ny):
                for i in range(self.nx):
                    idx = (self.nx * j) + i
                    coordinates = self.grid_vector.grid_vector[idx]

                    easting = coordinates[0]
                    northing = coordinates[1]

                    if easting > self.east_bound:
                        self.actnum.append(1)
                    else:
                        self.actnum.append(0)

    def print_actnum_vector(self):

        header = 'ACTNUM \n'

        f = open(self.actnum_file, 'w')

        f.writelines(header)

        row_counter = 0

        for vals in self.actnum:
            f.write(str(vals) + ' ')
            f.write('\n')
            row_counter += 1

            if row_counter == (self.nx):
                f.write('\n')
                row_counter = 0

        f.write('\n')
        f.write('/')
        f.close()
