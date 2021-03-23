import matplotlib.pyplot as plt 
import numpy as np
x = [15/300, 30/300, 45/300, 60/300, 75/300, 90/300, 105/300, 120/300, 135/300, 150/300, 165/300, 180/300, 195/300, 210/300, 225/300, 240/300, 255/300, 270/300, 285/300]
y = [0.879, 0.875, 0.863, 0.820, 0.79, 0.758, 0.727, 0.699, 0.684, 0.654, 0.633, 0.611, 0.599, 0.582, 0.559, 0.553, 0.537, 0.52, 0.494]
z = [0.912, 0.917, 0.902, 0.87, 0.843, 0.808, 0.794, 0.776, 0.759, 0.750, 0.734, 0.726, 0.714, 0.704, 0.695, 0.687, 0.680, 0.669, 0.663]
q = [0.834, 0.832, 0.801, 0.739, 0.665, 0.528, 0.580, 0.542, 0.515, 0.482, 0.457, 0.433, 0.411, 0.384, 0.368, 0.353, 0.335, 0.331, 0.317]
r = [0.897, 0.884, 0.874, 0.819, 0.786, 0.757, 0.727, 0.701, 0.679, 0.656, 0.633, 0.616, 0.605, 0.582, 0.565, 0.552, 0.535, 0.521, 0.501]



plt.plot(x, z, label = "Advanced Agent (Enhanced)")
plt.plot(x, y, label = "Basic Agent (Enhanced")
plt.plot(x, q, label = "Basic Agent (Random)")
plt.plot(x, r, label = "Advanced Agent (Random)")
plt.xlabel(' Density (Percentage of Mines vs Total Cells) ')
plt.ylabel(' Total Score (Percentage of Flagged Mines vs Total Mines)')

plt.title('Mine Density vs Avg Final Score (Both Selections)')
plt.xticks(np.arange(0, 1, 0.1))
plt.yticks(np.arange(0.2, 1, 0.1))
plt.legend()



plt.show()