from setuptools.namespaces import flatten
import xmltodict
import yaml
import json
import re
import time

def check(pparsed, index, line) -> bool:
    local_level = 1
    for i in range(index + 1, len(pparsed)):
        if len(pparsed[i]) == 1:
            if pparsed[i][0][0] == "/":
                local_level -= 1
            else:
                if pparsed[i] == line and local_level == 0:
                    return True
                else:
                    local_level += 1
    return False


def main(use_regex):
    f = open("Day.xml", "r", encoding="UTF8")

    pparsed = []
    if use_regex:
        result = open("Day2.yaml", 'w', encoding="UTF8")
        pparsed = re.sub(r"<\/(.+)>", r"", f.read())
        pparsed = re.sub(r"<(.+)>(\S+)", r"\1: \2", pparsed)
        pparsed = re.sub(r"<(.+)>(\s*\n)", r"\1: \n", pparsed)
        result.write(pparsed)
        return 0
    else:
        for line in f:
            parsed = list(flatten([i.split(">") for i in line.strip().split("<")]))
            parsed.pop(0)
            parsed.pop(-1)
            pparsed.append(parsed)

    result = open("Day.yaml", 'w', encoding="UTF8")
    tab = "  "
    level = 0
    last = []
    is_list = False
    for index, line in enumerate(pparsed):
        if len(line) == 1:
            if line[0][0] != "/":
                if line == last:
                    is_list = True
                else:
                    result.write(((level - 1) * tab + "- ", level * tab)[not is_list] +
                                 line[0] + ":\n")
                    is_list = check(pparsed, index, line)
                level += 1
            else:
                last = [line[0][1:]]
                level -= 1
        else:
            result.write(((level - 1) * tab + "- ", level * tab)[not is_list] + line[0] + ": " + line[1] + "\n")
            is_list = False

    f.close()
    result.close()


def main1():
    result = open("Day1.yaml", 'w', encoding="UTF8")
    result.write(yaml.dump(json.loads(json.dumps(
        xmltodict.parse(open("Day.xml", "r", encoding="UTF8").read()))), allow_unicode=True))


if __name__ == '__main__':
    start = time.time()
    for i in range(100):
        main(True)
    print("Regex: %f" % (time.time() - start))
    start = time.time()
    for i in range(100):
        main1()
    print("Lib: %f" % (time.time() - start))

