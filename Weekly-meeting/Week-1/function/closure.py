def sort_priority(numbers, group):
    found = [False]
    def helper(x):
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found[0]

if __name__ == "__main__":
    numbers = [8, 3, 1, 2, 5, 4, 7, 6]
    group = set([2, 3, 5, 7])
    found = sort_priority(numbers, group)
    print('Found:', found)
    print(numbers)