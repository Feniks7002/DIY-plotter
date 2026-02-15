import math
import tkinter as tk
import numpy as np
import config
from PIL import Image, ImageEnhance

def image_handler(path, contrast_factor, max_w, max_h):
    def contrast_enchance(img, factor):
        img_contrast_enchance = ImageEnhance.Contrast(img)
        return img_contrast_enchance.enhance(factor)
    
    image = Image.open(path)
    image.thumbnail((max_w, max_h))

    img_gray = image.convert('L')

    img_gray_enchanced = contrast_enchance(img_gray, contrast_factor)    
    
    img_array = np.array(img_gray_enchanced)
    img_normalized = img_array / 255.0
    return img_normalized

def amplitude_map(data, max_amp):
    return (1.0 - data) * max_amp

def trajectory_math(amp_map, x_base, y_base, freq, line_spacing):
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

def normalize_trajectory(pen_trajectory, target_w, target_h):
    pot_x = [point[0] for vector in pen_trajectory for point in vector]
    pot_y = [point[1] for vector in pen_trajectory for point in vector]
    max_x, min_x = max(pot_x), min(pot_x)
    max_y, min_y = max(pot_y), min(pot_y)
    source_width = max_x - min_x
    source_height = max_y - min_y

    if source_width != 0 and source_height != 0:
        scale_x = target_w / source_width
        scale_y = target_h / source_height     
        scale = min(scale_x, scale_y)
    
    normalized = []
    for i in range(len(pen_trajectory)):
        line = []
        for j in range(len(pen_trajectory[i])):
            x_shifted = pen_trajectory[i][j][0] - min_x
            y_shifted = pen_trajectory[i][j][1] - min_y
            x_scaled = x_shifted * scale
            y_scaled = y_shifted * scale
            line.append((x_scaled, y_scaled))
        normalized.append(line)
    return normalized

def simulation(pen_trajectory, w, h):
    root = tk.Tk()
    canvas = tk.Canvas(root, width=w, height=h, bg='white')
    canvas.pack()

    for line in pen_trajectory:
        for i in range(len(line)-1):
            x1, y1 = line[i]
            x2, y2 = line[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill='black')
    root.mainloop()



converted_image_data = image_handler(config.IMG_PATH_E, config.CONTRAST_FACTOR, config.WORK_WIDTH, config.WORK_HEIGHT)

amplitude = amplitude_map(converted_image_data, config.SINUS_MAX_AMPLITUDE)

trajectory = trajectory_math(amplitude, config.X_OFFSET, config.Y_OFFSET, config.SINUS_FREQUENCY, config.LINE_SPACING)

with open("results/trajectory_test.txt", "w") as file:
    for i in trajectory:
        file.write(str(i))

trajectory_normalized = normalize_trajectory(trajectory, config.WORK_WIDTH, config.WORK_HEIGHT)

with open("results/trajectory_norma_test.txt", "w") as file:
    for i in trajectory_normalized:
        file.write(str(i))

simulation(trajectory_normalized, config.WORK_WIDTH, config.WORK_HEIGHT)