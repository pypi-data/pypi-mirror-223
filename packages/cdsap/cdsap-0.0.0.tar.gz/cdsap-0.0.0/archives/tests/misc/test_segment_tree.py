import pytest 
from dsap.misc.segment_tree import SegmentTree

def test_range_sum():
    items = [1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15]
    segment_tree = SegmentTree(items) 

    expected_sum = sum(items[3:9]) 
    result = segment_tree.range_sum(3, 8)

    assert(expected_sum == result)

@pytest.mark.depends(on=["test_range_sum"])
def test_update(): 
    items = [1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15]
    segment_tree = SegmentTree(items) 

    sum_ = sum(items) 

    segment_tree.update(3, 8)

    sum_ = sum_ + 4
    new_sum = segment_tree.range_sum(0, len(items) - 1)


    assert(sum_ == new_sum)

def test_find_interval(): 
    items = [4, 1, 8, 9, 2, 6, 4, 1]
    segment_tree = SegmentTree(items)
    interval = segment_tree.find_interval(34.5)

    assert(interval == (6, 7))

