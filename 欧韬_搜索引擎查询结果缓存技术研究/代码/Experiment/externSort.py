__author__ = 'alan'
import time
from lineEle import LineEle
import heapq

class ExternSort:
    def __init__(self, inputFile, blockSize, output):
        self.iFile = inputFile
        self.bSize = blockSize
        self.oFile = output

    @staticmethod
    def convert_time(iFile, output):
        in_f = open(iFile, 'rb')
        out_f = open(output, 'wb')
        for line in in_f:
            line = line.strip()
            lineArr = line.split('\t')
            qid = lineArr[0]
            old_time = lineArr[1]
            q_time = time.strptime(old_time, '%Y%m%d%H%M%S')
            new_time = int(time.mktime(q_time))
            wline = "%d\t%s\n" % (new_time, qid)
            out_f.write(wline)
        in_f.close()
        out_f.close()

    @staticmethod
    def write_sort_block(block, block_id):
        block.sort(key=lambda x: int(x[0]))
        block_file = open(str(block_id), 'wb')
        for block_line in block:
            wline = '\t'.join(block_line) + '\n'
            block_file.write(wline)
        block_file.close()

    def gen_small(self):
        in_f = open(self.iFile, "rb")
        lineNum = 0
        block = []
        blockNum = 0
        for line in in_f:
            line = line.strip()
            lineArr = line.split("\t")
            block.append(lineArr)
            lineNum += 1
            if lineNum >= self.bSize:
                ExternSort.write_sort_block(block, blockNum)
                lineNum = 0
                blockNum += 1
                block = []
        if lineNum > 0:
            ExternSort.write_sort_block(block, blockNum)
            blockNum += 1
        self.blockAmout = blockNum

    def merge_file(self, blockNum):
        out_fp = open(self.oFile, 'wb')
        fp = []
        my_heap = []
        for fid in xrange(blockNum):
            fp.append(open(str(fid), 'rb'))
            heapq.heappush(my_heap, LineEle(fp[fid].readline(), fid))
        while my_heap:
            my_fid = my_heap[0].fid
            line = fp[my_fid].readline()
            if line:
                pop_line = heapq.heapreplace(my_heap, LineEle(line, my_fid))
            else:
                pop_line = heapq.heappop(my_heap)
            out_fp.write(str(pop_line))
        for fid in range(blockNum):
            fp[fid].close()
        out_fp.close()

    def work(self):
        self.gen_small()
        self.merge_file(self.blockAmout)

if __name__ == '__main__':
    esort = ExternSort("time_id", 1000000, "sortedLog")
    esort.merge_file(44)
    #ExternSort.convert_time("q_with_no", "time_id")
