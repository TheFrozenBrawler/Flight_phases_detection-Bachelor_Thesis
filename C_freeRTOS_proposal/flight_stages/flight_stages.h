// flight_stages.h
#ifndef FLIGHT_STAGES_H
#define FLIGHT_STAGES_H

#include <stdint.h>

// Flight stage constants
#define STG_THRUSTING           0
#define STG_E_TRANSONIC_START   1
#define STG_TRANSONIC           2
#define STG_E_TRANSONIC_STOP    3
#define STG_SMOOTH_P            4
#define STG_CRUISING            5
#define STG_E_APOGEE            6
#define STG_DESCENT             7

// Structures
typedef struct {
    int flight_stage;          // Current flight stage
    float mach_start_time;     // Timestamp when mach phase starts
    float mach_end_time;       // Timestamp when mach phase ends
    float apogee_time;         // Timestamp of apogee
} FlightStages;

typedef struct {
    int estim_mach_start_counter;  // Counter for mach start detection
    int estim_mach_end_counter;    // Counter for mach end detection
    int estim_apogee_counter;      // Counter for apogee detection
    int estim_trans_end_counter;   // Counter for smooth transition end
} FlightStagesTransitions;

// Function prototypes
void FlightStages_Init(FlightStages *fs);
void FlightStagesTransitions_Init(FlightStagesTransitions *fst);

void FSTrans_THRUSTING(FlightStagesTransitions *fst, FlightStages *fs, float est_vel, float start_mach_phase, int mach_thres_sampl_nb, float timestamp);
void FSTrans_E_TRANSONIC_START(FlightStages *fs);
void FSTrans_TRANSONIC(FlightStagesTransitions *fst, FlightStages *fs, float est_vel, float v_stop_transonic, int mach_thres_sampl_nb, float timestamp);
void FSTrans_E_TRANSONIC_STOP(FlightStages *fs);
void FSTrans_SMOOTH_P(FlightStagesTransitions *fst, FlightStages *fs, float timestamp, float smooth_stage_stop_time, int mach_thres_sampl_nb);
void FSTrans_CRUISING(FlightStagesTransitions *fst, FlightStages *fs, float est_vel, int apogee_thres_sampl_nb, float timestamp);
void FSTrans_E_APOGEE(FlightStages *fs);

#endif // FLIGHT_STAGES_H
