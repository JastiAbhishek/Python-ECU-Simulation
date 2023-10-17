from pathlib import Path
import datetime

def convert_data(sensorCode, data_a, data_b, data_c):
    intValue_a = int(data_a, 16)
    intValue_b = int(data_b, 16)
    intValue_c = int(data_c, 16)
    data_a = float(intValue_a)
    data_b = float(intValue_b)
    data_c = float(intValue_c)

    if sensorCode =='0a':
        converted_data = 3 * data_a                                                  # Fuel pressure conversion formula: 3A
        unit = 'kPa'
        sensor_name = 'fuel pressure'
        if not (0.0 <= converted_data <= 765):
            converted_data = None
        return sensor_name, converted_data, unit
    elif sensorCode == '0c':
        converted_data = ((256 * data_a) + data_b)/4                                 # Engine speed conversion formula: ((256A + B)/4)
        unit = 'rpm'
        sensor_name = 'engine speed'
        if not (0 <= converted_data <= 16383.75):
            converted_data = None
        return sensor_name, converted_data, unit
    elif sensorCode == '0d':
        converted_data = data_c                                                      # Vehicle speed conversion formula: C
        unit = 'km/h'
        sensor_name = 'vehicle speed'
        if not (0 <= converted_data <= 255):
            converted_data = None
        return sensor_name, converted_data, unit
    elif (sensorCode == '11') or (sensorCode == '2f'):
        converted_data = (100/255)*data_a                                            # Throttle position and fuel tank conversion formula: ((100/225)A)
        unit = '%'
        if sensorCode == '11':
            sensor_name = 'throttle position'
        else:
            sensor_name = 'fuel tank level'
        if not (0 <= converted_data <= 100):
            converted_data = None
        return sensor_name, converted_data, unit
    elif (sensorCode == '5c') or (sensorCode == '67') or (sensorCode == '68'):
        unit = 'C'                                                                  # Oil temperature, engine coolant temperature, and air intake temperature conversion formula: Respectively [(A-40), (B-40), and (C-40)]
        if sensorCode == '5c':
            converted_data = data_a - 40  
            sensor_name = 'oil temperature'
        elif sensorCode == '67':
            converted_data = data_b - 40  
            sensor_name = 'engine coolant temperature'
        else:
            converted_data = data_c - 40  
            sensor_name = 'air intake temperature'
        if not (-40 <= converted_data <= 215):
            converted_data = None
        return sensor_name, converted_data, unit
    else:
        return print("No sensor code was found.")

# relativePath = './Week II Mini-Project/inputdataframes.txt'
# relativePath = './Week II Mini-Project/Project Data Sets/Data_A.txt'
# relativePath = './Week II Mini-Project/Project Data Sets/Data_B.txt'
relativePath = './Week II Mini-Project/Project Data Sets/Data_C.txt'
# relativePath = './Week II Mini-Project/Project Data Sets/input_data_sample.txt'
# relativePath = './Week II Mini-Project/Project Data Sets/LData_A.txt'
# relativePath = './Week II Mini-Project/Project Data Sets/LData_B.txt'
# relativePath = './Week II Mini-Project/Project Data Sets/LData_C.txt'


inputFile = Path(relativePath)

with open(inputFile, 'r') as input_file:
    input_frames = input_file.readlines()

output_data = []
error_count = 0
fpcounter = 0
escounter = 0
vscounter = 0
tpcounter = 0
ftlcounter = 0
otcounter = 0
ectcounter = 0
aitcounter = 0

with open('output_data.txt', 'w') as output_file, open('log.txt', 'w') as log_file:
    for i, frame in enumerate(input_frames, start = 1):
        sensorCode, data_a, data_b, data_c, error = frame.split()
        sensor_name, converted_data, unit = convert_data(sensorCode, data_a, data_b, data_c)
        error_message = ''
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        error_dict = {
                'fuel pressure': 'DTC - P0091',
                'engine speed': 'DTC - P0725',
                'vehicle speed': 'DTC - P215A',
                'throttle position': 'DTC - P0510',
                'fuel tank level': 'DTC - P0656',
                'oil temperature': 'DTC - P0195',
                'engine coolant temperature': 'DTC - P0217',
                'air intake temperature': 'DTC - P0127'
            }
        
        error_explanation_dict = {
            'fuel pressure': 'Fuel Pressure regulator 1 control circuit low.',
            'engine speed': 'Engine Speed Input ciruit.',
            'vehicle speed': 'Vehicle Speed Wheel Speed Correlation.',
            'throttle position': 'Closed Throttle Position Switch',
            'fuel tank level':  'Fuel Level Output circuit',
            'oil temperature':  'Engine Oil Temperature sensor',
            'engine coolant temperature': 'Engine Coolant Over Temperature condition',
            'air intake temperature': 'Intake Air Temperature Too High'
        }

        if error == '00':
            if error == '00' and sensor_name == 'fuel pressure':
                fpcounter = 0
            elif error == '00' and sensor_name == 'engine speed':
                escounter = 0
            elif error == '00' and sensor_name == 'vehicle speed':
                vscounter = 0
            elif error == '00' and sensor_name == 'throttle position':
                tpcounter = 0
            elif error == '00' and sensor_name == 'fuel tank level':
                ftlcounter = 0
            elif error == '00' and sensor_name == 'oil temperature':
                otcounter = 0
            elif error == '00' and sensor_name == 'engine coolant temperature':
                ectcounter = 0
            elif error == '00' and sensor_name == 'air intake temperature':
                aitcounter = 0

            error_message = 'Value not in range.'
            if converted_data is not None:
                output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
            else:
                output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
        elif error == '0f':
            if error == '0f' and sensor_name == 'fuel pressure':
                fpcounter += 1
            elif error == '0f' and sensor_name == 'engine speed':
                escounter += 1
            elif error == '0f' and sensor_name == 'vehicle speed':
                vscounter += 1
            elif error == '0f' and sensor_name == 'throttle position':
                tpcounter += 1
            elif error == '0f' and sensor_name == 'fuel tank level':
                ftlcounter += 1
            elif error == '0f' and sensor_name == 'oil temperature':
                otcounter += 1
            elif error == '0f' and sensor_name == 'engine coolant temperature':
                ectcounter += 1
            elif error == '0f' and sensor_name == 'air intake temperature':
                aitcounter += 1

            error_message = error_dict.get(sensor_name, '')
            error_explanation = error_explanation_dict.get(sensor_name, '')

            if fpcounter >= 3 and sensor_name == 'fuel pressure':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            elif escounter >= 3 and sensor_name == 'engine speed':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            elif vscounter >= 3 and sensor_name == 'vehicle speed':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            elif tpcounter >= 3 and sensor_name == 'throttle position':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            elif ftlcounter >= 3 and sensor_name == 'fuel tank level':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            elif otcounter >= 3 and sensor_name == 'oil temperature':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            elif ectcounter >= 3 and sensor_name == 'engine coolant temperature':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            elif aitcounter >= 3 and sensor_name == 'air intake temperature':
                error_count += 1
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
                log_file.write(f"Frame {i}: Single event error detected 3 times, {error_message} generated - {error_explanation}\n")
            else:
                if converted_data is not None:
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {int(converted_data)} {unit}\n"
                else:
                    error_message = 'Value not in range.'
                    output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
        elif error == 'ff':
            error_count += 1
            error_message = error_dict.get(sensor_name, '')
            error_explanation = error_explanation_dict.get(sensor_name, '')
            output_line = f"Frame {i} - {current_time} - {sensor_name} - {error_message}\n"
            log_file.write(f"Frame {i}: {current_time} - {sensor_name} - {error_message} - {error_explanation}\n")

        output_data.append(output_line)
        output_file.write(output_line)

    log_file.write(f"Number of input data frames analyzed: {i}\n")
    log_file.write(f"Number of errors detected: {error_count}\n")

print("Output Data:")
print("".join(output_data))