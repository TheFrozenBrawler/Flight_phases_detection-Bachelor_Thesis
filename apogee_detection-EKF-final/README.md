# Apogee detection algorithm with Extended Kalman Filter
This project is a **final version** of the engineering thesis "Apogee detection algorithm with Extended Kalman Filter". The main goal of the thesis is to create an algorithm to detect a rocket apogee with barometric measurements. To achieve this goal, an altitude must be estimated with use of fine-tuned Kalman Filter.

## Project setup
Created with Python 3.11.9
### Windows
1. Clone repository:
    ```cmd
    git clone https://github.com/TheFrozenBrawler/Kalman-Filter---altitude-estimation
    cd Kalman-Filter---altitude-estimation\apogee-detection-EKF-final
    ```

2. Run the environment configuration script:
    ```cmd
    .\setup.bat
    ```

3. To run the program, do the following:
    ```cmd
    .\run.bat
    ```

## Project description
### Project elements
* **main.py** - main script of the project
* **algorithms/KalmanFilter_class.py** - Kalman Filter class with EKF equations
* **algorithms/noise_adder.py** - file for adding noise to measurements
* **algorithms/FlightStages_class.py** - file with class for flight stages
* **algorithms/FlightStagesTransitions_class.py** - file with class for managing changes in flight stages
* **algorithms/RealEvents_class.py.py** - file with class for real events
* **data** - folder with simulated data of rocket flight
* **config/config.py** - file with configuration of the project
