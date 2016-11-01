import math
import random
import matplotlib.pyplot as plt

# 1. Generate a random number sequence of 10 values between 0 to 90.
randoms = random.sample(range(0,90), 10)
randoms.sort()
print(randoms)

# 2. Perform sine and cosine operation on numbers generated.
# 3. Store the values in two different arrays named SIN & COSIN respectively.
SIN = list(map(math.sin, randoms))
COSIN = list(map(math.cos, randoms))
print(SIN)
print(COSIN)

# 4. Plot the values of SIN & COSIN in two different colors.
# 5. The plot should have labeled axes and legend.
plt.scatter(randoms, SIN, label="sin", color="red")
plt.scatter(randoms, COSIN, label="cos", color="teal")
plt.ylabel('Value of Sin/Cos')
plt.xlabel('Number')
plt.legend()
plt.show()





