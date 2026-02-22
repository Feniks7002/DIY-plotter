import math

class SinusEngine:
    def __init__(self, image_data, workspace_dimensions, render_dimensions, sin_data, offset_data):
        self.work_width, self.work_height = workspace_dimensions
        self.render_width, self.render_height = render_dimensions
        self.img_data = image_data
        self.sin_amp, self.sin_freq, self.line_space = sin_data
        self.x_off, self.y_off = offset_data

    def calculate_amplitude_map(self):
        return (1.0 - self.img_data) * self.sin_amp

    def calculate_trajectory(self, amplitude_map, offset):
        trajectory = []
        x_offset, y_offset = offset
        for y_index in range(0, amplitude_map.shape[0], self.line_space):
            amplitudes = amplitude_map[y_index, :]
            line_points = []
            for x, amp in enumerate(amplitudes):
                y = y_offset + math.sin(x * self.sin_freq) * amp
                x += x_offset
                line_points.append([x, y])
            trajectory.append(line_points)
            y_offset += self.line_space
        return trajectory

    def run(self):
        amplitude = self.calculate_amplitude_map()

        raw_trajectory = self.calculate_trajectory(amplitude, (self.x_off, self.y_off))

        return raw_trajectory
    

class TrajectoryNormalizer:
    def __init__(self, raw_trajectory, workspace_dimensions):
        self.trajectory = raw_trajectory
        self.work_width, self.work_height = workspace_dimensions
    
    def normalize_trajectory_mm(self, raw_trajectory):
        pot_x = [point[0] for vector in raw_trajectory for point in vector]
        pot_y = [point[1] for vector in raw_trajectory for point in vector]
        
        max_x, min_x = max(pot_x), min(pot_x)
        max_y, min_y = max(pot_y), min(pot_y)
        
        source_width = max_x - min_x
        source_height = max_y - min_y
        
        target_w = self.work_width
        target_h = self.work_height

        if source_width != 0 and source_height != 0:
            scale_x = target_w / source_width
            scale_y = target_h / source_height     
            scale = min(scale_x, scale_y)
        else:
            return raw_trajectory

        scaled_width = source_width * scale
        scaled_height = source_height * scale

        margin_x = (self.work_width - scaled_width) / 2
        margin_y = (self.work_height - scaled_height) / 2

        xy_mm = []
        for line in raw_trajectory:
            single_line = []
            for x, y in line:
                x_shifted = x - min_x
                y_shifted = y - min_y
                x_scaled = x_shifted * scale + margin_x
                y_scaled = y_shifted * scale + margin_y
                single_line.append((x_scaled, y_scaled)) # x_mm, y_mm
            xy_mm.append(single_line)
        return xy_mm

    def trajectory_reduction(self, trajectory_mm):
        def find_max_distance(array):
            # Funkcja pomocnicza szukająca w danej lini maksymalnego odchylenia od prostej przeprowadzonej przez środek sinusoidy 
            x_start, y_start = array[0]
            x_end, y_end = array[-1]
            dx = x_end - x_start
            dy = y_end - y_start

            length = math.sqrt(dx**2 + dy**2)
            if length == 0:
                return (0, 0)

            max_distance = 0
            index_maxd = 0

            for i in range(1,len(array)-1):
                xp, yp = array[i]
                d = abs(dx * (yp - y_start) - dy * (xp - x_start)) / length
                if d > max_distance:
                    max_distance = d
                    index_maxd = i

            return (max_distance, index_maxd)

        def ramer_douglas_peucker_algoritm(points):
            # Rekurencyjny algorytm dziel i zwyciężaj, mający na celu podzielić całą linię na mniejsze segmenty/zredukować ilość punktów, przez usunięcie tych, które są zbyt blisko siebie, tak aby przyspieszyć działnie plotera, ale by nie zatracić jakości. 
            if len(points) < 3:
                return points
            
            max_distance, index = find_max_distance(points)

            if max_distance <= tolerance:
                return [points[0], points[-1]]
            else:
                left = ramer_douglas_peucker_algoritm(points[:index+1:])
                right = ramer_douglas_peucker_algoritm(points[index::])
                return left[:-1] + right
        
        tolerance = 0.1
        reduced_trajectory = []

        for line in trajectory_mm:
            new_line = ramer_douglas_peucker_algoritm(line)
            reduced_trajectory.append(new_line)

        return reduced_trajectory

    def run(self):
        trajectory_mm = self.normalize_trajectory_mm(self.trajectory)
        return self.trajectory_reduction(trajectory_mm)


class StepsGenerator:
    def __init__(self, trajectory, stepper_motor_data):
        self.trajectory_mm = trajectory
        self.steps_per_mm = stepper_motor_data

    def trajectory_steps(self, trajectory_mm):
        steps = []
        for line in trajectory_mm:
            single_line = []
            for x, y in line:
                step_x = round(x * self.steps_per_mm)
                step_y = round(y * self.steps_per_mm)
                single_line.append((step_x, step_y))
            steps.append(single_line)

        return steps
    
    def txt_file_write(self):
        pass

    def run(self):
        pass