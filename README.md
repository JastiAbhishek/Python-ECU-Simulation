# Python ECU Simulation
Description: A Python application to simulate the logic and behavior of an Electronic Control Unit (ECU) as part of a CAN bus network. The application must accept incoming data-frames, determine the appropriate action for each frame, and output the result in the correct format to the appropriate location. Each frame is analyzed to isolate the sending system, the values included in the frame, and the included error code. Based on the sending system and the error code, application logic determines an appropriate action. In the event of an error code the application determines the severity and responds by monitoring the following frames for a recurring error, or triggering a Diagnostic Trouble Code (DTC) and logging the frame in a log file. If no error is detected the application converts the data portion of the frame to a meaningful value and attaches a unit of measure based on the sending system and transmits the converted value. All signal transmission is simulated using file interaction.
