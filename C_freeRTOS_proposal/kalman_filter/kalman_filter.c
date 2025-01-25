// kalman_filter.c
#include "kalman_filter.h"
#include <math.h>
#include <stdio.h>

void KalmanFilter_Init(KalmanFilter *kf, float Tp, float p0, float alt0, float T0, float L) {
    kf->F[0][0] = 1.0f;
    kf->F[0][1] = Tp;
    kf->F[1][0] = 0.0f;
    kf->F[1][1] = 1.0f;

    kf->G[0] = 0.5f * Tp * Tp;
    kf->G[1] = Tp;

    kf->Q[0][0] = ACC_VAR * Tp * Tp * Tp * Tp / 4.0f;
    kf->Q[0][1] = ACC_VAR * Tp * Tp * Tp / 2.0f;
    kf->Q[1][0] = ACC_VAR * Tp * Tp * Tp / 2.0f;
    kf->Q[1][1] = ACC_VAR * Tp * Tp;

    kf->P[0][0] = P_INIT_VALUE;
    kf->P[0][1] = 0.0f;
    kf->P[1][0] = 0.0f;
    kf->P[1][1] = P_INIT_VALUE;

    kf->x[0] = alt0;
    kf->x[1] = VELOCITY_START;

    kf->p0 = p0;
    kf->alt0 = alt0;
    kf->T_K = T0 + 273.15f;
    kf->L = L;
}

void KalmanFilter_Predict(KalmanFilter *kf, float u) {
    // Predict state
    kf->x[0] = kf->F[0][0] * kf->x[0] + kf->F[0][1] * kf->x[1] + kf->G[0] * u;
    kf->x[1] = kf->F[1][0] * kf->x[0] + kf->F[1][1] * kf->x[1] + kf->G[1] * u;

    // Predict covariance
    float P00 = kf->P[0][0], P01 = kf->P[0][1], P10 = kf->P[1][0], P11 = kf->P[1][1];
    kf->P[0][0] = kf->F[0][0] * P00 + kf->F[0][1] * P10 + kf->Q[0][0];
    kf->P[0][1] = kf->F[0][0] * P01 + kf->F[0][1] * P11 + kf->Q[0][1];
    kf->P[1][0] = kf->F[1][0] * P00 + kf->F[1][1] * P10 + kf->Q[1][0];
    kf->P[1][1] = kf->F[1][0] * P01 + kf->F[1][1] * P11 + kf->Q[1][1];
}

void KalmanFilter_Update(KalmanFilter *kf, float z, float R, float *alt_k, float *vel_k, float *P_trace) {
    // Observation model
    float h_x = kf->p0 * powf(1.0f + (kf->L / kf->T_K) * (kf->x[0] - kf->alt0), 5.2558f);
    float dh_dx = 5.2558f * kf->L * kf->p0 * powf(fabsf((kf->L * (kf->x[0] + kf->alt0)) / kf->T_K + 1.0f), 4.2558f) / kf->T_K;

    // Kalman gain
    float K[2];
    float S = dh_dx * kf->P[0][0] * dh_dx + R;
    K[0] = kf->P[0][0] * dh_dx / S;
    K[1] = kf->P[1][0] * dh_dx / S;

    // Update state estimate
    float y = z - h_x; // Measurement residual
    kf->x[0] += K[0] * y;
    kf->x[1] += K[1] * y;

    // Update covariance
    float P00 = kf->P[0][0], P01 = kf->P[0][1], P10 = kf->P[1][0], P11 = kf->P[1][1];
    kf->P[0][0] = (1 - K[0] * dh_dx) * P00;
    kf->P[0][1] = (1 - K[0] * dh_dx) * P01;
    kf->P[1][0] = (1 - K[1] * dh_dx) * P10;
    kf->P[1][1] = (1 - K[1] * dh_dx) * P11;

    // Output results
    *alt_k = kf->x[0];
    *vel_k = kf->x[1];
    *P_trace = kf->P[0][0] + kf->P[1][1];
}
