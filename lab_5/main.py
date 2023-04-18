import os

from lab_5.gauss.labs_2_3_and_4.enums import SolutionMethodMods, Sign, ExprType, SolutionMethod, VRole
from lab_5.gauss.labs_2_3_and_4.builder import expr_system_builder


def eller_m(last_y, h, y):
    return last_y + h * y


def func(
        h,
        T=10
):
    h = float(h)
    x_last = [0, 0, 0, 1]
    x_next = [0] * 4
    results = {float(0): x_last}
    for t in (i * h for i in range(round(T / h))):
        x_next = [0] * 4
        x_next[0] = eller_m(x_last[0], h, x_last[1] + x_last[2] - 2 * x_last[0])
        x_next[1] = eller_m(x_last[1], h, 2 * x_last[2] + 2 * x_last[3] - 1 * x_last[1])
        x_next[2] = eller_m(x_last[2], h, 4 * x_last[3] - 3 * x_last[2])
        x_next[3] = eller_m(x_last[3], h, 2 * x_last[0] - 6 * x_last[3])
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
