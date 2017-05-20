# CPRE 288 Rover Robot Web GUI

CPRE 288 is Iowa State University's Embedded Systems I class. For the final project we had to take a Roomba Robot fitted with an ARM Texas Instruments TMC Microcontroller, servo, infrared sensor, and sonar sensor, and program the robot to navigate through a challenege course. The scenario of the project was that our robot was a Mars Rover variant. We needed to develop this robot to avoid craters and other objects, remain in the competition zone, and find its way to a specified pickup zone without any onboard video or human line of sight.

My job in this four person group project was to develop the Command Center for the robot. I decided to use websockets with Flask to develop the GUI. The actual GUI design is made from HTML, Javascript, CSS, and Bootstrap. The backend, including the TCP sockets for communicating wirelessly with the robot, was developed using Python.
