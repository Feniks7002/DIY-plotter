import math

class SinusEngine:
    def __init__(self, screen_dimensions, image_data, sin_data, offset_data):
        self.screen_width, self.screen_height = screen_dimensions
        self.img_data = image_data
        self.sin_amp, self.sin_freq, self.line_space = sin_data
        self.x_off, self.y_off = offset_data

    def amplitude_map(self, data, amplitude):
        return (1.0 - data) * amplitude

    def trajectory_math(self, amp_map, x_base, y_base, freq, line_spacing):
        trajectory = []
        for y_index in range(0, amp_map.shape[0], line_spacing):
            amplitudes = amp_map[y_index, :]
            line_points = []
            for x, amp in enumerate(amplitudes):
                y = y_base + math.sin(x * freq) * amp
                x += x_base
                line_points.append([x, y])
            trajectory.append(line_points)
            y_base += line_spacing
        return trajectory

    def normalize_trajectory(self, trajectory, target_w, target_h):
        pot_x = [point[0] for vector in trajectory for point in vector]
        pot_y = [point[1] for vector in trajectory for point in vector]
        max_x, min_x = max(pot_x), min(pot_x)
        max_y, min_y = max(pot_y), min(pot_y)
        source_width = max_x - min_x
        source_height = max_y - min_y

        if source_width != 0 and source_height != 0:
            scale_x = target_w / source_width
            scale_y = target_h / source_height     
            scale = min(scale_x, scale_y)

        normalized = []
        for i in range(len(trajectory)):
            line = []
            for j in range(len(trajectory[i])):
                x_shifted = trajectory[i][j][0] - min_x
                y_shifted = trajectory[i][j][1] - min_y
                x_scaled = x_shifted * scale
                y_scaled = y_shifted * scale
                line.append((x_scaled, y_scaled))
            normalized.append(line)
        return normalized
    
    def txt_trajectory_test(self, raw_tr, normalized_tr):
        with open("results/trajectory_test.txt", "w") as file:
            for i in raw_tr:
                file.write(str(i))

        with open("results/trajectory_norma_test.txt", "w") as file:
            for i in normalized_tr:
                file.write(str(i))

    def run(self):
        amplitude = self.amplitude_map(self.img_data, self.sin_amp)

        raw_trajectory = self.trajectory_math(amplitude, self.x_off, self.y_off, self.sin_freq, self.line_space)

        normalized_trajectory = self.normalize_trajectory(raw_trajectory, self.screen_width, self.screen_height)

        self.txt_trajectory_test(raw_trajectory, normalized_trajectory)

        return normalized_trajectory