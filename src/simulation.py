import tkinter as tk

class Simulation:
    def __init__(self, trajectory, screen_dimension):
        self.trajectory = trajectory
        self.screen_width, self.screen_height = screen_dimension

    def run(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, bg='white')
        canvas.pack()

        for line in self.trajectory:
            for i in range(len(line)-1):
                x1, y1 = line[i]
                x2, y2 = line[i + 1]
                canvas.create_line(x1, y1, x2, y2, fill='black')
        root.mainloop()