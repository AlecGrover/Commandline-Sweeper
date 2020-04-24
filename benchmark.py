import time 

def averageList(nums):
    sums = 0
    for i in nums:
        sums = sums + i 
    avg = sums / len(num)    
    return avg


def main():
    timeList = []
    failCount = 0
    passCount = 0 


    start = time.time()

    # Run tests 


    '''
    After the algorithm is finished 
    If we hit a bomb: 
        failCount += 1
    else:
        passCount += 1 
    '''
    end = time.time()


    execTime = end - start 
    execTime = round(execTime, 2)
    timeList.append(execTime)

    avg = averageList(timeList)




if __name__ == "__main__":
    main()