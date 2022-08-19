from time import sleep

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def UpdateProgress(i, length):
     # print progress
    modu = round(length/100)
    if modu == 0:
        modu = 1
    if not (i+1)%modu:
        printProgressBar(i+1,length,'',str(i+1) + '/' + str(length) + ' extra tiles', length = 20)
    elif i+1 == length:
        printProgressBar(i+1,length,'',str(i+1) + '/' + str(length) + ' extra tiles', length = 20)




# # exemple

# # A List of Items
# items = list(range(0, 57))
# l = len(items)

# # Initial call to print 0% progress
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, item in enumerate(items):
#     # Do stuff...
#     sleep(0.1)
#     # Update Progress Bar
#     printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)