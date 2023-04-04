import enum
import random

N = 2  # количество матриц A
M = 5  # количество столбцов в матрице B
p = 3  # количество состояний (количество столбцов и строк в матрице A, количество строк в матрице B)


class InputE(enum.Enum):
    i1 = 'i1'
    i2 = 'i2'


class StateE(enum.Enum):
    s1 = 's1'
    s2 = 's2'
    s3 = 's3'


class OutputE(enum.Enum):
    o1 = 'o1'
    o2 = 'o2'
    o3 = 'o3'
    o4 = 'o4'
    o5 = 'o5'


A = {
    InputE.i1: {
        StateE.s1: {
            StateE.s1: 0.1,
            StateE.s2: 0.3,
            StateE.s3: 0.6,
        },
        StateE.s2: {
            StateE.s1: 0.5,
            StateE.s2: 0.2,
            StateE.s3: 0.3,
        },
        StateE.s3: {
            StateE.s1: 0.2,
            StateE.s2: 0.7,
            StateE.s3: 0.1,
        },
    },
    InputE.i2: {
        StateE.s1: {
            StateE.s1: 0.1,
            StateE.s2: 0.8,
            StateE.s3: 0.1,
        },
        StateE.s2: {
            StateE.s1: 0.3,
            StateE.s2: 0.3,
            StateE.s3: 0.4,
        },
        StateE.s3: {
            StateE.s1: 0,
            StateE.s2: 0.7,
            StateE.s3: 0.2,
        },
    },

}

B = {
    InputE.i1: {
        StateE.s1: {
            OutputE.o1: 0.2,
            OutputE.o2: 0.1,
            OutputE.o3: 0.0,
            OutputE.o4: 0.4,
            OutputE.o5: 0.3,
        },
        StateE.s2: {
            OutputE.o1: 0.2,
            OutputE.o2: 0.2,
            OutputE.o3: 0.2,
            OutputE.o4: 0.2,
            OutputE.o5: 0.2,
        },
        StateE.s3: {
            OutputE.o1: 0.0,
            OutputE.o2: 0.0,
            OutputE.o3: 0.0,
            OutputE.o4: 0.2,
            OutputE.o5: 0.0,
        },
    },
    InputE.i2: {
        StateE.s1: {
            OutputE.o1: 0.7,
            OutputE.o2: 0.1,
            OutputE.o3: 0.1,
            OutputE.o4: 0.0,
            OutputE.o5: 0.1,
        },
        StateE.s2: {
            OutputE.o1: 0.1,
            OutputE.o2: 0.3,
            OutputE.o3: 0.2,
            OutputE.o4: 0.3,
            OutputE.o5: 0.1,
        },
        StateE.s3: {
            OutputE.o1: 0.1,
            OutputE.o2: 0.2,
            OutputE.o3: 0.3,
            OutputE.o4: 0.4,
            OutputE.o5: 0.0,
        },
    },
}

init_C = {
    StateE.s1: 0.4,
    StateE.s2: 0.2,
    StateE.s3: 0.4,
}

inp = {
    InputE.i1: 0.5,
    InputE.i2: 0.5
}


def get_random_val(data: dict[enum.Enum, float], random_val=None):
    last = 0.0
    curr = 0.0
    random_val = random_val or random.random()
    curr_k = None
    for k, v in data.items():
        curr_k = k
        curr += v
        if last <= random_val < curr:
            return k, random_val
    return curr_k, random_val


def input_generator():
    max_iteration = 100
    i = 0
    while i <= max_iteration:
        yield get_random_val(inp)
        i += 1


curr_state, v = get_random_val(init_C)
print('x'.rjust(10) + "|"
      + 'z_old'.rjust(10) + '|'
      + 'r_1'.rjust(10) + '|'
      + 'z_new'.rjust(10) + '|'
      + 'r_2'.rjust(10) + '|'
      + 'y'.rjust(10) + '|')
for (i, inp_v) in input_generator():
    out, v = get_random_val(B[i][curr_state])
    old_state = curr_state
    curr_state, v = get_random_val(A[i][curr_state], random_val=v)
    print(str(i).rjust(10) + "|"
          + str(old_state).rjust(10) + '|'
          + str(round(inp_v, 2)).rjust(10) + '|'
          + str(curr_state).rjust(10) + '|'
          + str(round(v, 2)).rjust(10) + '|'
          + str(out).rjust(10) + '|')
    # print(f"Вход {i}, вывод: {out}, текущее состояние: {curr_state}")
