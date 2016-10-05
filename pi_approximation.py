import decimal
import multiprocessing
import argparse


def get_args():
    parser = argparse.ArgumentParser("The given script calculates the value "
            "of pi upto a fixed decimal place using the specified number of " 
            "terms of the infinite series according to the Newton Euler"
            "conjecture")
    parser.add_argument('-t', '--terms', type=int, help="No of terms", required=True)
    parser.add_argument('-d', '--decimal', type=int, help="No. of decimal place of the output", required=True)
    args = parser.parse_args()

    return args.terms, args.decimal

def factorial(num, isOddFactorial = False):
    
    total = 1
  
    if num == 0:
        return total

    step = 1
    if isOddFactorial:
        step = 2

    for x in xrange(1,num+1, step):
        total *= x

    return total

def processInput(num):
    # Using Newton-Euler Conjecture for approximating the value of PI
    # PI/2 = Sum from k = 0 to infinity of (k!/(2k+1)!!)
    return  2*decimal.Decimal(factorial(num, isOddFactorial = False))/decimal.Decimal(
            factorial(2*num+1, isOddFactorial = True))
       

def main():
    terms, decimal_place = get_args()
    decimal.getcontext().prec = decimal_place
    
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    
    # Calculating  terms of the infinite series depending on the input
    tasks = [(x,) for x in xrange(terms)]

    # Applying the same function across different cores for the given tasks.
    results = [pool.apply_async(processInput, t) for t in tasks]

    val = 0

    for result in results:
         val += result.get()

    print format(val, '.%sf' % decimal_place)

if __name__ == "__main__":
    main()

    
