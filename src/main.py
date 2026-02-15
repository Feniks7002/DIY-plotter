from image_handler import ImageHandler
from sinusoid_engine import SinusEngine
from simulation import Simulation
import config

def simulation(trajectory):
    simulation_instance = Simulation(trajectory, (config.WORK_WIDTH, config.WORK_HEIGHT))
    simulation_instance.run()

def main():
    image_instance = ImageHandler(config.IMG_PATH_E, (config.WORK_WIDTH, config.WORK_HEIGHT), config.CONTRAST_FACTOR)
    image_processed = image_instance.image_processing()

    engine_instance = SinusEngine((config.WORK_WIDTH, config.WORK_HEIGHT), image_processed, (config.SINUS_MAX_AMPLITUDE, config.SINUS_FREQUENCY, config.LINE_SPACING), (config.X_OFFSET, config.Y_OFFSET))
    sinusoid_trajectory = engine_instance.run()

    simulation(sinusoid_trajectory)


if __name__ == "__main__":
    main()


#converted_image_data = image_handler(config.IMG_PATH_E, config.CONTRAST_FACTOR, #config.WORK_WIDTH, config.WORK_HEIGHT)
#
#amplitude = amplitude_map(converted_image_data, config.SINUS_MAX_AMPLITUDE)
#
#trajectory = trajectory_math(amplitude, config.X_OFFSET, config.Y_OFFSET, config.#SINUS_FREQUENCY, config.LINE_SPACING)
#
#with open("results/trajectory_test.txt", "w") as file:
#    for i in trajectory:
#        file.write(str(i))
#
#trajectory_normalized = normalize_trajectory(trajectory, config.WORK_WIDTH, #config.WORK_HEIGHT)
#
#with open("results/trajectory_norma_test.txt", "w") as file:
#    for i in trajectory_normalized:
#        file.write(str(i))
#
#simulation(trajectory_normalized, config.WORK_WIDTH, config.WORK_HEIGHT)