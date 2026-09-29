"""Three comparison sorts modifying their input; merge uses auxiliary storage.
Functions return key-comparison counts."""

def insertion_sort(a):
    comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return comparisons


def merge_sort(a):
    temp = [None] * len(a)
    comparisons = 0

    def recur(lo, hi):
        nonlocal comparisons
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        recur(lo, mid)
        recur(mid, hi)
        i, j = lo, mid
        for k in range(lo, hi):
            if i == mid:
                temp[k] = a[j]
                j += 1
            elif j == hi:
                temp[k] = a[i]
                i += 1
            else:
                comparisons += 1
                if a[i] <= a[j]:  # left first on ties: stable
                    temp[k] = a[i]
                    i += 1
                else:
                    temp[k] = a[j]
                    j += 1
        a[lo:hi] = temp[lo:hi]

    recur(0, len(a))
    return comparisons


def heap_sort(a):
    comparisons = 0

    def sift_down(root, size):
        nonlocal comparisons
        while 2 * root + 1 < size:
            child = 2 * root + 1
            if child + 1 < size:
                comparisons += 1
                if a[child] < a[child + 1]:
                    child += 1
            comparisons += 1
            if a[root] >= a[child]:
                break
            a[root], a[child] = a[child], a[root]
            root = child

    for root in range(len(a) // 2 - 1, -1, -1):
        sift_down(root, len(a))
    for end in range(len(a) - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return comparisons

SORTS = {'insertion': insertion_sort, 'merge': merge_sort, 'heap': heap_sort}
