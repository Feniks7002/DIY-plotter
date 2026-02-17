import math

class SinusEngine:
    def __init__(self, screen_dimensions, image_data, sin_data, offset_data):
        self.screen_width, self.screen_height = screen_dimensions
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
        
        target_w = self.screen_width - self.x_off
        target_h = self.screen_height - self.y_off

        if source_width != 0 and source_height != 0:
            scale_x = target_w / source_width
            scale_y = target_h / source_height     
            scale = min(scale_x, scale_y)
        else:
            return raw_trajectory

        normalized = []
        for i in range(len(raw_trajectory)):
            line = []
            for j in range(len(raw_trajectory[i])):
                x_shifted = raw_trajectory[i][j][0] - min_x
                y_shifted = raw_trajectory[i][j][1] - min_y
                x_scaled = x_shifted * scale + self.x_off
                y_scaled = y_shifted * scale + self.y_off
                line.append((x_scaled, y_scaled))
            normalized.append(line)
        return normalized
    
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

        trajectory = self.normalize_trajectory(raw_trajectory)

        self.txt_trajectory_test(raw_trajectory, trajectory)

        return trajectory