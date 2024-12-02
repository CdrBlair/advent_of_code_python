import hashlib
import time


def main():
    start_time = time.time()

    door_id = "ffykfhsq"
    index = 0
    password = ""

    while len(password) < 8:
        current_input = door_id + str(index)
        current_hash = hashlib.md5(current_input.encode()).hexdigest()
        if current_hash[:5] == "00000":
            password += current_hash[5]
            print(current_input)
            print(current_hash)
            print(password)
        index += 1

    print(password)

    end_time = time.time()
    print(end_time - start_time)

    start_time_p2 = time.time()
    new_password = [""] * 8
    found_chars = 0
    index = 0
    while found_chars < 8:
        current_input = door_id + str(index)
        current_hash = hashlib.md5(current_input.encode()).hexdigest()
        if current_hash[:5] == "00000":
            print(current_input)
            print(current_hash)
            if current_hash[5] in "01234567":
                pw_index = int(current_hash[5])
                if pw_index < 8 and new_password[pw_index] == "":
                    new_password[pw_index] = current_hash[6]
                    print(new_password)
                    found_chars += 1

        index += 1

    print("".join(new_password))

    end_time_p2 = time.time()
    print(end_time_p2 - start_time_p2)


if __name__ == "__main__":
    main()
