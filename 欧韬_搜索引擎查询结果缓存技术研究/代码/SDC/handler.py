__author__ = 'outao'

def keyFunc(item):
    return item[1]


def pre_handler(filename, output):
        logfile = open(filename)
        line = logfile.readline()
        table = {}
        tops = []
        while line:
            query = int(line)
            if query in table:
                item = table[query]
                item[1] += 1
            else:
                item = [query, 1]
                table[query] = item
                tops.append(item)
            line = logfile.readline()
        logfile.close()
        tops.sort(key=keyFunc, reverse=True)
        text = ""
        for item in tops:
            text += str(item[1])
            text += '\n'
        out_file = open(output, 'w')
        out_file.write(text)
        out_file.close()

pre_handler("aol_log", "aol_rank")
