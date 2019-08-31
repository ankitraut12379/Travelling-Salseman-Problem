import math
import random
import numpy

numpy.warnings.filterwarnings("ignore",category=RuntimeWarning)

class Ant:
	def __init__(self,i,ACO):
		self.index=i
		self.path_length=0
		self.currCity=ACO.cities[0]
		self.path=[]
		self.path.append(ACO.cities[0])
		self.unvisited=[]
		self.unvisited.extend(ACO.cities[1:])
		self.transition_probs=[]

	def reset_ant(self,ACO):
		self.path_length=0
		self.currCity=ACO.cities[0]
		self.path=[]
		self.path.append(ACO.cities[0])
		self.unvisited=[]
		self.unvisited.extend(ACO.cities[1:])
		self.transition_probs=[]

	def get_transition_probability(self,ACO,city_next):
		b=0
		a=ACO.routing_table[self.currCity.index][city_next.index]
		for c in self.unvisited:
			b=b+ACO.routing_table[self.currCity.index][c.index]
		transition_probability=a/float(b)
		return transition_probability

	def city_sum(self,ACO,city_X,city_Y):

		return(math.pow(ACO.phermone[city_X.index][city_Y.index],ACO.alpha) *  math.pow(ACO.attractiveness[city_X.index][city_Y.index],ACO.bet))

	def Calculate_path_Length(self):
		sum_of_distances=0.0
		for i in range(0,len(self.path)-1):
			distance=math.sqrt(math.pow(self.path[i].x-self.path[i+1].x,2.0) + math.pow(self.path[i].y-self.path[i+1].y,2.0))
			sum_of_distances=sum_of_distances+distance
		distance=math.sqrt(math.pow(self.path[len(self.path)-1].x-self.path[0].x,2) + math.pow(self.path[len(self.path)-1].y-self.path[0].y,2.0))
		self.path_length=sum_of_distances+distance
		return sum_of_distances