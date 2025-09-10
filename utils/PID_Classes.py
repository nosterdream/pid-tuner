from math import exp


class PID_Object:
    def __init__(self, order, k_ob, tau_ob, t1_ob, t2_ob=None):
        self.order = order
        self.k_ob = k_ob
        self.tau_ob = tau_ob
        self.t1_ob = t1_ob
        self.t2_ob = t2_ob

        self.p_pid = None
        self.i_pid = None
        self.d_pid = None

        self.overshoot = None
        self.disturbance = None
        self.pid = None
        self.lamb = 3.0

        self.method = None

    def calculate_pid(self):
        match self.method:
            case "Optimal Modulus method":
                self.optimal_module_method()
            case "Aperiodic Stability Method":
                self.aperiodic_stability_method()
            case "Coon Method":
                self.coon_method()
            case "Kopelovich Method":
                self.kopelovich_method()
            case "Kopelovich-Sharkov Method":
                self.kopelovich_sharkov_method()
            case "Skogestads Method":
                self.skogestads_method()
            case "Lambda Method":
                self.lambda_method()
            case "AMIGO Method":
                self.amigo_method()
            case "Ziegler-Nichols Method":
                self.ziegler_nichols()
            case "Max Stability Method":
                self.max_stability_method()
            case "Huang Method":
                self.huang_method()
            case _:
                pass

    def __str__(self):
        if self.t2_ob is None:
            if self.pid == 0:
                return f"PID_Object 1st Order\nK = {round(self.k_ob, 4)} \nT = {self.t1_ob} \ntau = {self.tau_ob}\n\n\
Standard Form\nP = {round(self.p_pid, 4)}\nI = {round(self.i_pid, 4)}"
            elif self.pid == 1:
                return f"PID_Object 1st Order\nK = {round(self.k_ob, 4)} \nT = {self.t1_ob} \ntau = {self.tau_ob}\n\n\
Standard Form\nP = {round(self.p_pid, 4)}\nI = {round(self.i_pid, 4)} \nD = {round(self.d_pid, 4)}"
        else:
            if self.pid == 0:
                return f"PID_Object 2nd Order\nK = {round(self.k_ob, 4)} \nT1 = {self.t1_ob} \nT2 = {self.t2_ob} \ntau \
= {self.tau_ob}\n\n\
Standard Form\nP = {round(self.p_pid, 4)} \nI = {round(self.i_pid, 4)}"
            elif self.pid == 1:
                return f"PID_Object 2nd Order\nK = {round(self.k_ob, 4)} \nT1 = {self.t1_ob} \nT2 = {self.t2_ob} \ntau \
= {self.tau_ob}\n\nStandard Form\n\
P = {round(self.p_pid, 4)} \nI = {round(self.i_pid, 4)} \nD = {round(self.d_pid, 4)}"

    def optimal_module_method(self):
        t = self.t1_ob / self.tau_ob
        if self.t2_ob is None:
            if self.pid == 0:
                kr = (6 * t ** 3 + 6 * t ** 2 + 3 * t + 1) / (4 * (3 * t ** 2 + 3 * t + 1))
                i = (6 * t ** 3 + 6 * t ** 2 + 3 * t + 1) / (6 * t ** 2 + 6 * t + 3)
                self.p_pid = kr
                self.i_pid = i * self.tau_ob

            elif self.pid == 1:
                i = (180 * t ** 4 + 240 * t ** 3 + 135 * t ** 2 + 42 * t + 7) / (
                            15 * (2 * t + 1) * (6 * t ** 2 + 3 * t + 1))
                d = (60 * t ** 4 + 60 * t ** 3 + 27 * t ** 2 + 7 * t + 1) / (
                            180 * t ** 4 + 240 * t ** 3 + 135 * t ** 2 + 42 * t + 7)
                kr = 1 / (2 / i * (t + 1) - 2)
                self.p_pid = kr
                self.i_pid = i * self.tau_ob
                self.d_pid = d * self.tau_ob

        else:
            t1 = self.t1_ob / self.tau_ob
            t2 = self.t2_ob / self.tau_ob
            if self.pid == 0:
                kr = (3 * (2 * (t2 ** 3 + t2 ** 2 * t1 + t1 ** 3) + 2 * (
                            t2 ** 2 + t2 * t1 + t1 ** 2) + t2 + t1) + 1) / (
                             12 * (t1 + t2) * (t1 * t2 + t1 + t2 + 1) + 4)
                i = (2 * kr * (t1 + t2 + 1)) / (2 * kr + 1)
                self.p_pid = kr
                self.i_pid = i * self.tau_ob

            elif self.pid == 1:
                t1 = self.t1_ob / self.tau_ob
                t2 = self.t2_ob / self.tau_ob
                kr = (360 * t1 ** 2 * t2 ** 2 * (t2 ** 3 + 3 * t1 * t2 ** 2 + 3 * t2 * t1 ** 2 + t1 ** 3) +
                      360 * t1 * t2 * (t2 ** 4 + 5 * t1 * t2 ** 3 + 8 * t1 ** 2 * t2 ** 2 + 5 * t1 ** 3 * t2 + t1 ** 4)
                      + 180 * (t2 ** 5 + 7 * t1 * t2 ** 4 + 16 * t1 ** 2 * t2 ** 3 + 16 * t1 ** 3 * t2 ** 2 + 7 * t1 **
                      4 * t2 + t1 ** 5) + 60 * (7 * t2 ** 4 + 25 * t1 * t2 ** 3 + 36 * t1 ** 2 * t2 ** 2 + 25 * t1 ** 3
                      * t2 + 7 * t1 ** 4) + 5 * (75 * t2 ** 3 + 177 * t1 * t2 ** 2 + 177 * t1 ** 2 * t2 + 75 * t1 ** 3)
                      + 3 * (59 * t2 ** 2 + 98 * t1 * t2 + 59 * t1 ** 2) + 49 * (t1 + t2) + 7) / (720 * (t1 + t2) ** 2
                      * t1 ** 2 * t2 ** 2 + 720 * (t1 + t2) * t1 * t2 * (t2 ** 2 + 3 * t1 * t2 + t1 ** 2) + 240 *
                      (t1 + t2) ** 2 * (t2 ** 2 + 6 * t1 * t2 + t1 ** 2) + 240 * (t1 + t2) * (2 * t2 ** 2 + 5 * t1 * t2
                      + 2 * t1 ** 2) + 336 * (t1 + t2) ** 2 + 112 * (t1 + t2) + 16)
                i = (2 * kr * (t1 + t2 + 1)) / (2 * kr + 1)
                d = (4 * kr * (3 * (t1 + t2) * (2 * t2 + t1 + 1) + 1) - 3 * (t1 + t2) * (2 * (t2 ** 2 + t1 ** 2) + 3) -
                     6 * (t2 ** 2 + t2 * t1 + t1 ** 2) - 1) / (12 * kr * ((t1 + t2) * (t1 + t2 + 2) + 1))
                self.p_pid = kr
                self.i_pid = i * self.tau_ob
                self.d_pid = d * self.tau_ob

    def aperiodic_stability_method(self):
        t = self.t1_ob / self.tau_ob
        tt = 1 / (2 * t)
        if self.pid == 0:
            rk = (2 + tt ** 2) ** (1 / 2) - (2 + tt)
            i = (1 + tt ** 2) / ((3 + tt + 4 * tt ** 2 + tt ** 3) - (2 + tt ** 2) * (2 + tt ** 2) ** (1 / 2))
            kr = 2 * t * ((2 + tt ** 2) ** (1 / 2) - 1) * exp(rk)
            self.p_pid = kr
            self.i_pid = i * self.tau_ob
        elif self.pid == 1:
            rk = (3 + tt ** 2) ** (1 / 2) - (3 + tt)
            i = ((6 + tt) * (3 + tt ** 2) ** (1 / 2) - (9 + tt + tt ** 2)) / (
                    (21 + 6 * tt + tt ** 2) * (3 + tt ** 2) ** (1 / 2) - (36 + 9 * tt + 6 * tt ** 2 + tt ** 3))
            d = ((3 + tt ** 2) ** (1 / 2) - 1) / (2 * ((6 + tt) * (3 + tt ** 2) ** (1 / 2) - (9 + tt + tt ** 2)))
            kr = 2 * t * (((6 + tt) * (3 + tt ** 2) ** (1 / 2)) - (9 + tt + tt ** 2)) * exp(rk)
            self.p_pid = kr
            self.i_pid = i * self.tau_ob
            self.d_pid = d * self.tau_ob

    def coon_method(self):
        if self.pid == 0:
            if self.overshoot == 0:
                if self.disturbance == 0:
                    self.p_pid = 0.35 * self.t1_ob / self.tau_ob
                    self.i_pid = 1.2 * self.tau_ob
                elif self.disturbance == 1:
                    self.p_pid = 0.6 * self.t1_ob / self.tau_ob
                    self.i_pid = 4 * self.tau_ob
            elif self.overshoot == 1:
                if self.disturbance == 0:
                    self.p_pid = 0.6 * self.t1_ob / self.tau_ob
                    self.i_pid = self.tau_ob
                elif self.disturbance == 1:
                    self.p_pid = 0.7 * self.t1_ob / self.tau_ob
                    self.i_pid = 2.3 * self.tau_ob
        elif self.pid == 1:
            if self.overshoot == 0:
                if self.disturbance == 0:
                    self.p_pid = 0.6 * self.t1_ob / self.tau_ob
                    self.i_pid = self.tau_ob
                    self.d_pid = 0.5 * self.tau_ob
                elif self.disturbance == 1:
                    self.p_pid = 0.95 * self.t1_ob / self.tau_ob
                    self.i_pid = 2.4 * self.tau_ob
                    self.d_pid = 0.42 * self.tau_ob
            elif self.overshoot == 1:
                if self.disturbance == 0:
                    self.p_pid = 0.95 * self.t1_ob / self.tau_ob
                    self.i_pid = 1.35 * self.tau_ob
                    self.d_pid = 0.47 * self.tau_ob
                elif self.disturbance == 1:
                    self.p_pid = 1.2 * self.t1_ob / self.tau_ob
                    self.i_pid = 2 * self.tau_ob
                    self.d_pid = 0.42 * self.tau_ob

    def kopelovich_method(self):
        if self.pid == 0:
            if self.overshoot == 0:
                self.p_pid = 0.6 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 0.6 * self.t1_ob
            elif self.overshoot == 1:
                self.p_pid = 0.7 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 0.7 * self.t1_ob
            elif self.overshoot == 2:
                self.p_pid = 1.0 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = self.t1_ob
        elif self.pid == 1:
            if self.overshoot == 0:
                self.p_pid = 0.95 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 2.4 * self.tau_ob
                self.d_pid = 0.4 * self.tau_ob
            elif self.overshoot == 1:
                self.p_pid = 1.2 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 2.0 * self.tau_ob
                self.d_pid = 0.4 * self.tau_ob
            elif self.overshoot == 2:
                self.p_pid = 1.4 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 1.3 * self.tau_ob
                self.d_pid = 0.5 * self.tau_ob

    def kopelovich_sharkov_method(self):
        if self.pid == 0:
            if self.overshoot == 0:
                self.p_pid = 0.6 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 0.8 * self.tau_ob + 0.5 * self.t1_ob
            elif self.overshoot == 1:
                self.p_pid = 0.7 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = self.tau_ob + 0.3 * self.t1_ob
            elif self.overshoot == 2:
                self.p_pid = 1.0 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = self.tau_ob + 0.35 * self.t1_ob
        elif self.pid == 1:
            if self.overshoot == 0:
                self.p_pid = 0.95 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 2.4 * self.tau_ob
                self.d_pid = 0.4 * self.tau_ob
            elif self.overshoot == 1:
                self.p_pid = 1.2 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 2.0 * self.tau_ob
                self.d_pid = 0.4 * self.tau_ob
            elif self.overshoot == 2:
                self.p_pid = 1.4 * self.t1_ob / (self.k_ob * self.tau_ob)
                self.i_pid = 1.3 * self.tau_ob
                self.d_pid = 0.5 * self.tau_ob

    def huang_method(self):
        if self.t2_ob > self.t1_ob:
            self.t1_ob, self.t2_ob = self.t2_ob, self.t1_ob
        if self.tau_ob / self.t1_ob < 0.1 or self.tau_ob / self.t1_ob > 10:
            self.p_pid, self.i_pid, self.d_pid = None, None, None
        if self.pid == 0:
            self.p_pid = (1 / self.k_ob) * ((-13.054 - 9.0916 * self.tau_ob / self.t1_ob + 2.6647 * self.t2_ob /
                                             self.t1_ob + 9.162 * self.tau_ob * self.t2_ob / self.t1_ob ** 2) +
                                            (0.3053 * (self.tau_ob / self.t1_ob) ** (-1.0169) + 1.1075 *
                                             (self.tau_ob / self.t1_ob) ** 3.5959 - 2.2927 * (self.tau_ob / self.t1_ob)
                                             ** 3.6843) + (-31.0306 * (self.t2_ob / self.t1_ob) ** 0.8476 - 13.0155 *
                                            (self.t2_ob / self.t1_ob) ** 2.6083 + 9.6899 * (self.t2_ob / self.t1_ob) **
                                            2.9049) + (-0.6418 * (self.t2_ob / self.tau_ob) + 18.9643 * (self.t2_ob /
                                            self.t1_ob) * (self.tau_ob / self.t1_ob) ** (-0.2016) - 39.7340 *
                                            (self.t2_ob / self.t1_ob) * (self.tau_ob / self.t1_ob) ** 1.3293) +
                                            (28.155 * (self.tau_ob / self.t1_ob) * (self.t2_ob / self.t1_ob) ** 0.801 -
                                             2.0067 * (self.tau_ob / self.t1_ob) * (self.t2_ob / self.t1_ob) ** 3.956) +
                                            (4.825 * exp(self.tau_ob / self.t1_ob) + 2.1137 * exp(self.t2_ob /
                                            self.t1_ob) + 8.4511 * exp(self.tau_ob * self.t2_ob / self.t1_ob ** 2)))
            self.i_pid = self.t1_ob * (0.9771 - 0.2492 * self.tau_ob / self.t1_ob + 0.8753 * self.t2_ob / self.t1_ob +
                                       3.4651 * (self.tau_ob / self.t1_ob) ** 2 - 3.8516 * self.tau_ob * self.t2_ob /
                                       self.t1_ob ** 2)
        elif self.pid == 1:
            self.p_pid = 0.589 / (self.k_ob * self.tau_ob) * (self.tau_ob / self.t2_ob) ** 0.003 * (0.0052 * self.t2_ob
                                  ** 2 / self.tau_ob + 0.898 * self.t2_ob + 0.4877 * self.tau_ob + self.t1_ob)
            self.i_pid = 0.0052 * self.t2_ob ** 2 / self.tau_ob + 0.898 * self.t2_ob + 0.4877 * self.tau_ob + self.t1_ob
            self.d_pid = self.t1_ob * (0.0052 * self.t2_ob ** 2 / self.tau_ob + 0.898 * self.t2_ob + 0.4877 *
                                       self.tau_ob) / (0.0052 * self.t2_ob ** 2 / self.tau_ob + 0.898 * self.t2_ob +
                                                       0.4877 * self.tau_ob + self.t1_ob)

    def skogestads_method(self):
        minimum = min(self.t1_ob, 4 * self.tau_ob)
        if minimum <= 0.01:
            self.p_pid, self.i_pid, self.d_pid = None, None, None
        if self.pid == 0 and self.order == "1st Order":  # Only for 1st order
            self.p_pid = self.t1_ob / (2 * self.k_ob * self.tau_ob)
            self.i_pid = minimum
        elif self.pid == 1 and self.order == "2nd Order T1 != T2":  # Only for 2nd order
            self.p_pid = self.t1_ob * (1 + self.t2_ob / minimum) / (2 * self.k_ob * self.tau_ob)
            self.i_pid = minimum * (1 + self.t2_ob / minimum)
            self.d_pid = self.t2_ob / (1 + self.t2_ob / minimum)
        else:
            pass

    def lambda_method(self):
        if self.lamb > 3 or self.lamb < 1:
            self.p_pid, self.i_pid, self.d_pid = None, None, None
        tcl = self.lamb * self.t1_ob
        if self.pid == 0:
            self.p_pid = self.t1_ob / (self.k_ob * (self.tau_ob + tcl))
            self.i_pid = self.t1_ob
        elif self.pid == 1:
            self.p_pid = (self.tau_ob / 2 + self.t1_ob) / (self.k_ob * (self.tau_ob / 2 + tcl))
            self.i_pid = self.t1_ob + self.tau_ob / 2
            self.d_pid = self.t1_ob * self.tau_ob / (2 * self.t1_ob + self.tau_ob)
        else:
            print(1111111111)

    def amigo_method(self):
        if self.pid == 0:
            self.p_pid = 0.15 / self.k_ob + (0.35 - self.tau_ob * self.t1_ob / (self.tau_ob + self.t1_ob) ** 2) * \
                         self.t1_ob / (self.tau_ob * self.k_ob)
            self.i_pid = 0.35 * self.tau_ob + (13 * self.tau_ob * self.t1_ob ** 2) / (self.t1_ob ** 2 + 12 *
                                               self.tau_ob * self.t1_ob + 7 * self.tau_ob ** 2)
        elif self.pid == 1:
            self.p_pid = (0.2 + 0.45 * self.t1_ob / self.tau_ob) / self.k_ob
            self.i_pid = self.tau_ob * (0.4 * self.tau_ob + 0.8 * self.t1_ob) / (self.tau_ob + 0.1 * self.t1_ob)
            self.d_pid = 0.5 * self.tau_ob * self.t1_ob / (0.3 * self.tau_ob + self.t1_ob)

    def ziegler_nichols(self):
        if self.pid == 0:
            if self.tau_ob / self.t1_ob < 1:
                self.p_pid, self.i_pid, self.d_pid = None, None, None
            self.p_pid = 0.9 * self.t1_ob / (self.k_ob * self.tau_ob)
            self.i_pid = 3.33 * self.tau_ob
        elif self.pid == 1:
            self.p_pid = 1.6 * self.t1_ob / (self.k_ob * self.tau_ob)
            self.i_pid = 2 * self.tau_ob
            self.d_pid = 0.5 * self.tau_ob

    def max_stability_method(self):
        if self.pid == 0:
            jpi = 2 / self.tau_ob + 1 / (2 * self.t1_ob) - ((2 / self.tau_ob ** 2) + (1 / (4 * self.t1_ob ** 2))) ** \
                  (1 / 2)
            self.p_pid = 1 / self.k_ob * ((self.tau_ob + 2 * self.t1_ob) * jpi - self.tau_ob * self.t1_ob * jpi ** 2 -
                                          1) * exp(-self.tau_ob * jpi)
            ki = 1 / self.k_ob * ((self.tau_ob + self.t1_ob) - self.tau_ob * self.t1_ob * jpi) * jpi ** 2 * exp(
                -self.tau_ob * jpi)
            self.i_pid = self.p_pid / ki
        elif self.pid == 1:
            jpid = 3 / self.tau_ob + 1 / (2 * self.t1_ob) - ((3 / self.tau_ob ** 2) + (1 / (4 * self.t1_ob ** 2))) ** \
                   (1 / 2)
            self.p_pid = 1 / self.k_ob * (-self.tau_ob ** 2 * self.t1_ob * jpid ** 3 + (self.tau_ob ** 2 + 3 *
                                          self.tau_ob * self.t1_ob) * jpid ** 2 - self.tau_ob * jpid - 1) * exp(
                                          -self.tau_ob * jpid)
            ki = 1 / (2 * self.k_ob) * (-self.tau_ob ** 2 * self.t1_ob * jpid ** 4 + (self.tau_ob ** 2 + 2 *
                                        self.tau_ob * self.t1_ob) * jpid ** 3 + 4 * self.t1_ob * jpid ** 2
                                        - 4 * jpid) * exp(-self.tau_ob * jpid)
            kd = 1 / (2 * self.k_ob) * (self.tau_ob ** 2 * (jpid - self.t1_ob * jpid ** 2) - 2 * self.tau_ob * (1 - 2 *
                                        self.t1_ob * jpid) - 2 * self.t1_ob) * exp(-self.tau_ob * jpid)
            self.i_pid = self.p_pid / ki
            self.d_pid = kd / self.p_pid


if __name__ == "__main__":
    obj = PID_Object('first', 1, 2, 3)
    obj.pid = 1
    obj.optimal_module_method()
    print(obj)

    obj2 = PID_Object('second', 2, 3, 4, 5)
    obj2.pid = 1
    obj2.aperiodic_stability_method()
    print(obj2)

    obj3 = PID_Object('second', 1, 2, 3, 4)
    obj3.pid = 0
    obj3.overshoot = 0
    obj3.disturbance = 0
    obj3.coon_method()
    print(obj3)

    obj4 = PID_Object('second', 1, 2, 3, 4)
    obj4.pid = 0
    obj4.overshoot = 0
    obj4.disturbance = 0
    obj4.kopelovich_method()
    print(obj4)
