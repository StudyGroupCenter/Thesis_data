__author__ = 'alan'
class LineEle():
    def __init__(self, line_str, file_id = 0):
        self.line = line_str
        self.fid = file_id

    def __cmp__(self, other):
        first = int(self.line.split('\t')[0])
        second = int(other.line.split('\t')[0])
        return int.__cmp__(first, second)

    def __repr__(self):
        return self.line

class BucketEle(object):
    def __init__(self):
        self.day = 0
        self.querys = set()




if __name__ == '__main__':
    print str(LineEle("123\t222"))
    pass