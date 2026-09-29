import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from sort import SORTS

class Tagged:
    def __init__(self, key, tag): self.key, self.tag = key, tag
    def __lt__(self, other): return self.key < other.key
    def __le__(self, other): return self.key <= other.key
    def __ge__(self, other): return self.key >= other.key

def stable(a):
    return all(x.key != y.key or x.tag < y.tag for x, y in zip(a, a[1:]))

class SortTests(unittest.TestCase):
    def test_basic(self):
        for name, sorter in SORTS.items():
            for data in ([], [2], [3, 1, 2, 1, 0], [-5, 0, -5, 3], list(range(50)), list(range(50, 0, -1)), [7]*50):
                with self.subTest(name=name, data=data[:5]):
                    actual = data.copy();sorter(actual)
                    self.assertEqual(actual, sorted(data))
    def test_sizes(self):
        for n in range(201):
            for name, sorter in SORTS.items():
                with self.subTest(name=name, n=n):
                    data = [(i*37+n*11)%13-6 for i in range(n)]
                    actual=data.copy();sorter(actual)
                    self.assertEqual(actual, sorted(data))
    def test_stability(self):
        for name, sorter in SORTS.items():
            with self.subTest(name=name):
                data=[Tagged(key, i) for i,key in enumerate([3,1,3,1,2,1,3])]
                sorter(data)
                self.assertEqual([x.key for x in data], [1,1,1,2,3,3,3])
                self.assertEqual(sorted(x.tag for x in data), list(range(7)))
                self.assertTrue(all(x.key == [3,1,3,1,2,1,3][x.tag] for x in data))
                if name != 'heap':self.assertTrue(stable(data))
        ties=[Tagged(1,i) for i in range(4)]
        SORTS['heap'](ties)
        self.assertFalse(stable(ties))

if __name__ == '__main__': unittest.main()
