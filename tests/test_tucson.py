import pytest

from tridat import tucson 

@pytest.fixture
def read_rwl_headless():
    return tucson.read_rwl(r'./tests/data/mn008.rwl')

def test_rwl_headless(read_rwl_headless):
    cnt = 0
    for series in read_rwl_headless:
        if type(series) == tucson.TreeRingSeries:
            cnt += 1
    assert cnt == 16
