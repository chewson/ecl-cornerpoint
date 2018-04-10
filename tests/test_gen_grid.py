import unittest
import os
from cp_gen import GenerateGridPoints, InterpretMapValues, GenerateGridFiles


class TestCpGen(unittest.TestCase):

    def test_gridpoint_gen(self):
        current_dir = os.path.dirname(__file__)
        easting = 367947.315968816
        northing = 6246378.058582101
        fault_line_file = os.path.join(current_dir,'test_data','fault_line.csv')
        fault_elevation_file = os.path.join(current_dir, 'test_data', 'fault_depth.csv')
        res_file = os.path.join(current_dir, 'test_data', 'res_depths.csv')
        height_file = os.path.join(current_dir, 'test_data', 'height.csv')
        grid_interpret = InterpretMapValues(fault_line_file,fault_elevation_file,res_file,height_file,'open')
        grid_interpret.check_fault_side(easting, northing)
        grid_interpret.find_new_pts(easting, northing)

        #assert (int(grid_interpret.new_value) == 424)

        easting_2 = 365638.3992886146
        northing_2 = 6248144.503279194
        grid_interpret.check_fault_side(easting_2, northing_2)
        grid_interpret.find_new_pts(easting_2, northing_2)

        #assert (int(grid_interpret.new_value) == 462)

        easting_3 = 367268.3422021029
        northing_3 = 6247105.576070392

        grid_interpret.check_fault_side(easting_3, northing_3, height=True)
        grid_interpret.find_new_pts(easting_3, northing_3)
        #assert (int(grid_interpret.new_value) == 4)

    def test_interpret_map_values(self):
        dx = 80
        dy = 100
        nx = 75
        ny = 56
        nz = 6
        x0 = 366046.90992691246
        y0 = 6249318.971364301
        theta = 56.7
        grid_points = GenerateGridPoints(dx, dy, nx, ny, nz, x0, y0, theta)

        grid_points.gen_grid_vector()

        #assert (len(grid_points.grid_vector)==((nx+1)*(ny+1)))

    def test_generate_coord(self):
        current_dir = os.path.dirname(__file__)
        fault_line_file = os.path.join(current_dir, 'test_data', 'fault_line.csv')
        fault_elevation_file = os.path.join(current_dir, 'test_data', 'fault_depth.csv')
        res_file = os.path.join(current_dir, 'test_data', 'res_depths.csv')
        height_file = os.path.join(current_dir, 'test_data', 'height.csv')

        east_bound = 366374.02
        north_bound = 6249077.40

        dx = 80
        dy = 100
        nx = 75
        ny = 56
        nz = 6
        x0 = 366046.90992691246
        y0 = 6249318.971364301
        theta = 56.7

        grid_interpret = InterpretMapValues(fault_line_file, fault_elevation_file, res_file, height_file, 'open')

        grid_points = GenerateGridPoints(dx, dy, nx, ny, nz, x0, y0, theta)

        grid_points.gen_grid_vector()

        coord = GenerateGridFiles(grid_points, grid_interpret, east_bound, north_bound)

        coord.generate_coord_vector()
        coord.print_coord_vector()

        coord.generate_zcorn_vector()
        coord.print_zcorn_vector()

        coord.generate_actnum_vector()
        coord.print_actnum_vector()


if __name__ == '__main__':
    unittest.main()