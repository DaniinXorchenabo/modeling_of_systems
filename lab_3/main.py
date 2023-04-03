import enum


class ZState(enum.Enum):
    z1 = 'z1'
    z2 = 'z2'
    z3 = 'z3'
    z4 = 'z4'
    z5 = 'z5'
    z6 = 'z6'
    z7 = 'z7'
    z8 = 'z8'


class YState(enum.Enum):
    y1 = 'y1'
    y2 = 'y2'
    y3 = 'y3'
    y4 = 'y4'
    y5 = 'y5'


rules = {
    ZState.z1: ZState.z6,
    ZState.z2: ZState.z4,
    ZState.z3: ZState.z7,
    ZState.z4: ZState.z3,
    ZState.z5: ZState.z1,
    ZState.z6: ZState.z8,  # z2
    ZState.z7: ZState.z5,
    ZState.z8: ZState.z2,

}

output_rules = {
    ZState.z1: YState.y1,
    ZState.z2: YState.y2,
    ZState.z3: YState.y3,
    ZState.z4: YState.y2,
    ZState.z5: YState.y5,  # 1
    ZState.z6: YState.y4,  # 1
    ZState.z7: YState.y1,  # 3
    ZState.z8: YState.y4,
}

curr_state = ZState.z1
max_iteration = 100
i = 0
while True:
    out = output_rules[curr_state]
    curr_state = rules[curr_state]
    print(out, curr_state)
    if i >= max_iteration:
        break
    i += 1


