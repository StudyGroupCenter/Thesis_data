__author__ = 'alan'
from lineEle import BucketEle

class CacheStratege(object):
    def __init__(self, cache_size, log_file, time_to_live=3600, warm_up_num=0):
        self.size = cache_size
        self.logFile = log_file
        self.cache = {}
        self.ttl = time_to_live
        self.hit = 0
        self.q_num = 0
        self.warm_up = warm_up_num

    def prefetch(self, now):
        pass

    def processQuery(self, qid, qtime):
        self.q_num += 1
        if qid in self.cache and qtime < self.cache[qid]:
            if self.q_num > self.warm_up:
                self.hit += 1
        else:
            self.cache[qid] = qtime + self.ttl


    def test(self):
        qf = open(self.logFile, "rb") #log sorted by query time
        for line in qf:
            line = line.strip()
            lineArr = line.split('\t')
            now, qid = int(lineArr[0]), lineArr[1]
            self.prefetch(now)
            self.processQuery(qid, now)
        qf.close()

    def report(self):
        print "cache size\tttl\tquery amount\thit"
        print "%d\t%d\t%d\t%d" % (self.size, self.ttl, self.q_num, self.hit)


class OfflineCache(CacheStratege):
    def __init__(self, cache_size, log_file, bucket_num, time_to_live=3600, warm_up_num=0, min_age=1800):
        super(OfflineCache, self).__init__(cache_size, log_file, time_to_live, warm_up_num)
        self.N = bucket_num + 1
        self.day = 86400
        self.buckets = [BucketEle()] * self.N #circle buckets
        self.buck_id = 0
        self.interval = self.day/bucket_num
        self.prefetch_time = 0
        self.last_bucket_id = 0
        self.live_age = self.ttl - min_age

    def processQuery(self, qid, qtime):
        super(OfflineCache, self).processQuery(qid, qtime)
        today = qtime/self.day
        day_time = qtime % self.day
        bucket_id = day_time/self.interval
        self.buck_id = (self.buck_id + ((bucket_id - self.last_bucket_id + self.N-1) % (self.N - 1))) % self.N
        self.last_bucket_id = bucket_id
        if today > self.buckets[self.buck_id].day:
            self.buckets[bucket_id].day = today
            self.buckets[bucket_id].querys.clear()
        self.buckets[bucket_id].querys.add(qid)

    def refresh(self, candidate_set, now):
        for qid in candidate_set:
            deadline = self.cache[qid]
            if deadline - now < self.live_age:
                self.cache[qid] = now + self.ttl


    def prefetch(self, now):
        if now >= self.prefetch_time:
            r_tick = now % self.interval
            self.prefetch_time = now - r_tick + self.interval
            bucket_need = self.ttl/self.interval
            day_time = now % self.day
            bucket_id = day_time/self.interval
            bucket_index = (self.buck_id + ((bucket_id - self.last_bucket_id + self.N-1) % (self.N - 1))) % self.N
            candidate = set()
            for bid in range(0, bucket_need):
                bucket_index = (bucket_index + 1) % self.N
                for x in self.buckets[bucket_index].querys:
                    candidate.add(x)
            self.refresh(candidate, now)


if __name__ == '__main__':
    cache_test = OfflineCache(9999999, 'sortedLog', 240, warm_up_num=10000000)
    cache_test.test()
    cache_test.report()









