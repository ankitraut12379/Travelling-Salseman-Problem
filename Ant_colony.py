import numpy
import math
import Ant_Class
import random

from multiprocessing import Process, Queue

class AntColonyOptimization:
	def __init__(self,num_cities,initial_pheromone=1,alpha=1,beta=3,epsilon=0.1,pheromone_deposit=1,evaporation_constant=0.6):
		self.cities=[]
		self.shortest_paths=[]
		self.shortest_path_lengths=[]
		self.shortest_path_length=-1
		self.evaporation_constant=evaporation_constant
		self.pheromone_deposit=pheromone_deposit
		self.pheromone=numpy.full((num_cities,num_cities),initial_pheromone)
		self.alpha=alpha
		self.beta=beta
		self.attractiveness=numpy.zeros((num_cities,num_cities))
		self.epsilon=epsilon
		self.routing_table=numpy.full((num_cities,num_cities),(1.00/(num_cities-1)))


	def add_cities(self,city):
		if isinstance(city,list):
			self.cities.extend(city)
		else:
			self.cities.append(city)

	def calc_attraction(self):
		city_list=self.cities
		for i,c in enumerate(city_list):
			for j,d in enumerate(city_list):
				distance=self.calc_distance(c,d)
				if distance>0:
					self.attractiveness[i][j]=1/distance
				else:
					self.attractiveness[i][j]=0

	def update_pheromone(self,a):
		for i in range(0,len(a.path)-1):
			#print("Success",a.index,i)
			#curr_pher=self.pheromone[a.path[i].index][a.path[i+1].index]
			self.pheromone[a.path[i].index][a.path[i+1].index] += self.pheromone_deposit/a.path_length

		self.pheromone=self.pheromone*(1-self.evaporation_constant)

	def get_pheromone(self,i,j):
		return self.pheromone[i][j]

	def update_routing_table(self,a):
		for c in a.path:
			temp_cities=list(a.path)
			temp_cities.remove(c)
			for t_c in temp_cities:
				numerator=self.city_sum(c,t_c)
				denom=0
				other_temp_cities=list(temp_cities)
				other_temp_cities.remove(t_c)
				for o_tc in other_temp_cities:
					denom=denom+self.city_sum(c,o_tc)
				if denom>0:
					self.routing_table[c.index][t_c.index]=numerator/denom
				else:
					self.routing_table[c.index][t_c.index]=0
	def city_sum(self,city_x,city_y):
		x=math.pow(self.pheromone[city_x.index][city_y.index],self.alpha)
		y=math.pow(self.attractiveness[city_x.index][city_y.index],self.beta)
		return x*y

	def get_best_path(self,num_ants=1,num_steps=3):
		Number_of_Cities=len(self.cities)
		Number_of_Ants=num_ants
		Number_Steps=num_steps
		self.calc_attraction()
		ants=[]

		for i in range(0,Number_of_Ants):
			ants.append(Ant_Class.Ant(i,self))

		for i in range(0,Number_Steps):
			print("Step : ",i+1,"of",Number_Steps)
			path_lengths=[]
			paths=[]

			processList=[]

			Q=Queue()

			for a in ants:
				p=Process(target=self.TOUR,args=(a,Q,))
				processList.append(p)
				p.start()

			for process in processList:
				process.join()

			ants=[]
			while Q.empty()==False:
				ants.append(Q.get())

			for a in ants:
				print(a.index)
				path_length=a.Calculate_path_Length()
				path_lengths.append(path_length)
				paths.append(a.path)
				self.update_pheromone(a)
				self.update_routing_table(a)
			best_path_len=min(path_lengths)
			best_path=paths[path_lengths.index(best_path_len)]

			print("step best path : ",best_path_len," step: ",i+1)

			self.shortest_paths.append(best_path)
			self.shortest_path_lengths.append(best_path_len)

		output_index=self.shortest_path_lengths.index(min(self.shortest_path_lengths))
		output_path=self.shortest_paths[output_index]
		self.shortest_path_length=self.shortest_path_lengths[output_index]
		self.shortest_paths=[]
		self.shortest_path_lengths=[]

		return output_path

	def calc_distance(self,city1,city2):
		distance=math.sqrt(math.pow((city1.index-city2.x),2)+math.pow((city1.y-city2.y),2))
		return distance

	def TOUR(self,ant,Q):
		ant.reset_ant(self)
		while(ant.unvisited):
			if random.random()<self.epsilon:
				next_city=ant.unvisited.pop(random.randint(0,len(ant.unvisited)-1))
				ant.path.append(next_city)
				ant.currCity=next_city

			else:
				for a in ant.unvisited:
					ant.transition_probs.append(ant.get_transition_probability(self,a))
				selection=numpy.random.choice(ant.unvisited,1,p=ant.transition_probs)
				next_city=selection[0]
				ant.path.append(next_city)
				ant.currCity=next_city
				ant.unvisited.pop(ant.unvisited.index(next_city))
			ant.transition_probs=[]

		Q.put(ant)

class City:
	def __init__(self,i,x_coordinate,y_coordinate=0,prob=0):
		self.index=i
		self.x=x_coordinate
		self.y=y_coordinate
		

			






