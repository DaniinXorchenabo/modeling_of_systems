import os
from typing import Callable

from lab_5.gauss.labs_2_3_and_4.enums import SolutionMethodMods, Sign, ExprType, SolutionMethod, VRole
from lab_5.gauss.labs_2_3_and_4.builder import expr_system_builder


def eller_m(last_y, h, ys, func):
    return last_y + h * func(ys)

def runge_kutta_method(expt_num, t,  ys, func):
    k1 = func(ys)
    # k2 = func([  ((i + (t*k1/2)) if ind == expt_num else i) for ind, i in enumerate(ys)])
    # k3 = func([  ((i + (t * k2 / 2)) if ind == expt_num else i) for ind, i in enumerate(ys)])
    # k4 = func([  ((i + (t * k3)) if ind == expt_num else i) for ind, i in enumerate(ys)])
    k2 = func([(i + (t * k1 / 2))  for ind, i in enumerate(ys)])
    k3 = func([(i + (t * k2 / 2))  for ind, i in enumerate(ys)])
    k4 = func([(i + (t * k3))for ind, i in enumerate(ys)])
    return ys[expt_num] + t*(1/6*k1 + 1/3*k2 + 1/3*k3 + 1/6*k4)

def func(
        h,
        T=20
):
    h = float(h)
    x_last = [1, 0, 0, 0]
    x_next = [0] * 4
    results = {float(0): x_last}
    for t in (i * h for i in range(round(T / h))):
        x_next = [0] * 4
        x_next[0] = runge_kutta_method(0, h, x_last, lambda ys:  ys[1] + ys[2] - 2 * ys[0])
        x_next[1] = runge_kutta_method(1, h, x_last, lambda ys: 2 * ys[2] + 2 * ys[3] - 1 * ys[1])
        x_next[2] = runge_kutta_method(2, h, x_last, lambda ys: 4 * ys[3] - 3 * ys[2])
        x_next[3] = runge_kutta_method(3, h, x_last, lambda ys: 2 * ys[0] - 6 * ys[3])
        # x_next[3] = runge_kutta_method(3, h, x_last, lambda ys: ys[0] +   ys[1] +  ys[2] +  ys[3])
        results[round(t, 6)] = x_last
        x_last = x_next
    results[round(float(T), 6)] = x_next
    return results


print(*[
    (str(k).rjust(10) + '|' + '|'.join(
        [str(round(i, 6)).rjust(10) for i in v]
    )) for k, v in func(0.001).items()], sep='\n')

ExprSystem, Expression, Variables, *_ = expr_system_builder()
ex_sys = ExprSystem(
    Expression(x1=-2, x2=1, x3=1, sign=Sign.equal, b=0),
    Expression(x2=-1, x3=2, x4=2, sign=Sign.equal, b=0),
    Expression(x3=-3, x4=4, sign=Sign.equal, b=0),
    Expression(x1=1, x2=1, x3=1, x4=1, sign=Sign.equal, b=1),

    solution_method=SolutionMethod.gauss_only,
)


ex_sys.run()

print('Конечный результат --------------------------')
print(ex_sys)
print([i.value for i in Variables.nodes_dict['b']])
'''
      20.0|  0.300358|  0.467223|  0.133492|  0.100119
'''