from multiprocessing import Pool

def do_something(number):
    return number ** 2

number_of_workers = 10
array_of_numbers = [x for x in range(0, 100000)]
with Pool(number_of_workers) as p:
    print(p.map(do_something, array_of_numbers))
