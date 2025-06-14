"""
Clinical Trials Driver Script class

Raluca Cobzaru (c) 2018

"""

from collections import namedtuple
import numpy as np
import scipy
import pandas as pd
from ClinicalTrialsModel import ClinicalTrialsModel
from ClinicalTrialsPolicy import ClinicalTrialsPolicy
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    time_total = time.time()
    np.random.seed(2345678173)
    # initializes a policy object and a model object, then runs the policy on the model
    policy_names = ["model_A", "model_B", "model_C", "model_C_extension"]
    state_names = ["potential_pop", "success", "failure", "l_response"]
    # extracts data from given data set; defines initial state
    file = "Parameters.xlsx"
    raw_data = pd.ExcelFile(file)
    data = raw_data.parse("Parameters")
    initial_state = {
        "potential_pop": float(data.iat[0, 0]),
        "success": data.iat[1, 0],
        "failure": float(data.iat[2, 0]),
        "l_response": float(data.iat[3, 0]),
        "theta_stop_low": data.iat[4, 0],
        "theta_stop_high": data.iat[5, 0],
        "alpha": data.iat[6, 0],
        "K": int(data.iat[7, 0]),
        "N": int(data.iat[8, 0]),
        "trial_size": int(data.iat[9, 0]),
        "patient_cost": data.iat[10, 0],
        "program_cost": data.iat[11, 0],
        "success_rev": data.iat[12, 0],
        "sampling_size": int(data.iat[13, 0]),
        "enroll_min": int(data.iat[14, 0]),
        "enroll_max": int(data.iat[15, 0]),
        "enroll_step": int(data.iat[16, 0]),
        "H": int(data.iat[17, 0]),
        "true_l_response": data.iat[18, 0],
        "true_succ_rate": data.iat[19, 0],
    }
    model_name = data.iat[20, 0]
    numIterations = int(data.iat[21, 0])

    decision_names = ["enroll", "prog_continue", "drug_success"]

    ################################################################
    # Solution Q5
    theta_list = list(np.arange(0.77, 0.79, 0.005))
    theta_avg = []
    for theta in theta_list:
        initial_state.update({"theta_stop_low": theta})
        avg_policy_value = 0
        for i in range(0, numIterations):

            M = ClinicalTrialsModel(state_names, decision_names, initial_state, False)
            P = ClinicalTrialsPolicy(M, policy_names)
            t = 0
            stop = False
            policy_info = {
                "model_A": [-1, stop],
                "model_B": [-1, stop],
                "model_C": [-1, stop],
                "model_C_extension": [-1, stop],
            }
            policy_value = P.run_policy(policy_info, model_name, t)
            avg_policy_value += policy_value
            print(
                "Finished run policy for iteration {} - Value: {} and Avg_value: {:,}".format(
                    i, policy_value, avg_policy_value / (i + 1)
                )
            )

        avg_policy_value = avg_policy_value / numIterations
        print(
            "Theta {} - Average values after {} iterations is {:,}".format(
                initial_state["theta_stop_low"], numIterations, avg_policy_value
            )
        )
        theta_avg.append(avg_policy_value)

    print(theta_list)
    print(theta_avg)
    plt.plot(theta_list, theta_avg, "bo")
    plt.show()
    # End Solution Q5
    ###############################################################

    print("Total elapsed time {:.2f} secs".format(time.time() - time_total))

    pass
