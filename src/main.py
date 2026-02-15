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