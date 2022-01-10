import sys

def factorize_cmd(number):
    f_list = []
    for i in range(1, number + 1):
        if number % i == 0:
            print(i)
            f_list.append(i)

    print(f_list)

    return


if __name__ == '__main__':
    number_str = sys.argv[1]
    factorize_cmd(int(number_str))