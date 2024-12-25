import os
import time
import itertools



# Main method
def main():
    start_time = time.time()

    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/wires.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    readInitialInputs = False
    initialInputs = {}
    # key: outwire value (in1, in2, gatetype, currentvalue)
    gates = {}
    outPutWires = []
    for line in lines:
        if line.strip() == "":
            readInitialInputs = True
            continue
        if not readInitialInputs:
            line = line.strip()
            wire, value = line.split(":")
            initialInputs[wire] = int(value.strip())
        else:
            line = line.strip()
            gatedef , outwire = line.split("->")
            in1, gateType, in2 = gatedef.strip().split(" ")
            gates[outwire.strip()] = (in1.strip(), gateType.strip(), in2.strip(), None)
            if outwire.strip().startswith("z"):
                outPutWires.append(outwire.strip())
    #print(initialInputs)
    #print(gates)
    #print(outPutWires)
    #reveresed
    gatesP2 = gates.copy()
    outPutWires = sorted(outPutWires, reverse=True)
    #print(outPutWires)
    outPutValues = {}
    for wire in outPutWires:
        outPutValues[wire] = findValue(wire, initialInputs, gates, outPutValues)
    #print(outPutValues)
    
    result = ''
    for wire in outPutWires:
        result += str(outPutValues[wire])
    #print(result)
    intValue = int(result, 2)
    print(intValue)
    end_time = time.time()
    print("Part 1 took: ", end_time - start_time)
    print("Part 1 took in ms: ", (end_time - start_time) * 1000)

    # Assuming we have a regular bid adder check for obvious errors in cabeling
    possibleWrongWires = []
    for wire in gatesP2:
        # final output can only come from xor gate or and gate if both inputs are x and y
        in1, gateType, in2, currentValue = gatesP2[wire]
        if wire.startswith("z"):
            if gateType != "XOR":
                if wire == "z45" and gateType == "OR": #Most significant bit ignore if OR gate for now
                    continue
                print('hit rule1')
                possibleWrongWires.append(wire)
        #XOR are not going to OR
        if gateType == "XOR":
            for wire2 in gatesP2:
                in1_2, gateType_2, in2_2, currentValue_2 = gatesP2[wire2]
                if gateType_2 == "OR" and (in1_2 == wire or in2_2 == wire):
                    print('hit rule2')
                    possibleWrongWires.append(wire)
                #if XOR goes to XOR the wire must be an output wire (found this rule after the manual approach, this was all that was missing -.-)
                if gateType_2 == "XOR" and (in1 == wire2 or in2 == wire2) and not wire.startswith("z"):
                    print('hit rule2.1')
                    possibleWrongWires.append(wire)
        # OR ar not poiting to other ORs
        if gateType == "OR":
            for wire2 in gatesP2:
                in1_2, gateType_2, in2_2, currentValue_2 = gatesP2[wire2]
                if gateType_2 == "OR" and (in1_2 == wire or in2_2 == wire):
                    print('hit rule3')
                    possibleWrongWires.append(wire)
        # Assuming it starts with a half adder ANDs only go to OR except for the first one
        if gateType == "AND":
            for wire2 in gatesP2:
                in1_2, gateType_2, in2_2, currentValue_2 = gatesP2[wire2]
                if gateType_2 != "OR" and (in1_2 == wire or in2_2 == wire) and not (in1 == "x00" and in2 == "y00"): # Peek the input for the order of the last and not ;)
                    print('hit rule4')
                    possibleWrongWires.append(wire)
    possibleWrongWires = list(set(possibleWrongWires))
    print(possibleWrongWires)
    #print(len(possibleWrongWires))
    #find last Wrong wire.... did it manually
    #changes = [('vmv', 'z07'),('kfm','z20'),('hnv','z28'),('tqr','hth')]
    possiblePairs = list(itertools.combinations(possibleWrongWires, 2))
    print(len(possiblePairs))
    sets = list(itertools.combinations(possiblePairs, 4))
    print(len(sets))    

    validSets = []
    for setofPairs in sets:
        allelements = set(itertools.chain(*setofPairs))
        if len(allelements) == 8:
            validSets.append(setofPairs)
    print(len(validSets))
    

   
    xList = []
    yList = []
    
    for value in initialInputs:
        if value.startswith("x"):
            xList.append(value)
        if value.startswith("y"):
            yList.append(value)
    xList = sorted(xList, reverse=True)
    yList = sorted(yList, reverse=True)

    x=''
    y=''
    for wire in xList:
        x += str(initialInputs[wire])
    for wire in yList:
        y += str(initialInputs[wire])


    z = int(x,2 ) + int(y,2)
    z = bin(z)[2:]
    

    print(x)
    print(y)
    print("Calculated z:",z)
    changeList = []
    for changes in validSets:
        tempGates = gatesP2.copy()
        changeList = []
        for change in changes:
            changeList.append(change[0])
            changeList.append(change[1])
            tempGate = tempGates[change[0]]
            tempGates[change[0]] = tempGates[change[1]]
            tempGates[change[1]] = tempGate
        

        outPutValues = {}
        for wire in outPutWires:
            outPutValues[wire] = findValueP2(wire, initialInputs, tempGates, 0)
            if outPutValues[wire] is None:
                break
        #print(outPutValues)
        if len(outPutValues) != len(outPutWires):
            continue
        result = ''
        for wire in outPutWires:
            result += str(outPutValues[wire])
        print(result)
        if result == z:    
            print("corrected Adder: ",result)
            intValue = int(result, 2)
            print(intValue)
            changeList.sort()
            print(','.join(changeList)) 
            break

    end_timeP2 = time.time()
    print("Part 2 took: ", end_timeP2 - start_time)
    print("Part 2 took in ms: ", (end_timeP2 - start_time) * 1000)

    
 
        

def findValueP2(wire, initialInputs, gates, depth):
    if depth > 100:
        return None
    if wire in initialInputs:
        return initialInputs[wire]
    in1, gateType, in2, currentValue = gates[wire]
    if gateType == "AND":
        if currentValue is None:
            in1 = findValueP2(in1, initialInputs, gates, depth+1)
            in2 = findValueP2(in2, initialInputs, gates, depth+1)
            if in1 is None or in2 is None:
                return None
            gates[wire] = (in1, gateType, in2, in1 & in2)
            return in1 & in2
        else:
            return currentValue
    elif gateType == "OR":
        if currentValue is None:
            in1 = findValueP2(in1, initialInputs, gates, depth+1)
            in2 = findValueP2(in2, initialInputs, gates, depth+1)
            if in1 is None or in2 is None:
                return None
            gates[wire] = (in1, gateType, in2, in1 | in2)
            return in1 | in2
        else:
            return currentValue
    elif gateType == "XOR":
        if currentValue is None:
            in1 = findValueP2(in1, initialInputs, gates, depth+1)
            in2 = findValueP2(in2, initialInputs, gates, depth+1)
            if in1 is None or in2 is None:
                return None
            gates[wire] = (in1, gateType, in2, in1 ^ in2)
            return in1 ^ in2
        else:
            return currentValue



def findValue(wire, initialInputs, gates, outPutValues):
    if wire in initialInputs:
        return initialInputs[wire]
    in1, gateType, in2, currentValue = gates[wire]
    if gateType == "AND":
        if currentValue is None:
            in1 = findValue(in1, initialInputs, gates, outPutValues)
            in2 = findValue(in2, initialInputs, gates, outPutValues)
            gates[wire] = (in1, gateType, in2, in1 & in2)
            return in1 & in2
        else:
            return currentValue
    elif gateType == "OR":
        if currentValue is None:
            in1 = findValue(in1, initialInputs, gates, outPutValues)
            in2 = findValue(in2, initialInputs, gates, outPutValues)
            gates[wire] = (in1, gateType, in2, in1 | in2)
            return in1 | in2
        else:
            return currentValue
    elif gateType == "XOR":
        if currentValue is None:
            in1 = findValue(in1, initialInputs, gates, outPutValues)
            in2 = findValue(in2, initialInputs, gates, outPutValues)
            gates[wire] = (in1, gateType, in2, in1 ^ in2)
            return in1 ^ in2
        else:
            return currentValue
      

if __name__ == "__main__":
    main()
    
    