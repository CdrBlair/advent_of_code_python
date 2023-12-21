import os
import re
import sys
import time
from collections import deque
from functools import cache
from math import lcm

from numpy import rec


# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/pulses.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    # Low == False, Off == False
    modules = {}
    for line in lines:
        line = line.strip()
        splitted = line.split("->")
        if splitted[0].strip() == "broadcaster":
            reciever = splitted[1].strip().split(",")
            reciever = tuple([r.strip() for r in reciever])
            modules["broadcaster"] = (reciever, "b", None, {})
        elif splitted[0].__contains__("%"):
            name = splitted[0].strip()[1:]
            reciever = splitted[1].strip().split(",")
            reciever = tuple([r.strip() for r in reciever])
            modules[name] = (reciever, "f", False, {})
        elif splitted[0].__contains__("&"):
            name = splitted[0].strip()[1:]
            reciever = splitted[1].strip().split(",")
            reciever = tuple([r.strip() for r in reciever])
            modules[name] = (reciever, "c", False, {})

    toAdd = []
    for name, module in modules.items():
        for reciever in module[0]:
            if reciever not in modules:
                toAdd.append(reciever)
            if reciever in modules and modules[reciever][1] == "c":
                modules[reciever][3][name] = False

    for name in toAdd:
        modules[name] = (tuple(), "o", None, {})

    for module in modules:
        # convert dict to tuple
        modules[module] = (
            modules[module][0],
            modules[module][1],
            modules[module][2],
            tuple(modules[module][3].items()),
        )

    modulesPart2 = modules.copy()
    buttonPressed = 1000
    highPulse = 0
    lowPulse = 0
    firstRK = 0
    for i in range(buttonPressed):
        lowPulse += 1
        stack = deque((("broadcaster", modules["broadcaster"], False, ""),))
        while stack:
            name, state, pulse, sender = stack.popleft()
            # print the types of the inputs
            # print(name, state, pulse, sender)
            pulseBefore = pulse
            pulse, state = calculatePulse(name, modules[name], pulse, sender)
            # print("Pulse: ", pulse)
            # print("State: ", state)

            if pulse != None:
                if pulse == True:
                    highPulse += len(state[0])
                else:
                    lowPulse += len(state[0])
                for reciever in state[0]:
                    stack.append((reciever, modules[reciever], pulse, name))
                modules[name] = state
            elif name == "rx":
                modules[name] = state

    print("High pulse: ", highPulse)
    print("Low pulse: ", lowPulse)
    print("Total pulse: ", highPulse + lowPulse)
    print("Low and High multiplied: ", lowPulse * highPulse)
    endtimep1 = time.time()
    print("Part 1 time: ", endtimep1 - start_time)
    print(" Time in ms: ", (endtimep1 - start_time) * 1000)

    # # clear cache
    # calculatePulse.cache_clear()
    # highPulse = 0
    # lowPulse = 0
    # buttonsPressed = 0
    # while modulesPart2["rx"][2] == None:
    #     buttonsPressed += 1
    #     lowPulse += 1
    #     stack = deque((("broadcaster", modulesPart2["broadcaster"], False, ""),))
    #     while stack:
    #         name, state, pulse, sender = stack.popleft()
    #         # print the types of the inputs
    #         # print(name, state, pulse, sender)
    #         pulseBefore = pulse
    #         pulse, state = calculatePulse(name, state, pulse, sender)
    #         # print("Pulse: ", pulse)
    #         # print("State: ", state)

    #         if pulse != None:
    #             if pulse == True:
    #                 highPulse += len(state[0])
    #             else:
    #                 lowPulse += len(state[0])
    #             for reciever in state[0]:
    #                 stack.append((reciever, modulesPart2[reciever], pulse, name))
    #             modulesPart2[name] = state
    #         elif name == "rx" and not pulseBefore:
    #             print("rx", state)
    #             print("pulse", pulseBefore)
    #             modulesPart2[name] = state

    # print("Buttons pressed: ", buttonsPressed)

    # Part2 Alternative
    # Find parent of rx
    for name, module in modulesPart2.items():
        if "rx" in module[0]:
            parentModule = name
            break
    grandParentModules = []
    for name, module in modulesPart2.items():
        if parentModule in module[0]:
            grandParentModules.append(name)
    grandParentFirstHigh = {}
    for name in grandParentModules:
        grandParentFirstHigh[name] = 0

    calculatePulse.cache_clear()
    buttonsPressed = 0
    while not all(grandParentFirstHigh.values()):
        buttonsPressed += 1
        stack = deque((("broadcaster", modulesPart2["broadcaster"], False, ""),))
        while stack:
            name, state, pulse, sender = stack.popleft()
            # print the types of the inputs
            # print(name, state, pulse, sender)
            # if name == parentModule and pulse:
            #     print("parentModule", name)
            #     print("pulse", pulse)
            #     print("buttonsPressed", buttonsPressed)
            if (
                name in grandParentModules
                and not pulse
                and not grandParentFirstHigh[name]
            ):
                grandParentFirstHigh[name] = buttonsPressed

            pulse, state = calculatePulse(name, modulesPart2[name], pulse, sender)
            # print("Pulse: ", pulse)
            # print("State: ", state)

            if pulse != None:
                if pulse == True:
                    highPulse += len(state[0])
                else:
                    lowPulse += len(state[0])
                # print("state[0]", state[0])
                for reciever in state[0]:
                    stack.append((reciever, modulesPart2[reciever], pulse, name))

                modulesPart2[name] = state

    print("grandParentFirstHigh: ", grandParentFirstHigh)
    print("LCM of grandParentFirstHigh: ", lcm(*list(grandParentFirstHigh.values())))
    endTimeP2 = time.time()
    print("Part 2 time: ", endTimeP2 - endtimep1)
    print(" Time in ms: ", (endTimeP2 - endtimep1) * 1000)
    print("Total time: ", endTimeP2 - start_time)


# False low, True high


@cache
def calculatePulse(name, state, pulse, sender):
    state = (state[0], state[1], state[2], dict(state[3]))
    if state[1] == "o":
        return (None, (state[0], state[1], state[2], tuple(state[3].items())))
    if name == "broadcaster":
        return (False, (state[0], state[1], True, tuple(state[3].items())))
    elif state[1] == "f":
        if pulse == True:
            # Nothing happens if pulse is high
            return (None, (state[0], state[1], state[2], tuple(state[3].items())))
        else:
            turnedOn = not state[2]
            newState = (state[0], state[1], turnedOn, tuple(state[3].items()))
            return (newState[2], newState)
    else:
        state[3][sender] = pulse

        for s in state[3].values():
            if s == False:
                return (True, (state[0], state[1], state[2], tuple(state[3].items())))

        return (False, (state[0], state[1], state[2], tuple(state[3].items())))


if __name__ == "__main__":
    main()
