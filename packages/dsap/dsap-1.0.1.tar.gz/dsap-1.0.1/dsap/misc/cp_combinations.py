

def combinations(items, min_ = None, max_ = None, combination = [], level = 1): 
    results = [] 

    if min_ is None: 
        min_ = 0 
    if max_ is None: 
        max_ = len(items)

    for i in range(len(items)): 
        combination.append(items[i])
        
        if level >= min_:
            results.append(combination[:])
        
        if level + 1 <= max_:
            results += \
                combinations(
                    items[i + 1:], 
                    min_, 
                    max_, 
                    combination, 
                    level + 1
                ) 
        
        combination.pop()

    return results
