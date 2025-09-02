import re

# Replace this with your log file path
log_file = "tymponogram.log"

def openfile():
    with open(log_file, "rb") as f:
        return f.read()
    
if __name__ == "__main__":
    log_contents = openfile()
    splitted = log_contents.split(b'\n')
    for l in splitted:
        # for d in l:
        #     hexbyte = hex(d).zfill(2).replace("0x", "").zfill(2).upper()
        #     if d == 13:
        #         print("\\n\n", end="")
        #     elif d == 10:
        #         pass
        #     elif d >= 32 and d <= 126:
        #         print(chr(d), end="")
        #     else:
        #         print(hexbyte, end="")
        for d in l:
            hexbyte = hex(d).zfill(2).replace("0x", "").zfill(2).upper()
            print(hexbyte, end="")
        print()
    # for d in log_contents:
    #     hexbyte = hex(d).zfill(2).replace("0x", "").zfill(2).upper()
    #     # print(hexbyte, end=",")
    #     if d == 13:
    #         print("\\n\n", end="")
    #     elif d == 10:
    #         pass
    #     elif d >= 32 and d <= 126:
    #         print(chr(d), end="")
    #     else:
    #         print(hexbyte, end=" ")

