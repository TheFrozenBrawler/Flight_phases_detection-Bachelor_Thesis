// flight_stages.c
#include "flight_stages.h"
#include <stdio.h>

void FlightStages_Init(FlightStages *fs) {
    fs->flight_stage = STG_THRUSTING;
    fs->mach_start_time = 0.0f;
    fs->mach_end_time = 0.0f;
    fs->apogee_time = 0.0f;
}

void FlightStagesTransitions_Init(FlightStagesTransitions *fst) {
    fst->estim_mach_start_counter = 0;
    fst->estim_mach_end_counter = 0;
    fst->estim_apogee_counter = 0;
    fst->estim_trans_end_counter = 0;
}

void FSTrans_THRUSTING(FlightStagesTransitions *fst, FlightStages *fs, float est_vel, float start_mach_phase, int mach_thres_sampl_nb, float timestamp) {
    if (est_vel > start_mach_phase) {
        fst->estim_mach_start_counter++;
        if (fst->estim_mach_start_counter >= mach_thres_sampl_nb) {
            fs->mach_start_time = timestamp;
            fs->flight_stage = STG_E_TRANSONIC_START;
        }
    }
}

void FSTrans_E_TRANSONIC_START(FlightStages *fs) {
    fs->flight_stage = STG_TRANSONIC;
}

void FSTrans_TRANSONIC(FlightStagesTransitions *fst, FlightStages *fs, float est_vel, float v_stop_transonic, int mach_thres_sampl_nb, float timestamp) {
    if (est_vel < v_stop_transonic) {
        fst->estim_mach_end_counter++;
        if (fst->estim_mach_end_counter >= mach_thres_sampl_nb) {
            fs->mach_end_time = timestamp;
            fs->flight_stage = STG_E_TRANSONIC_STOP;
        }
    }
}

void FSTrans_E_TRANSONIC_STOP(FlightStages *fs) {
    fs->flight_stage = STG_SMOOTH_P;
}

void FSTrans_SMOOTH_P(FlightStagesTransitions *fst, FlightStages *fs, float timestamp, float smooth_stage_stop_time, int mach_thres_sampl_nb) {
    if (timestamp > smooth_stage_stop_time) {
        fst->estim_trans_end_counter++;
        if (fst->estim_trans_end_counter >= mach_thres_sampl_nb) {
            fs->flight_stage = STG_CRUISING;
        }
    }
}

void FSTrans_CRUISING(FlightStagesTransitions *fst, FlightStages *fs, float est_vel, int apogee_thres_sampl_nb, float timestamp) {
    if (est_vel <= 0) {
        fst->estim_apogee_counter++;
        if (fst->estim_apogee_counter >= apogee_thres_sampl_nb) {
            fs->apogee_time = timestamp;
            fs->flight_stage = STG_E_APOGEE;
        }
    }
}

void FSTrans_E_APOGEE(FlightStages *fs) {
    fs->flight_stage = STG_DESCENT;
}
