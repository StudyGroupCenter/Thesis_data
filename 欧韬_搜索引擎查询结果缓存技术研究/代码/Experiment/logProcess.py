__author__ = 'alan'
import sys
import fileinput

def reduceLog():
    num = 0
    f = open('querylog', "rb")
    output = open('qlog',"wb")
    wlines = []
    count = 0
    for line in f:
        line = line.strip()
        arr = line.split('\t')
        wlines.append('%s\t%s\n' % (arr[0], arr[2]))
        count += 1
        if count%10000 == 0:
            output.writelines(wlines)
            wlines = []
    output.writelines(wlines)

    f.close()
    output.close()
    print count

def head(lineNum, fileName):
    i = 0
    f = open(fileName, 'rb')
    for line in f:
        i += 1
        print line.decode('gbk'),
        if i >= lineNum:
            break
    f.close()

def getRowCount(fileName):
    f = open(fileName, 'rb')
    count = 0
    for line in f:
        count += 1
    f.close()
    return count

def getQid(dictFile, qFile, output):
    df = open(dictFile, 'rb')
    M = {} # get query_id by query
    for line in df:
        line = line.strip()
        lineArr = line.split()
        query = lineArr[1]
        M[query] = lineArr[0]
    df.close()
    qf = open(qFile, 'rb')
    f = open(output, 'wb')
    for line in qf:
        line = line.strip()
        lineArr = line.split('\t')
        query = lineArr[1]
        key = '_'.join(query.split())
        if key in M:
            wline = "%s\t%s\n" % (M[key], line)
            f.write(wline)
    qf.close()
    f.close()



def getId(qFile, output):
    num = 0
    qf = open(qFile, 'rb')
    f = open(output, 'wb')
    qnum = {}
    for line in qf:
        line = line.strip()
        lineArr = line.split('\t')
        query = lineArr[1]
        if query not in qnum:
            num += 1
            qnum[query] = num
        wline = "%s\t%s\n" % (qnum[query], line)
        f.write(wline)
    qf.close()
    f.close()

def getQueryById(qlog, id):
    f = open(qlog, 'rb')
    for line in f:
        line = line.strip()
        lineArr = line.split('\t')
        query = lineArr[2]
        qid = lineArr[0]
        if qid == id:
            print query.decode('gbk')
            break
    f.close()

#reduceLog()
#head(10, 'qlog')
#print getRowCount('sortedLog')
#getQid('myQnumFreqlog', 'qlog','q_with_no')

head(10, 'sortedLog')

#getId('qlog', 'qlog_with_no')
#getQueryById('qlog_with_no', '3421880')
print "finished"


