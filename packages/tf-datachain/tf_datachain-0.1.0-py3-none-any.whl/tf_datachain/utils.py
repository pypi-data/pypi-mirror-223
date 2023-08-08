import os
import random
import numpy as np
from keras_cv import visualization

def split(list: list, *args, shuffle=True):
    resultList = []
    lastSplitPoint = 0
    
    if shuffle:
        random.shuffle(list)
    
    total = sum(args)
    for i in range(len(args)):
        thisSplitPoint = int(len(list) * sum(args[:i+1]) / total)
        resultList.append(list[lastSplitPoint:thisSplitPoint])
        lastSplitPoint = thisSplitPoint
    
    return tuple(resultList)

