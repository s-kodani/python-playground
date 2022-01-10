import factorize
import subprocess
from time import time
from concurrent import futures


def main():

    numbers = [2139079, 1214759, 1516637, 1852285, 1516637, 1214759, 1516637, 1852285, 2139079, 1214759, 1516637, 1852285]

    # ------------------------------------------------
    # 直列処理
    # ------------------------------------------------
    start = time()
    for number in numbers:
        result = factorize.factorize(number)
        # print(result)
    end = time()

    print('直列処理')
    print('Took %.3f seconds' % (end - start), end='\n\n')

    # ------------------------------------------------
    # ThreadPoolExecutor
    # ------------------------------------------------
    start = time()
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(factorize.factorize, numbers))

        # for result in results:
            # print(result)

    end = time()
    print('ThreadPoolExecutor')
    print('Took %.3f seconds' % (end - start), end='\n\n')

    # ------------------------------------------------
    # ProcessPoolExecutor
    # ------------------------------------------------
    start = time()
    with futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(factorize.factorize, numbers))

        # for result in results:
            # print(result)

    end = time()
    print('ProcessPoolExecutor')
    print('Took %.3f seconds' % (end - start), end='\n\n')


    # ------------------------------------------------
    # subprocess
    # ------------------------------------------------
    start = time()
    procs = []
    for number in numbers:
        proc = subprocess.Popen(['python', 'factorize_cmd.py', str(number)], stdout=subprocess.PIPE)
        procs.append(proc)

    for proc in procs:
        result, _ = proc.communicate()
        result = result.decode('utf-8')
        result = result.rstrip()
        # print(result)

    end = time()
    print('subprocess')
    print('Took %.3f seconds' % (end - start), end='\n\n')


if __name__ == '__main__':
    main()
