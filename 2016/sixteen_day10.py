import os
import time


# Main method
def main():

    start_time = time.time()
    # Open file
    script_dir = os.path.dirname(__file__)
    rel_path = "../inputs/2016/botinstructions.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "r") as file:
        lines = file.readlines()

    bots = {}
    # bot = {botid: (#ofchips, chip1, chip2, lowKind, lowId, highKind, highId)}
    for line in lines:
        if "value" in line:
            splitted = line.strip().split()
            value = int(splitted[1])
            botid = int(splitted[-1])
            if botid not in bots:
                bots[botid] = (1, value, None, None, None, None, None)
            else:
                chips, value1, value2, lowKind, lowId, highKind, highId = bots[botid]
                if value1 is None:
                    bots[botid] = (1, value, None, lowKind, lowId, highKind, highId)
                else:

                    bots[botid] = (
                        chips + 1,
                        min(value, value1),
                        max(value, value1),
                        lowKind,
                        lowId,
                        highKind,
                        highId,
                    )
        else:
            splitted = line.strip().split()
            botid = int(splitted[1])
            lowKind = splitted[5]
            lowId = int(splitted[6])
            highKind = splitted[-2]
            highId = int(splitted[-1])
            if botid not in bots:
                # print("is there", lowKind, lowId, highKind, highId)
                bots[botid] = (0, None, None, lowKind, lowId, highKind, highId)
            else:
                # print("not there", chips, value1, value2, lowKind, lowId, highKind, highId)
                chips, value1, value2, _, _, _, _ = bots[botid]
                bots[botid] = (chips, value1, value2, lowKind, lowId, highKind, highId)

    # print(bots)
    output = {}
    while any([chips == 2 for chips, _, _, _, _, _, _ in bots.values()]):
        for botid, (
            chips,
            value1,
            value2,
            lowKind,
            lowId,
            highKind,
            highId,
        ) in bots.items():
            # print(botid, chips, value1, value2, lowKind, lowId, highKind, highId)
            if highId == "bot" or lowId == "bot":
                print(botid, chips, value1, value2, lowKind, lowId, highKind, highId)
            if chips == 2:
                if value1 == 17 and value2 == 61:
                    print("this is the bot", botid)
                    endTimeP1 = time.time()
                    print("Part 1 took", endTimeP1 - start_time, "seconds")
                    print("Part 1 took in ms", (endTimeP1 - start_time) * 1000)
                if lowKind == "bot":
                    (
                        lowchips,
                        lowv1,
                        lowv2,
                        lowlowKind,
                        lowlowId,
                        lowhighKind,
                        lowhighId,
                    ) = bots[lowId]
                    if lowv1 is None:
                        bots[lowId] = (
                            1,
                            value1,
                            None,
                            lowlowKind,
                            lowlowId,
                            lowhighKind,
                            lowhighId,
                        )
                    else:
                        bots[lowId] = (
                            2,
                            min(value1, lowv1),
                            max(value1, lowv1),
                            lowlowKind,
                            lowlowId,
                            lowhighKind,
                            lowhighId,
                        )
                else:
                    if lowId not in output:
                        output[lowId] = []
                    output[lowId].append(value1)
                if highKind == "bot":
                    (
                        highchips,
                        highv1,
                        highv2,
                        highlowKind,
                        highlowId,
                        highhighKind,
                        highhighId,
                    ) = bots[highId]
                    if highv1 is None:
                        bots[highId] = (
                            1,
                            value2,
                            None,
                            highlowKind,
                            highlowId,
                            highhighKind,
                            highhighId,
                        )
                    else:
                        bots[highId] = (
                            2,
                            min(value2, highv1),
                            max(value2, highv1),
                            highlowKind,
                            highlowId,
                            highhighKind,
                            highhighId,
                        )
                else:
                    if highId not in output:
                        output[highId] = []
                    output[highId].append(value2)

                bots[botid] = (0, None, None, lowKind, lowId, highKind, highId)
    # print(bots)
    # print(output)
    outputMult = output[0][0] * output[1][0] * output[2][0]
    print("Part 2:", outputMult)
    endTimeP2 = time.time()
    print("Part 2 took", endTimeP2 - endTimeP1, "seconds")
    print("Part 2 took in ms", (endTimeP2 - endTimeP1) * 1000)


if __name__ == "__main__":
    main()
