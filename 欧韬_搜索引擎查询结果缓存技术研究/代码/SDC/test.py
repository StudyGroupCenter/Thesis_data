__author__ = 'linfuyuan' 
min_frequency = int(raw_input('please input min_frequency:')) 
file_name = raw_input('please input the transaction file:') 
transactions = [] 
   
   
def has_infrequent_subset(candidate, Lk): 
    for i in range(len(candidate)): 
        subset = candidate[:-1] 
        subset.sort() 
        if not ''.join(subset) in Lk: 
            return False 
        lastitem = candidate.pop() 
        candidate.insert(0, lastitem) 
    return True 
   
   
def countFrequency(candidate, transactions): 
    count = 0 
    for transaction in transactions: 
        if transaction.issuperset(candidate): 
            count += 1 
    return count 
   
   
with open(file_name) as f: 
    for line in f.readlines(): 
        line = line.strip() 
        tokens = line.split(',') 
        if len(tokens) > 0: 
            transaction = set(tokens) 
            transactions.append(transaction) 
currentFrequencySet = {} 
for transaction in transactions: 
    for item in transaction: 
        time = currentFrequencySet.get(item, 0) 
        currentFrequencySet[item] = time + 1 
Lk = set() 
for (itemset, count) in currentFrequencySet.items(): 
    if count >= min_frequency: 
        Lk.add(itemset) 
print ', '.join(Lk) 
   
while len(Lk) > 0: 
    newLk = set() 
    for itemset1 in Lk: 
        for itemset2 in Lk: 
            cancombine = True 
            for i in range(len(itemset1)): 
                if i < len(itemset1) - 1: 
                    cancombine = itemset1[i] == itemset2[i] 
                    if not cancombine: 
                        break 
                else: 
                    cancombine = itemset1[i] < itemset2[i] 
                    if not cancombine: 
                        break 
            if cancombine: 
                newitemset = [] 
                for char in itemset1: 
                    newitemset.append(char) 
                newitemset.append(itemset2[-1]) 
                if has_infrequent_subset(newitemset, Lk) and countFrequency(newitemset, transactions) >= min_frequency: 
                    newLk.add(''.join(newitemset)) 
    print ', '.join(newLk) 
    Lk = newLk