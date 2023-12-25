from math import sqrt, pow, ceil
import threading
import datetime

class Monom:
    def __init__(self, a, xi) -> None:
        self.a = a
        self.xi = xi


    def is_number(self):
        return self.xi == 0


def find_polynom_max_power_coef(polynom):
    max_power = 0
    coef = 0
    for monom in polynom:
        if monom.xi > max_power:
            max_power = monom.xi
            coef = monom.a
        elif monom.xi == max_power:
            coef += monom.a
    return coef


def find_polynom_free_coef(polynom):
    coef = 0
    for monom in polynom:
        if monom.xi == 0:
            coef += monom.a
    return coef


def find_number_dividers(number, dividers, neg = True):
    for i in range(1, number + 1):
        n = number
        while n % i == 0:
            n /= i
            dividers.append(i)
            if neg:
                dividers.append(-i)
            if i == 1:
                break


def check_polynom(polynom, value, roots):
    sum = 0
    for monom in polynom:
        sum += monom.a * pow(value, monom.xi)
    if sum == 0:
        roots[value] = 0


def find_roots(polynom):
    roots = {}
    max_coef = find_polynom_max_power_coef(polynom)
    free_coef = find_polynom_free_coef(polynom)

    start_time = datetime.datetime.now()

    max_coef_dividers = []
    free_coef_dividers = []
    max_coef_thread = threading.Thread(target=find_number_dividers, 
                                       args=(max_coef, max_coef_dividers,))
    
    free_coef_thread = threading.Thread(target=find_number_dividers, 
                                       args=(free_coef, free_coef_dividers,))
    max_coef_thread.start()
    max_coef_thread.join()
    free_coef_thread.start()

    free_coef_thread.join()

    threads = []
    for div1 in max_coef_dividers:
        for div2 in free_coef_dividers:
            thread = threading.Thread(target=check_polynom, 
                                      args=(polynom, div2/div1, roots,))
            threads.append(thread)
            thread.start()
            thread.join()

    end_time = datetime.datetime.now()
    print(end_time - start_time)

    return list(roots.keys())

