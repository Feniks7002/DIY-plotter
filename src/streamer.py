import serial
import time

class GCodeStreamer:
    def __init__(self, port, timeout, baundrate, gcode_path):
        self.port = port
        self.timeout = timeout
        self.baundrate = baundrate
        self.gcode_path = gcode_path
        self.serial_port = None
    
    def connect(self):
        self.serial_port = serial.Serial(self.port, self.baundrate, timeout=self.timeout)
        time.sleep(2)
        self.serial_port.reset_input_buffer()

    def clean_line(self, line):
        line = line.split(";")[0].strip()
        if "(" in line and ")" in line:
            line = line[:line.find("(")] + line[line.find(")") + 1:]
        return line.strip()

    def emergency_stop(self):
        """Natychmiastowe zatrzymanie pracy Arduino oraz cewek silnika krokowego"""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.reset_output_buffer()
                # Wysyłanie komendy M112 do Arduino w celu natychmiastowego zatrzymania pracy
                self.serial_port.write(b"M112\n")
                self.serial_port.flush()
            except Exception:
                pass
            finally:
                self.serial_port.close()

    def stream(self):
        with open(self.gcode_path, 'r') as file:
            for line in file:
                cleaned_line = self.clean_line(line)
                if not cleaned_line:
                    continue
                
                self.serial_port.write((cleaned_line + '\n').encode('ascii'))

                while True:
                    raw_response = self.serial_port.readline()
                    if not raw_response:
                        raise TimeoutError(f"Przekroczono limit czasu odpowiedzi Arduino dla: '{cleaned_line}'")
                    
                    response = raw_response.decode("ascii", errors="replace").strip()
                    if "ok" in response:
                        break
                    elif "error" in response.lower():
                        raise RuntimeError(f"Błąd Arduino przy komendzie: '{cleaned_line}': {response}")

    def run(self):
        self.connect()
        try:
            self.stream()
        except KeyboardInterrupt:
            print("\n[E-STOP] Przerwano przesyłanie G-code przez użytkownika.")
            self.emergency_stop()
        except Exception as e:
            print(f"\nWystąpił błąd podczas przesyłania G-code: {e}")
            self.emergency_stop()