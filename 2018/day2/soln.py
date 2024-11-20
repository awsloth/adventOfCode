with open("data.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

def countLetters(s : str):
    count_dict = dict()
    for letter in s:
        if letter in count_dict:
            count_dict[letter] += 1
        else:
            count_dict[letter] = 1

    return count_dict

counts = [countLetters(l) for l in lines]

twos = sum([any(c == 2 for c in d.values()) for d in counts])
threes = sum([any(c == 3 for c in d.values()) for d in counts])

print(twos*threes)

