import pytest 
from dsap.misc.cp_combinations import combinations 
from dsap.misc.cp_permutations import * 

def test_combinations():
    items = ["A", "B", "C"] 
    combs = combinations(items) 
    match_ = [
        ['A'], 
        ['A', 'B'], 
        ['A', 'B', 'C'], 
        ['A', 'C'], 
        ['B'], 
        ['B', 'C'], 
        ['C'], 
    ]
    
    assert(len(combs) == len(match_) )

    for item in match_: 
        assert(item in combs)

def test_combinations_range():
    items = ["A", "B", "C", "D"] 
    combs = combinations(items, 2, 3) 
    
    match_ = [
        ['A', 'B'], 
        ['A', 'B', 'C'], 
        ['A', 'B', 'D'], 
        ['A', 'C'], 
        ['A', 'C', 'D'], 
        ['A', 'D'], 
        ['B', 'C'], 
        ['B', 'C', 'D'], 
        ['B', 'D'], 
        ['C', 'D']
    ]
    
    assert(len(combs) == len(match_))

    for item in match_: 
        assert(item in combs)

def test_permutations_without_repetitions():
    items = [1, 2, 3] 
    perm = permutation_without_repetition(items, 3) 

    match_ = [
        [1, 2, 3], [1, 3, 2], 
        [2, 1, 3], [2, 3, 1], 
        [3, 1, 2], [3, 2, 1]
    ] 

    assert(len(perm) == len(match_)) 
    
    for item in match_: 
        assert(item in perm)


