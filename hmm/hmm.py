class HMM:
    #constructor
    #t_probs[i, j] is the probability of transitioning to state i from state j
    #e_probs[i, j] is the probability of emitting emission j while in state i
    def __init__(self, transition_probs, emission_probs):
        self.t_probs = transition_probs
        self.e_probs = emission_probs

    #accessors
    def emission_prob(self, emission):
        return self.e_probs[:, emission]

    @property
    def num_states(self):
        return self.t_probs.shape[0]

    @property
    def transition_probs(self):
        return self.t_probs