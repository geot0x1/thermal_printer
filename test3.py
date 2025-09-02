from pprint import pprint

class ThermalPrinterParser:
    """
    A simple state-machine parser for thermal printer byte streams.
    """
    def __init__(self):
        self.TEXT_MODE = "TEXT_MODE"
        self.COMMAND_MODE = "COMMAND_MODE"
        self.GRAPHICS_MODE = "GRAPHICS_MODE"
        self.state = self.TEXT_MODE
        self.output = []

    def parse_stream(self, hex_stream):
        """
        Parses a hexadecimal string byte stream and interprets the commands and data.
        """
        # Remove spaces and convert hex string to a list of integers
        hex_stream = hex_stream.replace(" ", "").replace("\n", "")
        byte_list = [int(hex_stream[i:i+2], 16) for i in range(0, len(hex_stream), 2)]
        
        i = 0
        while i < len(byte_list):
            current_byte = byte_list[i]

            # --- State Machine Logic ---
            if self.state == self.TEXT_MODE:
                if current_byte == 0x1B:
                    self.state = self.COMMAND_MODE
                    self.output.append({'type': 'state_change', 'from': 'TEXT_MODE', 'to': 'COMMAND_MODE', 'trigger': hex(current_byte)})
                elif current_byte == 0x0D:
                    self.output.append({'type': 'control', 'name': 'Carriage Return', 'value': hex(current_byte)})
                else:
                    try:
                        char = chr(current_byte)
                        self.output.append({'type': 'text_data', 'value': char, 'hex': hex(current_byte)})
                    except ValueError:
                        self.output.append({'type': 'text_data', 'value': 'Invalid ASCII', 'hex': hex(current_byte)})
            
            elif self.state == self.COMMAND_MODE:
                if current_byte == 0x41:  # Command: Alignment (ESC A)
                    alignment_param = byte_list[i+1]
                    param_desc = "center" if alignment_param == 0x08 else "unknown"
                    self.output.append({'type': 'command', 'name': 'Alignment', 'parameter': hex(alignment_param), 'description': param_desc})
                    i += 1  # Skip parameter byte
                    self.state = self.TEXT_MODE
                elif current_byte == 0x4B: # Command: Graphics (ESC K)
                    graphics_mode = byte_list[i+1]
                    if graphics_mode == 0x55:
                         mode_desc = "Start Graphics (U)"
                    elif graphics_mode == 0x59:
                         mode_desc = "Start Graphics (Y)"
                    else:
                         mode_desc = "Unknown Mode"
                    self.output.append({'type': 'command', 'name': 'Graphics', 'mode': hex(graphics_mode), 'description': mode_desc})
                    i += 1
                    self.state = self.GRAPHICS_MODE
                else:
                    self.output.append({'type': 'command', 'name': 'Unknown', 'value': hex(current_byte)})
                    self.state = self.TEXT_MODE

            elif self.state == self.GRAPHICS_MODE:
                if current_byte == 0x1B:
                    self.output.append({'type': 'state_change', 'from': 'GRAPHICS_MODE', 'to': 'COMMAND_MODE', 'trigger': hex(current_byte)})
                    self.state = self.COMMAND_MODE
                elif current_byte == 0x0D:
                    self.output.append({'type': 'control', 'name': 'Carriage Return', 'value': hex(current_byte)})
                    self.state = self.TEXT_MODE
                else:
                    # Treat byte as graphics data
                    binary_rep = bin(current_byte)[2:].zfill(8)
                    self.output.append({'type': 'graphics_data', 'hex': hex(current_byte), 'binary': binary_rep})

            i += 1
        
        return self.output

if __name__ == '__main__':
    parser = ThermalPrinterParser()

    # The full byte stream you provided, cleaned up for parsing
    test_stream = """
    1B 41 08 20 20 20 31 2E 30 20 1B 4B 55 00 FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0D
    20 20 20 20 20 20 20 1B 4B 55 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 55 00 30 30 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF 20 20 20 4D 45 50 20 3D 20 20 20 31 38 20 64 61 50 61 0D
    """
    
    parsed_output = parser.parse_stream(test_stream)
    pprint(parsed_output)
