import os
import time


# Main method
def main():
 
    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2024/testequations.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()
    
    equations = []
    for line in lines:
        splitted = line.split(":")
        equations.append((int(splitted[0]), [int(x) for x in splitted[1].strip().split(" ")]))

    listTrueequations = []
    for equation in equations:
        if recursiveAddOrMulti(0, equation[1], equation[0]) == equation[0]:
            listTrueequations.append(equation)
    
    #print("End", listTrueequations)

    print(sum([x[0] for x in listTrueequations]))
    endtime = time.time()
    print("Time taken;" , endtime - start_time)
    print("Time taken in ms;", (endtime - start_time) * 1000)
    

    listTrueConEquations = []
    for equation in equations:
        #starttimeeq = time.time()
        if recursiveAddOrMultiORCon(0, equation[1], equation[0]) == equation[0]:
            listTrueConEquations.append(equation)
        # if (time.time() - starttimeeq) * 1000 > 10:
        #     print(equation)
        #     print("Time taken for equation in ms;", (time.time() - starttimeeq) * 1000)
    
    #print("End", listTrueConEquations)
    print(sum([x[0] for x in listTrueConEquations]))

    endtimeP2 = time.time() 
    print("Time taken;" , endtimeP2 - endtime)
    print("Time taken in ms;", (endtimeP2 - endtime) * 1000)


def recursiveAddOrMulti(currentSum, currentList, target):
    if currentSum >  target:
        return -1
    if len(currentList) == 1:
        
        if currentSum + currentList[0] == target or currentSum * currentList[0] == target:
            #print("A",currentSum, currentList[0], target)
            return target
        else:
            return -1
    else:
        if currentSum == 0:
            multiValue = 1
        else:
            multiValue = currentSum
        # sumPath = recursiveAddOrMulti(currentSum + currentList[0], currentList[1:], target)
        # multiPath = recursiveAddOrMulti(multiValue * currentList[0], currentList[1:], target)
        if recursiveAddOrMulti(currentSum + currentList[0], currentList[1:], target) == target or recursiveAddOrMulti(multiValue * currentList[0], currentList[1:], target) == target:
           # print("B",currentSum, currentList[0], target)
            return target
        else:
            return -1
   
def recursiveAddOrMultiORCon(currentSum, currentList, target):
    if currentSum >  target:
        return -1
    if len(currentList) == 1:
        
        if currentSum + currentList[0] == target or currentSum * currentList[0] == target or int(str(currentSum) + str(currentList[0])) == target:
            #if int(str(currentSum) + str(currentList[0])) == target:
                #print("A",currentSum, currentList[0], target)
            return target
        else:
            return -1
    else:
        if currentSum == 0:
            multiValue = 1
            convalue = ""
        else:
            multiValue = currentSum
            convalue = str(currentSum)
        # sumPath = recursiveAddOrMultiORCon(currentSum + currentList[0], currentList[1:], target)
        # multiPath = recursiveAddOrMultiORCon(multiValue * currentList[0], currentList[1:], target)
        # conPath = recursiveAddOrMultiORCon(int(convalue + str(currentList[0])), currentList[1:], target)
        if  recursiveAddOrMultiORCon(multiValue * currentList[0], currentList[1:], target) == target or recursiveAddOrMultiORCon(currentSum + currentList[0], currentList[1:], target) == target or recursiveAddOrMultiORCon(int(convalue + str(currentList[0])), currentList[1:], target) == target:
           # print("B",currentSum, currentList[0], target)
            return target
        else:
            return -1



if __name__ == "__main__":
    main()

