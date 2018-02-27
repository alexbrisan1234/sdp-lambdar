class PID:
    """PID Controller
    """

    def __init__(self, P=0.2, I=0.0, D=0.0, SP = 1):

        #coefficients for the terms
        self.__Kp = P
        self.__Ki = I
        self.__Kd = D
        #The terms
        self.__PTerm = 0.0
        self.__ITerm = 0.0
        self.__DTerm = 0.0
        # Distance from the obstacle
        self.__SetPoint = SP
        
        # Timestamp of last measurement
        self.__last_time = 0
        self.__last_error = 0.0
        self.output = 0.0
        # Windup Guard
        self.__windup_guard = 20.0

    def update(self, process_value, current_time):
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        .. figure:: images/pid_1.png
           :align:   center
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """ 
        delta_time = current_time - self.__last_time
        # Don't update if the datapoint is the same or older than the previous one
        if delta_time <= 0:
            return self.output
        error = process_value - self.__SetPoint
        delta_error = error - self.__last_error

        self.__PTerm = self.__Kp * error

        self.__ITerm += error * delta_time

        if (self.__ITerm < -self.__windup_guard):
             self.__ITerm = -self.__windup_guard
        elif (self.__ITerm > self.__windup_guard):
             self.__ITerm = self.__windup_guard

        self.__DTerm = delta_error / delta_time

        # Update time and error values
        self.__last_time = current_time
        self.__last_error = error

        self.output = self.__PTerm + (self.__Ki * self.__ITerm) + (self.__Kd * self.__DTerm)
        return self.output

    def update_tracking(self, left_distance, right_distance, current_time):
        return self.update(left_distance - right_distance, current_time)

    def update_collision_avoidance(self, distance, current_time):
        return self.update(distance, current_time)

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.__Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.__Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.__Kd = derivative_gain

    def setSp(self, sp):
        """Determines the distance from the wall that has to be kept constant"""
        self.__SetPoint = sp

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.__windup_guard = windup
