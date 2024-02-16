import numpy as np
import random
from FAdo.fa import *
from graphviz import Digraph
import json
import pandas as pd

class FSM(object):

    def __init__(self, numStates, numAlphabet):

        self.states = self.initialize_states(numStates)
        self.alphabets = self.initialize_alphabets(numAlphabet)
        self.accepting_states = self.initialize_terminals(numStates)
        self.initial_state = self.states[0]
        self.transitions = self.initialize_transitions()
    
    def get_symbols(self, start="0", end="1"):

        syms = []
        for i in range(len(self.transitions)):
            if self.transitions[i]['fromState'] == start and self.transitions[i]['toState'] == end:
                syms.append(self.transitions[i]['symbol'])
        
        return syms

    def initialize_states(self, numStates):

        states = []

        for i in range(numStates):
            states.append("s" + str(i))
        
        return states

    def initialize_terminals(self, numStates):
        
        n = random.randint(1, numStates)
        accepts = list(random.sample(self.states, n))

        return accepts


    def initialize_alphabets(self, numAlphabet):
        
        alphabets = []

        if numAlphabet > 26:
            alphabets = ["a" + str(i) for i in range(numAlphabet)]
        else:
            alphabets = "abcdefghijklmnopqrstuvwxyz"[:numAlphabet]

        return alphabets
    
    def initialize_transitions(self):

        transitions = []

        for i in range(len(self.states)):
            for j in range(len(self.alphabets)):
        
                toStates = []
                for k in range(len(self.states)):
                    
                    if len(toStates) < 1:

                        diff = len(self.states) - k
                        diff = 1/diff

                        if random.random() < diff:
                            toStates.append(self.states[k])

                transitions.append({"fromState" : self.states[i], "symbol" : self.alphabets[j], "toStates" : toStates})

        return transitions

    def getTransitionMatrix(self):

        trans_mat = dict()

        for alphabet in self.alphabets:
            toState = []
            fromState = []
            for trans in self.transitions:
                if alphabet == trans["symbol"]:
                    toState.append(trans["toStates"][0])
                    fromState.append(trans["fromState"])

            trans_mat.update({alphabet: pd.Series(toState, index=fromState)})

        return pd.DataFrame(trans_mat), self.initial_state, self.accepting_states
    
    def serialize(self):
        # Convert the fsm instance into a dictionary
        fsm_dict = {
            "states": self.states,
            "alphabets": self.alphabets,
            "accepting_states": self.accepting_states,
            "initial_state": self.initial_state,
            "transitions": self.transitions,
        }
        return json.dumps(fsm_dict)
    
    @classmethod
    def deserialize(cls, json_string):
        # Convert the JSON string back into a dictionary
        fsm_dict = json.loads(json_string)
        # Create a new fsm instance
        fsm_instance = cls(len(fsm_dict["states"]), len(fsm_dict["alphabets"]))
        # Set the attributes of the fsm instance
        fsm_instance.states = fsm_dict["states"]
        fsm_instance.alphabets = fsm_dict["alphabets"]
        fsm_instance.accepting_states = fsm_dict["accepting_states"]
        fsm_instance.initial_state = fsm_dict["initial_state"]
        fsm_instance.transitions = fsm_dict["transitions"]
        return fsm_instance

    def convertToString(self):

        metadata = "#fsm: "

        metadata += "#states{"
        for i in range(len(self.states)):
            metadata += self.states[i]

        metadata += "}#initial{"

        metadata += self.initial_state

        metadata += "}#accepting{"
        for i in range(len(self.accepting_states)):
            metadata += self.accepting_states[i]
        
        metadata += "}#alphabets{"
        for i in range(len(self.alphabets)):
            metadata += self.alphabets[i]

        metadata += "}#transitions"
        for i in range(len(self.transitions)):
            metadata += "{"
            metadata += self.transitions[i]['fromState'] + ":" + self.transitions[i]['symbol'] + ">"
            for j in range(len(self.transitions[i]['toStates'])):
                metadata += self.transitions[i]['toStates'][j]
            metadata += "}"

        return metadata
    
    def checkString(self, input):

        currentState = self.initial_state
        trail = []
        observed_states = []
        result = "reject"

        for i in range(len(input)):
            for trans in self.transitions:
                if trans['symbol'] == input[i] and trans['fromState'] == currentState:
                    observed_states.append(currentState)
                    currentState = trans['toStates'][0]
                    trail.append(trans['symbol'])
                    break
        
        observed_states.append(currentState)

        if currentState in self.accepting_states:
            result = "accept"

        return result, trail, observed_states, currentState
    
    def randomStringInLanguage(self):

        if len(self.accepting_states) == 0:
            return None

        currentState = self.accepting_states[int(np.floor(random.random()*len(self.accepting_states)))]
        trail = []

        while True:
            if currentState == self.initial_state:
                if np.round(random.random()):
                    break

            transitions = []
            
            for i in range(len(self.transitions)):
                if self.transitions[i]['toStates'][0] == currentState:
                    transitions.append(self.transitions[i])

            if len(transitions) == 0:
                break

            transition = transitions[int(np.floor(random.random()*len(transitions)))]

            trail.append(transition['symbol'])
            currentState = transition['fromState']

        trail.reverse()

        return trail
    
    def randomStringNotInLanguage(self):

        nonAcceptingStates = []

        for i in range(len(self.states)):
            if self.states[i] not in self.accepting_states:
                nonAcceptingStates.append(self.states[i])

        if len(nonAcceptingStates) == 0:
            return ""

        currentState = nonAcceptingStates[int(np.floor(random.random()*len(nonAcceptingStates)))]
        trail = []

        while True:
            if currentState == self.initial_state:
                if np.round(random.random()):
                    break

            transitions = []

            for i in range(len(self.transitions)):
                if self.transitions[i]['toStates'][0] == currentState:
                    transitions.append(self.transitions[i])

            if len(transitions) == 0:
                break
            
            transition = transitions[int(np.floor(random.random()*len(transitions)))]

            trail.append(transition['symbol'])
            currentState = transition['fromState']

        trail.reverse()

        return trail
    
    def getReachableStates(self):
        unprocessedStates = [self.initial_state]
        reachableStates = [self.initial_state]

        while len(unprocessedStates) != 0:
            currentState = unprocessedStates.pop()

            for i in range(len(self.transitions)):
                transition = self.transitions[i]

                if currentState == transition['fromState']:
                    if transition['toStates'][0] not in reachableStates:
                        reachableStates.append(transition['toStates'][0])
                        if transition['toStates'][0] not in unprocessedStates:
                            unprocessedStates.append(transition['toStates'][0])
                  
        return reachableStates

    def removeUnreachableStates(self):
        reachableStates = self.getReachableStates()
        states = []
        acceptingStates = []
        transitions = []

        for i in range(len(self.states)):
            if self.states[i] in reachableStates:
                states.append(self.states[i])

        for i in range(len(self.accepting_states)):
            if self.accepting_states[i] in reachableStates:
                acceptingStates.append(self.accepting_states[i])

        for i in range(len(self.transitions)):
            if self.transitions[i]['fromState'] in reachableStates:
                transitions.append(self.transitions[i])

        return states, acceptingStates, transitions
    


def visualize_dfa(dfa):
    dot = Digraph()

    # Add states
    for state in dfa.States:
        if state in dfa.Final:
            dot.node(str(state), shape='doublecircle')
        else:
            dot.node(str(state), shape='circle')

    # Mark the initial state
    dot.node("", shape='plaintext')
    dot.edge("", str(dfa.Initial))

    # Add transitions
    for start_state, transitions in dfa.delta.items():
        for input_char, end_state in transitions.items():
            dot.edge(str(start_state), str(end_state), label=input_char)

    # Display the graph in the notebook
    return dot


def createDFA(numStates, numAlphabet):
    dfa = FSM(numStates, numAlphabet)
    states, accepts, trans = dfa.removeUnreachableStates()
    dfa.states = states
    dfa.accepting_states = accepts
    dfa.transitions = trans
    dfa.accepting_states = dfa.initialize_terminals(len(dfa.states))
    return dfa


def simple_test():
    f = createDFA(6, 5)

    dfa = DFA()
    for state in f.states:
        dfa.addState(state)
    for trans in f.transitions:
        for symbol, dest_state in trans.items():
            if len(trans['toStates']) == 1:
                dfa.addTransition(trans['fromState'], trans['symbol'], trans['toStates'][0])
            else:
                for i in range(len(trans['toStates'])):
                    dfa.addTransition(trans['fromState'], trans['symbol'], trans['toStates'][i])

    dfa.setInitial(f.initial_state)
    for state in f.accepting_states:
        dfa.addFinal(state)

    dfa_dot = visualize_dfa(dfa)

# simple_test()
    

# fs = """{"states": ["s0", "s2", "s3"], "alphabets": "abcd", "accepting_states": ["s2", "s0"], "initial_state": "s0", "transitions": [{"fromState": "s0", "symbol": "a", "toStates": ["s2"]}, {"fromState": "s0", "symbol": "b", "toStates": ["s0"]}, {"fromState": "s0", "symbol": "c", "toStates": ["s3"]}, {"fromState": "s0", "symbol": "d", "toStates": ["s3"]}, {"fromState": "s2", "symbol": "a", "toStates": ["s0"]}, {"fromState": "s2", "symbol": "b", "toStates": ["s0"]}, {"fromState": "s2", "symbol": "c", "toStates": ["s0"]}, {"fromState": "s2", "symbol": "d", "toStates": ["s3"]}, {"fromState": "s3", "symbol": "a", "toStates": ["s2"]}, {"fromState": "s3", "symbol": "b", "toStates": ["s3"]}, {"fromState": "s3", "symbol": "c", "toStates": ["s0"]}, {"fromState": "s3", "symbol": "d", "toStates": ["s0"]}]}"""
# d = FSM.deserialize(fs)
# gg = d.checkString("ab")

# print("T")
