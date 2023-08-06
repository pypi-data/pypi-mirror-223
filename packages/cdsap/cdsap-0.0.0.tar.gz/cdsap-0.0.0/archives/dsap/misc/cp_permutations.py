

def permutation_with_repetition(items, r, perm = [], level = 1):      
    if level > r: 
        return [perm[:]] 

    results = [] 

    for i in range(len(items)):
        perm.append(items[i])
        results += \
            permutation_with_repetition(
                items, r, perm, level + 1
            )
        perm.pop()
        
    return results

def permutation_without_repetition(items, r, perm = [], level = 1):      
    if level > r: 
        return [perm[:]] 

    results = [] 

    for i in range(len(items)):
        perm.append(items[i])
        new_items = items[:]
        new_items.pop(i)
        results += \
            permutation_without_repetition(
                new_items, r, perm, level + 1
            )
        perm.pop()
        
    return results

