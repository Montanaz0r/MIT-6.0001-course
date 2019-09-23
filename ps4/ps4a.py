def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]   # returning list containing one element.
    else:
        permutations = []
        first_letter = sequence[0]   # grabbing first letter.
        rest_of_sequence = sequence[1:]   # leaving the rest of sequence.
        subsequence = get_permutations(rest_of_sequence)   # calling recursive func for the rest of sequence.
        for item in subsequence:   # iterating through our new subset.
            for i in range(len(item) + 1):   # iterating through length of each item in subset.
                new_item = item[0:i] + first_letter + item[i:len(item) + 1]   # creating new item with different
                permutations.append(new_item)                                 # sequence of first_letter variable.
        return permutations


if __name__ == '__main__':
    #    #EXAMPLE
    #    example_input = 'abc'
    #    print('Input:', example_input)
    #    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    #    print('Actual Output:', get_permutations(example_input))
    
    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)

    # Test case #1
    print(12 * '-' + '#####' + 12 * '-')
    example_input = 'abc'
    print(f'Input: {example_input}')
    print('Expected Output: ["abc", "acb", "bac", "bca", "cab", "cba"]')
    print(f'Actual Output: {get_permutations(example_input)}')

    # Test case #2
    print(12 * '-' + '#####' + 12 * '-')
    example_input = 'mz'
    print(f'Input: {example_input}')
    print('Expected Output: ["mz", "zm"]')
    print(f'Actual Output: {get_permutations(example_input)}')

    # Test case #3
    print(12 * '-' + '#####' + 12 * '-')
    example_input = 'bus'
    print(f'Input: {example_input}')
    print('Expected Output: ["bus", "bsu", "ubs", "usb", "sbu", "sub"]')
    print(f'Actual Output: {get_permutations(example_input)}')

