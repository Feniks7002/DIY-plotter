from image_handler import ImageHandler
from sinusoid_engine import SinusEngine, TrajectoryNormalizer, StepsGenerator
from simulation import Simulation
from gcode_generator import GCodeGenerator
import config

def simulation(trajectory):
    simulation_instance = Simulation(trajectory, (config.RENDER_WIDTH, config.RENDER_HEIGHT))
    simulation_instance.run()

def main():
    image_instance = ImageHandler(config.IMG_PATH_L, (config.RENDER_WIDTH, config.RENDER_HEIGHT), config.CONTRAST_FACTOR)
    image_processed = image_instance.image_processing()

    engine_instance = SinusEngine(image_processed, (config.WORK_WIDTH, config.WORK_HEIGHT), (config.RENDER_WIDTH, config.RENDER_HEIGHT), (config.SINUS_MAX_AMPLITUDE, config.SINUS_FREQUENCY, config.LINE_SPACING), (config.X_OFFSET, config.Y_OFFSET))
    raw_trajectory = engine_instance.run()
    
    simulation(raw_trajectory)

    trajectory_normalizer_instance = TrajectoryNormalizer(raw_trajectory, (config.WORK_WIDTH, config.WORK_HEIGHT), config.LINE_SPACING)
    full_trajectory = trajectory_normalizer_instance.run()

    gcode_instance = GCodeGenerator(full_trajectory, (config.Z_UP, config.Z_DOWN), config.GCODE_PATH, config.TRAVEL_SPEED, config.DRAWING_SPEED)
    gcode_generate = gcode_instance.run()

    streamer_instace = GCodeStreamer(config.SERIAL_PORT, config.SERIAL_TIMEOUT, config.BAUNDRATE, config.GCODE_PATH)
    steamer_instace.run()

if __name__ == "__main__":
    main()