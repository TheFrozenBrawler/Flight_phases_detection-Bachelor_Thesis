// kalman_filter.h
#ifndef KALMAN_FILTER_H
#define KALMAN_FILTER_H

#include <stdint.h>

// Kalman filter structure
typedef struct {
    float F[2][2];   // State transition matrix
    float G[2];      // Control input matrix
    float Q[2][2];   // Process noise covariance
    float P[2][2];   // Estimate error covariance
    float x[2];      // State estimate vector
    float p0;        // Initial pressure
    float alt0;      // Initial altitude
    float T_K;       // Temperature in Kelvin
    float L;         // Temperature lapse rate
} KalmanFilter;

// Function prototypes
void KalmanFilter_Init(KalmanFilter *kf, float Tp, float p0, float alt0, float T0, float L);
void KalmanFilter_Predict(KalmanFilter *kf, float u);
void KalmanFilter_Update(KalmanFilter *kf, float z, float R, float *alt_k, float *vel_k, float *P_trace);

#endif // KALMAN_FILTER_H
