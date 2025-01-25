# Flight phases detection algorithm
This repository contains the code for the flight phases detection algorithm created during the bachelor thesis "Development of an algorithm for detecting rocket flight parameters from barometer readings" in Poznan University of Technology.

## Abstract
This thesis presents the process of creating an algorithm for detecting rocket flight parameters based on barometer readings. The analysis of the requirements for the algorithm led to the use of the Kalman filter as the main filtering component, enabling the estimation of true flight parameters. The design and testing process of the filter is subsequently described, initially as a linear model (Linear Kalman Filter) and later as an extended model (Extended Kalman Filter), which allowed achieving the required algorithm performance. Additionally, the method for determining the apogee and other phases of rocket flight is explained. A significant component enabling the testing of the developed algorithm was a program simulating measurement errors observed during the flight phase at speeds near or exceeding the speed of sound, caused by breaking the sound barrier.
The process of modeling rocket flight altitude using accelerometer readings is also detailed by describing the state equations and subsequently adapting them to the form required by the filter, as well as the method for obtaining correct algorithm settings.
In the final stage of the work, the performance analysis of the final version of the algorithm is presented, along with a proposal for implementation in C and FreeRTOS, and development trends that offer the possibility of extending the algorithm’s functionality to detect rocket flight phases such as engine ignition, acceleration, engine burnout, or coasting. 

## Repository structure
- **apogee_detection-LKF** - folder with algorithm implementation with Linear Kalman Filter. It was a part of the process of creating the algorithm. During tests, it was found that the algorithm does not meet the requirements, so it was replaced by the Extended Kalman Filter.
- **apogee_detection-EKF-final** - folder with the final version of the algorithm with Extended Kalman Filter. It meets the requirements and is ready for implementation in C and FreeRTOS.
- **C_freeRTOS_proposal** - folder with a proposal for the implementation of the algorithm in C and FreeRTOS.
- **Maciej Kowalski, praca inżynierska - Algorytm wykrywania parametrów lotu rakiety na podstawie odczytów barometru** - a file with the bachelor thesis in Polish.
