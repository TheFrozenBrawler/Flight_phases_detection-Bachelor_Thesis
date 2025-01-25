# Apogee detection algorithm with Linear Kalman Filter
This project is part of the process to create an algorithm to detect a rocket flight parameters with barometric measurements. There is no algorithm for detecting the moment of apogee, because the performance of the filter was not satisfactory. The improved, final version of KF is in the project apogee_detecion-EKF-final.

## Project setup
Created with Python 3.11.9
### Windows
1. Clone repository:
    ```cmd
    git clone https://github.com/TheFrozenBrawler/Kalman-Filter---altitude-estimation
    cd Kalman-Filter---altitude-estimation\apogee_detection-LKF
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
* **KalmanFilter_class.py** - Kalman Filter class with linear KF equations
* **noise_adder.py** - file for adding noise to measurements
* **data folder** - folder with simulated data of rocket flight
* **config.py** - file with configuration of the project
* **pressure_preprocessing.py** - file with algorithm to calculate altitude from pressure
