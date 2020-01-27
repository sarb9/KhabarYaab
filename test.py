import matplotlib.pyplot as plt
import heapq

import re

str = "cat:milad  "
category = re.search("cat:", str.strip())
print(type(category))
print(str[category.end() :])
print((category.end()))
