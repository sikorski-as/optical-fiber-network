import Parameters


def get_amount_of_transponder_used(transponders_used):

    amount_of_transponder_types = len(Parameters.Parameters.transponders_cost)
    return [sum(t_list[i] for t in transponders_used.values() for t_list in t) for i in range(amount_of_transponder_types)]
