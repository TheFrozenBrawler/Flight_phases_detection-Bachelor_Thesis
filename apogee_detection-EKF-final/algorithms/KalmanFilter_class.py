import numpy as np

class KalmanFilter_class:
    def __init__(self, F, G, Q, P, x, p0, alt0, T0, L):
        self.F = F  # State transition matrix
        self.G = G  # Control input matrix
        self.Q = Q  # Process noise covariance
        self.P = P  # Estimate error covariance
        self.x = x  # State estimate

        self.p0 = p0
        self.alt0 = alt0
        self.T_K = T0 + 273.15
        self.L = L

    def predict(self, u):
        # Predict the state and estimate covariance
        # x = F*X + G*u
        self.x = self.F @ self.x + self.G * u

        # P_pred = F*P*A_T + Q
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z, R):
        # R update
        self.R = R

        # linearize the observation model
        h_x = self.h_x(self.x[0][0])
        dh_dx = self.dh_dx(self.x[0][0])

        # Kalman gain
        # K = P*H.T * inv(H * P * H.T + R)
        K = self.P @ dh_dx.T / (dh_dx @ self.P @ dh_dx.T + self.R)

        # Update the state estimate
        # x_curr = x*K*(z-H*x)
        self.x = self.x + K * (z - h_x)

        # Update the estimate covariance
        # P_curr = (I-K*H) * P (I-KH).T + K*R*K.T
        self.P = (np.eye(self.P.shape[0]) - K * dh_dx) @ self.P @ (np.eye(self.P.shape[0]) - K * dh_dx).T + (K*self.R@K.T)

        # P matrix trace
        P_trace = np.trace(self.P)

        return self.x[0][0], self.x[1][0], P_trace
    
    def update_P(self, P_new):
        self.P = P_new

    ''' UKF additional functions '''
    def h_x(self, alt_pred):
        h_x = self.p0 * (1+(self.L/self.T_K)*(alt_pred-self.alt0))**5.2558

        return h_x

    def dh_dx(self, alt_pred):
        dh_dhn = ( 5.257*self.L*self.p0* ( np.abs(((self.L*(alt_pred+self.alt0))/(self.T_K))+1 ))**4.257 ) / (self.T_K)

        dh_dx = np.array([dh_dhn, 0.0])

        return dh_dx
