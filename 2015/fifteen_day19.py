import os
import time
import re
from random import shuffle


# Main method
def main():
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2015/reindeer_med.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    replacements= {}
    medicineStart = ""

    doneReplacement = False
    for line in lines:
        if line.strip() == "":
            doneReplacement = True
        elif doneReplacement:
            medicineStart = line.strip()
        else:
            line = line.strip().split(" => ")
            if line[0] in replacements:
                replacements[line[0].strip()].append(line[1].strip())
            else:
                replacements[line[0].strip()] = [line[1].strip()]
    print(replacements)
    print(medicineStart)

    possibleMolecules = set()
    for key in replacements:
        keyOccurencesIndex = [m.start() for m in re.finditer(key, medicineStart)]
        for index in keyOccurencesIndex:
            for replacement in replacements[key]:
                possibleMolecules.add(medicineStart[:index] + replacement + medicineStart[index+len(key):])
    
    print(len(possibleMolecules))

    replacementsList = []
    for key in replacements:
        for replacement in replacements[key]:
            replacementsList.append((key, replacement))
    
    target = medicineStart
    steps = 0

    while target != "e":
        temp = target
        for key, replacement in replacementsList:
            if replacement not in target:
                continue
            target = target.replace(replacement, key, 1)
            steps += 1
        
        if temp == target:
            target = medicineStart
            steps = 0
            shuffle(replacementsList)
    
    print(steps)
   
        

if __name__ == "__main__":
    main()


