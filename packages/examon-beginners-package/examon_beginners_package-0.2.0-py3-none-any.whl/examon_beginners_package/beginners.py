from examon_core.examon_item import examon_item


@examon_item(choices=[
    'Hello, Bob. How are you?', 'Hello, Jeff. How are you?',
    'Hello, Bob.', 'Hello, Jeff.', '. How are you?'],
    tags=['strings', 'beginner'])
def question():
    name = 'Jeff'
    name = 'Bob'
    greeting = f'Hello, {name}'
    greeting += ". How are you?"
    return greeting


@examon_item(choices=[
    'Hello', 'Hell',
    'Hello,', ['H', 'e', 'l', 'l', 'o']],
    tags=['strings', 'slicing', 'beginner'])
def question():
    greeting = 'Hello, how are you'
    return greeting[0:5]


@examon_item(choices=[
    'j', 'jk', 'ba'],
    tags=['strings', 'slicing', 'beginner'])
def question():
    letters = 'abcdefghijk'
    return letters[-2:]


@examon_item(choices=[
    'Hello, {name} you are {(23)}',
    'Hello, Bob you are (23)',
    'Hello, Bob you are 23'
],
    tags=['strings', 'interpolation', 'beginner'])
def question():
    name = 'Bob'
    return f'Hello, {name} you are {(23)}'


@examon_item(choices=[
    [True, True],
    [False, True],
    [True, False],
    [False, False],
], tags=['equality', 'dict', 'beginner'])
def question():
    my_object = {'name': 'bob'}
    new_ref = my_object
    return [
        my_object is new_ref,
        my_object is {'name': 'bob'}
    ]


@examon_item(choices=[
    ['the', 'cat', 'in', 'the', 'hat'], []
], tags=['array', 'for', 'if', 'beginner'])
def question():
    words = ['the', 'cat', 'in', 'the', 'hat']

    new_words = []
    for w in words:
        if (len(w) > 2):
            new_words.append(w)

    return new_words


@examon_item(choices=['15', '12345', '5'],
             tags=['for', 'range', 'beginner', '__add__'])
def question():
    x = None
    for i in range(1, 5):
        x += i

    return x


@examon_item(choices=['10', '25', '5'],
             tags=['beginner', '__pow__'])
def question():
    return 5 ** 2


@examon_item(choices=['182.0', '37.0', '117.0', '182', '37', '117'],
             tags=['beginner', '__pow__'])
def question():
    return 36 / 4 * (3 + 2) * 4 + 2


@examon_item(choices=['Jam',
                      'dno',
                      'maJ',
                      'dnoB semaJ'],
             tags=['beginner', 'slicing'])
def question():
    var = "James Bond"
    return var[2::-1]


@examon_item(choices=['10', '20', '30'],
             tags=['beginner', ''])
def question():
    p, q, r = 10, 20, 30
    return r


@examon_item(choices=['py', 'yn', 'pyn', 'yna'],
             tags=['beginner', 'slicing'])
def question():
    str = "pynative"
    return str[1:3]


@examon_item(choices=[
    ['Jon', 'Kelly', 'Scott', 'Jessa'],
    ['Jon', 'Kelly', 'Jessa', 'Scott'],
    ['Jon', 'Scott', 'Kelly', 'Jessa']
],
    tags=['beginner', ''])
def question():
    sample_list = ["Jon", "Kelly", "Jessa"]
    sample_list.append(2, "Scott")
    return sample_list


@examon_item(choices=[
    [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5],
    [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
],
    tags=['beginner', ''])
def question():
    my_list = []
    for x in range(0.5, 5.5, 0.5):
        my_list.append(x)
    return my_list


@examon_item(choices=['CatCatCatCatCat', 'CatCatCatCatCatCat'],
             tags=['beginner', 'strings'])
def question():
    return "Cat" * 2 * 3


@examon_item(choices=[
    (False, False),
    (True, False),
    (False, True),
    (True, True),
],
    tags=['beginner', ''])
def question():
    list_one = [20, 40, 60, 80]
    list_two = [20, 40, 60, 80]

    return list_one == list_two, list_one is list_two
