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

    def trajectory_math(self, amplitude_map, offset):
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
    
    def normalize_trajectory(self, raw_trajectory):
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
            line = []
            for x, y in line:
                x_shifted = x - min_x
                y_shifted = y - min_y
                x_scaled = x_shifted * scale + margin_x
                y_scaled = y_shifted * scale + margin_y
                line.append((x_scaled, y_scaled)) # x_mm, y_mm
            xy_mm.append(line)
        return xy_mm
    
    def txt_trajectory_test(self, raw_trajectory, trajectory):
        with open("results/trajectory_test.txt", "w") as file:
            for i in raw_trajectory:
                file.write(str(i))

        with open("results/trajectory_norma_test.txt", "w") as file:
            for i in trajectory:
                file.write(str(i))

    def run(self):
        amplitude = self.calculate_amplitude_map()

        raw_trajectory = self.trajectory_math(amplitude, (self.x_off, self.y_off))

        trajectory_mm = self.normalize_trajectory(raw_trajectory)

        self.txt_trajectory_test(raw_trajectory, trajectory_mm)

        return (trajectory_mm, raw_trajectory)