def factorize(number):
    f_list = []
    for i in range(1, number + 1):
        if number % i == 0:
            print(i)
            f_list.append(i)

    return f_list
