from math import radians, cos, sqrt


class GenerateGridPoints(object):

    def __init__(self):

        self.dx = 80
        self.dy = 100
        self.nx = 75
        self.ny = 56
        self.x0 = 366046.90992691246
        self.y0 = 6249318.971364301
        self.theta_i = radians(33.3)
        self.theta_j = radians(56.7)
        self.grid_vector = list()

    def calc_i_new(self, x0, y0):
        x1 = (x0 + self.dx * cos(self.theta_i))

        y1 = y0 - sqrt(self.dx ** 2 - (x1 - x0) ** 2)

        return x1, y1

    def calc_j_new(self, x0, y0):
        x1 = (x0 - self.dy * cos(self.theta_j))

        y1 = y0 - sqrt(self.dy ** 2 - (x1 - x0) ** 2)

        return x1, y1

    def gen_grid_vector(self):
        y_vector = list()
        x0 = self.x0
        y0 = self.y0
        y_vector.append([x0, y0])

        for idx in range(self.ny):
            x0, y0 = self.calc_j_new(x0, y0)
            y_vector.append([x0, y0])

        for x0, y0 in y_vector:
            self.grid_vector.append([x0, y0])
            x1 = x0
            y1 = y0
            for idx in range(self.nx):
                x1, y1 = self.calc_i_new(x1, y1)
                self.grid_vector.append([x1, y1])
