
class GCodeGenerator:
    def __init__(self, trajectory_mm, z_positions, result_path, feedrate_travel, feedrate_draw):
        self.trajectory_map = trajectory_mm
        self.f_travel = feedrate_travel
        self.f_draw = feedrate_draw
        self.z_up, self.z_down = z_positions
        self.path = result_path

    def generate_code(self):
        gcode = [
            "; --- PREAMBLE ---",
            "G21 ; Millimeters",
            "G90 ; Absolute coordinates",
            f"G00 Z{self.z_up:.2f} F{self.f_travel}"
        ]

        if not self.trajectory_map or not self.trajectory_map[0]:
            return gcode

        # Dojazd do pierwszego punktu
        first_x, first_y = self.trajectory_map[0][0]
        gcode.append(f"G00 X{first_x:.2f} Y{first_y:.2f}")
        gcode.append(f"G01 Z{self.z_down:.2f} F{self.f_draw}")
        gcode.append(f"G04 P0.2")

        # Rysowanie całej trajektorii
        gcode.append(f"; --- TRAJECTORY ---")
        for line in self.trajectory_map:
            for x, y in line:
                gcode.append(f"G1 X{x:.2f} Y{y:.2f} F{self.f_draw}")

        # Zakończenie pracy
        gcode.extend([
            "; --- POSTAMBLE ---",
            f"G00 Z{self.z_up:.2f} F{self.f_travel}",
            "G00 X0.00 Y0.00",
            "M02 ; End of program"
        ])

        return gcode

    def save_file(self, path, gcode_list):
        with open(path, "w", encoding="utf-8") as file:
            for element in gcode_list:
                file.write(element + "\n")

    def run(self):
        generated_code = self.generate_code()
        save = self.save_file(self.path, generated_code)