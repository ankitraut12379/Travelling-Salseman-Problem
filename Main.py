import random
import math
import matplotlib.pyplot as plot
import Ant_colony

number_of_cities=int(input(" Enter the number of cities : "))
X=int(input(" Enter the X range : "))
Y=int(input(" Enter the Y range : "))
increment=360.0/number_of_cities

aco=Ant_colony.AntColonyOptimization(number_of_cities,initial_pheromone=1,alpha=1,beta=3,epsilon=0,pheromone_deposit=2,evaporation_constant=0.6)

for i in range(0,number_of_cities):
	#aco.add_cities(Ant_colony.City(i,random.uniform(0,X)),(i,random.uniform(0,X)))
	angle=i*increment
	print(i,math.sin(math.radians(angle)),math.cos(math.radians(angle)))
	aco.add_cities(Ant_colony.City(i,math.sin(math.radians(angle)),math.cos(math.radians(angle))))
number_of_ants=int(input("Enter the number of Ants : "))
number_of_iterations=int(input("Enter the iterations : "))
shortest_path=aco.get_best_path(num_ants=number_of_ants,num_steps=number_of_iterations)

print("Shortest route found : ",aco.shortest_path_length)

plot.figure(1)

plot.margins(0.1,0.1)

for i,c in enumerate(aco.cities):
	if i==0:
		plot.plot(c.x,c.y,'go')
	else:
		plot.plot(c.x,c.y,'bo')
for i in range(0,len(shortest_path)-1):
	plot.plot([shortest_path[i].x,shortest_path[i+1].x],[shortest_path[i].y,shortest_path[i+1].y],'c-',linewidth=2.0,alpha=0.4)


plot.show()