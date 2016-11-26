__author__ = 'outao'
from collections import OrderedDict


class alg:
    def __init__(self,c, **kwargs):
        self.c = c        # Cache size
        self.cn = 0       # Items in cache now
        self.cached = {}  # Cached keys
        self.hitcount = 0
        self.count = 0
        self.p = 0
        self.t1 = OrderedDict()
        self.t2 = OrderedDict()
        self.b1 = OrderedDict()
        self.b2 = OrderedDict()

    def setup(self, reqlist):
                # I'm an online algorithm :-)
        pass

    def replace(self, args):
        if self.t1 and ((args in self.b2 and len(self.t1) == self.p) or (len(self.t1) > self.p)):
            k, e = self.t1.popitem(last=False)
            self.b1[k] = e
        else:
            k, e = self.t2.popitem(last=False)
            self.b2[k] = e
        del self.cached[k]

    def get(self, key, warm=0):
        if not warm:
            self.count += 1
        if key in self.t1:
            del self.t1[key]
            self.t2[key] = 1
            if not warm:
                self.hitcount += 1
            return 1
        elif key in self.t2:
            del self.t2[key]
            self.t2[key] = 1
            if not warm:
                self.hitcount += 1
            return 1
        return 0

    def put(self, key, val=1):
        if key in self.cached:
            return
        self.cached[key] = 1
        if key in self.b1:
            self.p = min(self.c, self.p + max(len(self.b2) / len(self.b1), 1))
            self.replace(key)
            del self.b1[key]
            self.t2[key] = 1
            return
        if key in self.b2:
            self.p = max(0, self.p - max(len(self.b1)/len(self.b2), 1))
            self.replace(key)
            del self.b2[key]
            self.t2[key] = 1
            return
        if len(self.t1) + len(self.b1) == self.c:
            if len(self.t1) < self.c:
                self.b1.popitem(last=False)
                self.replace(key)
            else:
                del self.cached[self.t1.popitem(last=False)[0]]
        else:
            total = len(self.t1) + len(self.b1) + len(self.t2) + len(self.b2)
            if total >= self.c:
                if total == (2 * self.c):
                    self.b2.popitem(last=False)
                self.replace(key)
        self.t1[key] = 1