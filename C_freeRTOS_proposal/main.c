// main.c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include "kalman_filter.h"
#include "flight_stages.h"
#include "config.h"
#include <stdio.h>

// Globals
QueueHandle_t sensorQueue;
SemaphoreHandle_t flightStageMutex;
FlightStages flightStages;
FlightStagesTransitions fstTransitions;

void KalmanFilterTask(void *parameters) {
    KalmanFilter kf;
    KalmanFilter_Init(&kf, TP, PRESSURE_START, ALTITUDE_START, TEMPERATURE_START, L);

    float measurement;
    while (1) {
        if (xQueueReceive(sensorQueue, &measurement, portMAX_DELAY)) {
            float alt_k, vel_k, P_trace;
            KalmanFilter_Update(&kf, measurement, R_NOMINAL, &alt_k, &vel_k, &P_trace);
            printf("Altitude: %.2f, Velocity: %.2f, P_trace: %.2f\n", alt_k, vel_k, P_trace);
        }
    }
}

void FlightStagesTask(void *parameters) {
    float est_vel;
    float timestamp = 0.0f;

    while (1) {
        // Retrieve the estimated velocity from the queue
        if (xQueueReceive(sensorQueue, &est_vel, portMAX_DELAY)) {
            xSemaphoreTake(flightStageMutex, portMAX_DELAY);

            switch (flightStages.flight_stage) {
                case STG_THRUSTING:
                    FSTrans_THRUSTING(&fstTransitions, &flightStages, est_vel, START_MACH_PHASE, MACH_THRES_SAMPL_NB, timestamp);
                    break;
                case STG_E_TRANSONIC_START:
                    FSTrans_E_TRANSONIC_START(&flightStages);
                    break;
                case STG_TRANSONIC:
                    FSTrans_TRANSONIC(&fstTransitions, &flightStages, est_vel, STOP_TRANSONIC, MACH_THRES_SAMPL_NB, timestamp);
                    break;
                case STG_E_TRANSONIC_STOP:
                    FSTrans_E_TRANSONIC_STOP(&flightStages);
                    break;
                case STG_SMOOTH_P:
                    FSTrans_SMOOTH_P(&fstTransitions, &flightStages, timestamp, MACH_SMOOTH_STAGE_TIME, MACH_THRES_SAMPL_NB);
                    break;
                case STG_CRUISING:
                    FSTrans_CRUISING(&fstTransitions, &flightStages, est_vel, APOGEE_THRES_SAMPL_NB, timestamp);
                    break;
                case STG_E_APOGEE:
                    FSTrans_E_APOGEE(&flightStages);
                    break;
                case STG_DESCENT:
                    // Handle descent logic if needed
                    break;
                default:
                    printf("Unknown flight stage\n");
                    break;
            }

            xSemaphoreGive(flightStageMutex);
        }

        // Increment timestamp based on the sampling period
        timestamp += TP;
        vTaskDelay(pdMS_TO_TICKS((int)(TP * 1000)));
    }
}


int main(void) {
    // Initialize FreeRTOS objects
    sensorQueue = xQueueCreate(10, sizeof(float));
    flightStageMutex = xSemaphoreCreateMutex();

    // Initialize flight stages
    flightStages.flight_stage = STG_THRUSTING;
    FlightStagesTransitions_Init(&fstTransitions);

    // Create tasks
    xTaskCreate(KalmanFilterTask, "KalmanFilter", 1000, NULL, 1, NULL);
    xTaskCreate(FlightStagesTask, "FlightStages", 1000, NULL, 1, NULL);

    // Start scheduler
    vTaskStartScheduler();

    return 0;
}
