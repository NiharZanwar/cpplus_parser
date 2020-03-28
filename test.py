with open("log.txt", "a") as f:
    f.write("hello\n")

def make_log(string):
    string += "\n"
    with open("log.txt", "a") as f:
        f.write(string)