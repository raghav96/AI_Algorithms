from hmm import HMM
import numpy as np

# Viterbi algorithm
def viterbi(hmm, initial_dist, emissions):
    # Set the initial state probabilities by getting the emission probability 
    # of the first element and multiplying it by initial probabilities
    state_probs = hmm.emission_prob(emissions[0]) * initial_dist
    # stack to hold the maximum transition probabilities
    max_stack = []

    # start from the second state to figure out best transitions in each state.
    for emission in emissions[1:]:
        # Calculating the transition probabilities using
        # cross pdt of transition probabiltiies and transpose of state probs
        transition_probs = hmm.t_probs * np.vstack(state_probs)

        # Calculating the ma
        max_trans_index = np.argmax(transition_probs, axis=0)
        # Updating the state probabilities for the new state
        state_idxs = np.array([ a for a in range(hmm.num_states)])

        # Updating the state probabilities using the emission probabilities and cross pdt
        # with transition probabilities of all the states
        state_probs = hmm.emission_prob(emission) * transition_probs[max_trans_index, state_idxs]

        # append the maximum transition indexes through the max stack
        max_stack.append(max_trans_index)

    # Initialize the best path using index of the last transition with the best probability
    best_path = [np.argmax(state_probs)]

    # Pop the elements from the maximum transition probabilty stack to build best path
    while max_stack:
        max_transitions = max_stack.pop()
        #Backtracking transitions from the current_state to calculate prev_state
        prev_state = max_transitions[best_path[-1]]

        # Adding state to best path
        best_path.append(prev_state)

    # Reverse to return path from start to finish
    best_path.reverse()

    return best_path

#examples
#from Wikipedia
test_transition_probs = np.array([[0.7, 0.4], [0.3, 0.6]]) #0=Healthy, 1=Fever
test_emissions = [3, 2, 1, 0]
test_emission_probs = np.array([[0.1, 0.4, 0.2, 0.3], [0.3, 0.1, 0.1, 0.5]]) #0=Dizzy, 1=Cold, 2=Normal #3=Weak
test_initial_dist = np.array([[0.6, 0.4]])
test_hmm = HMM(test_transition_probs, test_emission_probs)

if __name__ == "__main__":
    print "Best path in 2-state HMM with given test transitions, emissions, and initial dist"
    print(viterbi(test_hmm, test_initial_dist, test_emissions))