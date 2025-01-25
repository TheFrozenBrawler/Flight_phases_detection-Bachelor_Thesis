import numpy as np

class KalmanFilter:
    def __init__(self, F, G, H, Q, P, x):
        self.F = F  # State transition matrix
        self.G = G  # Control input matrix
        self.H = H  # Observation matrix
        self.Q = Q  # Process noise covariance
        self.P = P  # Estimate error covariance
        self.x = x  # State estimate

    def predict(self, u):
        # Predict the state and estimate covariance
        # x = F*X + G*u
        self.x = self.F @ self.x + self.G * u

        # P_pred = F*P*A_T + Q
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z, R):
        self.R = R
        # Kalman gain
        # K = P*H.T * inv(H * P * H.T + R)
        K = self.P @ self.H.T / (self.H @ self.P @ self.H.T + self.R)

        # Update the state estimate
        # x_curr = x*K*(z-H*x)
        self.x = self.x + K * (z - self.H @ self.x)

        # Update the estimate covariance
        # P_curr = (I-K*H) * P (I-KH).T + K*R*K.T
        self.P = (np.eye(self.P.shape[0]) - K * self.H) @ self.P @ (np.eye(self.P.shape[0]) - K * self.H).T + (K*self.R@K.T)

        # P matrix trace
        P_trace = np.trace(self.P)

        return self.x[0][0], self.x[1][0], P_trace

    