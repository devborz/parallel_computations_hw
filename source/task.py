from one_var_solution import *
from math import gcd

class MonomV2:
    def __init__(self, a, xi, yi) -> None:
        self.a = a
        self.xi = xi
        self.yi = yi
    
    def is_number(self):
        return self.xi == 0 and self.yi == 0
    
    def power(self):
        return self.xi + self.yi
    
    def print(self, end=' + '):
        str = f''
        if self.a == -1:
            str = '-'
        elif self.a == 0:
            str = ''
            return
        elif self.a == 1:
            str = ''
        else:
            str = f'{self.a}'
        
        if self.xi == 0:
            str += ''
        elif self.xi == 1:
            str += f'x'
        else:
            str += f'x^{self.xi}'

        if self.yi == 0:
            str += ''
        elif self.yi == 1:
            str += f'y'
        else:
            str += f'y^{self.yi}'
        print(str, end=end)


def find_free_coef(polynom: [MonomV2], var: str):
    coefs = []
    if var == "x":
        for el in polynom:
            if el.xi == 0:
                coefs.append(el)
    if var == "y":
        for el in polynom:
            if el.yi == 0:
                coefs.append(el)
    return coefs


def check_var_zero(polynom: [MonomV2], var: str):
    result = []
    if var == "x":
        for el in polynom:
            if el.xi == 0:
                result.append(el)
    elif var == "y":
        for el in polynom:
            if el.yi == 0:
                result.append(el)
    return len(result) == 0


def find_max_power_monoms(polynom: [MonomV2]):
    max = 0
    monoms = []
    for el in polynom:
        if el.power() > max:
            max = el.power()
            monoms = [el]
        elif el.power() == max:
            monoms.append(el)
    return monoms


def find_coefs_gcd(polynom: [MonomV2]):
    coefs = []
    for el in polynom:
        if el.a != 0:
            coefs.append(el.a)
    return gcd(*coefs)


def check_rational_root(polynom: [MonomV2], root: float, var: str):
    result = {}
    if var == "x":
        for el in polynom:
            new_monom = MonomV2(el.a * pow(root, el.xi), 0, el.yi)
            key = f'y{el.yi}'
            if key in result:
                result[key].a += new_monom.a
            else:
                result[key] = new_monom
    else:
        for el in polynom:
            new_monom = MonomV2(el.a * pow(root, el.yi), el.xi, 0)
            key = f'x{el.xi}'
            if key in result:
                result[key].a += new_monom.a
            else:
                result[key] = new_monom
    sum = 0
    for monom in result.values():
        if monom.is_number() or monom.a == 0:
            sum += monom.a
        else:
            return False
    return sum == 0


def find_rational_roots(polynom: [MonomV2], x_roots, y_roots):
    max_power_monoms = find_max_power_monoms(polynom)
    coefs_gcd = find_coefs_gcd(max_power_monoms)

    x_free_coefs = find_free_coef(polynom, "x")
    y_free_coefs = find_free_coef(polynom, "y")

    x_free_coefs_gcd = find_coefs_gcd(x_free_coefs)
    y_free_coefs_gcd = find_coefs_gcd(y_free_coefs)

    coefs_gcd_dividers = []
    x_free_coef_dividers = []
    y_free_coef_dividers = []

    find_number_dividers(coefs_gcd, coefs_gcd_dividers, False)
    find_number_dividers(x_free_coefs_gcd, x_free_coef_dividers)
    find_number_dividers(y_free_coefs_gcd, y_free_coef_dividers)

    for div1 in coefs_gcd_dividers:
        for div2 in x_free_coef_dividers:
            root = div2/div1
            if check_rational_root(polynom, root, "x"):
                x_roots.add(root)

    for div1 in coefs_gcd_dividers:
        for div2 in y_free_coef_dividers:
            root = div2/div1
            if check_rational_root(polynom, root, "y"):
                y_roots.add(root)


# def sort_polynom(plnm: [MonomV2], var: str):
#     polynom = plnm.copy()
#     if var == "x":
#         polynom = sorted(polynom, key=lambda x : (x.yi, -x.xi))
#     elif var == "y":
#         polynom = sorted(polynom, key=lambda x : (x.xi, -x.yi))
#     return polynom


# def divide_polynom_by_root(plnm: [MonomV2], root: float, var: str):
#     polynom = sort_polynom(plnm, var)
#     calculation = [polynom.pop(0), polynom.pop(0)]
#     result = []
#     while len(polynom) > 0 or len(calculation) > 0:
#         while len(calculation) < 2:
#             calculation.append(polynom.pop(0))
#         mult = MonomV2(calculation[0].a, calculation[0].xi, calculation[0].yi)
#         if var == "x":
#             mult.xi -= 1
#         else:
#             mult.yi -= 1
#         if calculation[1].xi == mult.xi and calculation[1].yi == mult.yi:
#             calculation[1].a -= -root * mult.a
#         else:
#             mult.a *= -root
#             calculation.append(mult)
#         calculation[0].a = 0
#         while calculation[0].a == 0:
#             calculation.pop(0)
#             if len(calculation) == 0:
#                 break
#         result.append(mult)
#     return result





start_time = datetime.datetime.now()

polynom_1 = [MonomV2(1, 1, 1), MonomV2(-3, 1, 0), MonomV2(2, 0, 1), MonomV2(-6, 0, 0)]
polynom_2 = [MonomV2(1, 1, 1), MonomV2(3, 1, 0), MonomV2(2, 0, 1), MonomV2(6, 0, 0)]
# polynom_2 = [MonomV2(1, 3, 0), MonomV2(-4, 2, 0), 
#              MonomV2(4, 1, 0), MonomV2(1, 2, 1), 
#              MonomV2(-4, 1, 1), MonomV2(4, 0, 1),]

print('Многочлен №1:')
for i in range(0, len(polynom_1)):
    if i == len(polynom_1) - 1:
        polynom_1[i].print('\n')
    else:
        polynom_1[i].print()
print('Многочлен №2:')
for i in range(0, len(polynom_2)):
    if i == len(polynom_2) - 1:
        polynom_2[i].print('\n')
    else:
        polynom_2[i].print()

# проверка на нулевые корни
polynom_1_x_zero = False
if check_var_zero(polynom_1, "x"):
    polynom_1_x_zero = True
    while check_var_zero(polynom_1, "x"):
        for el in polynom_1:
            el.xi -= 1

polynom_2_x_zero = False
if check_var_zero(polynom_2, "x"):
    polynom_2_x_zero = True
    while check_var_zero(polynom_2, "x"):
        for el in polynom_2:
            el.xi -= 1

polynom_1_y_zero = False
if check_var_zero(polynom_1, "y"):
    polynom_1_y_zero = True
    while check_var_zero(polynom_1, "y"):
        for el in polynom_1:
            el.yi -= 1

polynom_2_y_zero = False
if check_var_zero(polynom_2, "y"):
    polynom_2_y_zero = True
    while check_var_zero(polynom_2, "y"):
        for el in polynom_2:
            el.yi -= 1

if polynom_1_x_zero and polynom_2_x_zero:
    print("Корень: x = 0")

if polynom_1_y_zero and polynom_2_y_zero:
    print("Корень: y = 0")
        
polynom_1_x_roots = set()
polynom_1_y_roots = set() 

polynom_2_x_roots = set()
polynom_2_y_roots = set() 

threads = []
thread1 = threading.Thread(target=find_rational_roots, 
                           args=(polynom_1, polynom_1_x_roots, polynom_1_y_roots,))
thread2 = threading.Thread(target=find_rational_roots, 
                           args=(polynom_2, polynom_2_x_roots, polynom_2_y_roots,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Корни x:", list(polynom_1_x_roots.intersection(polynom_2_x_roots)))
print("Корни y:", list(polynom_1_y_roots.intersection(polynom_2_y_roots)))

end_time = datetime.datetime.now()
print(f'Время работы: {end_time - start_time}')






