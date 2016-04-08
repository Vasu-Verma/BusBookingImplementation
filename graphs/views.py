from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import Edges,Vertices,Bus
from forms import MyForm
import itertools


Stops = []


class Vertex:
	def __init__(self, node):
		self.id = node
		self.adjacent = {}
		
	def __str__(self):
		return str([x.id for x in self.adjacent])
	
	def add_neighbor(self, neighbor, weight=0):
		self.adjacent[neighbor] = weight
	
	def get_connections(self):
		return self.adjacent.keys()  
	
	def get_id(self):
		return self.id
	
	def get_weight(self, neighbor):
		return self.adjacent[neighbor]

class Graph:
	def __init__(self):
		self.vert_dict = {}
		self.num_vertices = 0

	def __iter__(self):
		return iter(self.vert_dict.values())

	def add_vertex(self, node):
		self.num_vertices = self.num_vertices + 1
		new_vertex = Vertex(node)
		self.vert_dict[node] = new_vertex
		return new_vertex

	def get_vertex(self, n):
		if n in self.vert_dict:
			return self.vert_dict[n]
		else:
			return None

	def add_edge(self, frm, to, cost ):
		if frm not in self.vert_dict:
			self.add_vertex(frm)
		if to not in self.vert_dict:
			self.add_vertex(to)

		self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
		self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

	def get_vertices(self):
		return self.vert_dict.keys()

class NewPath:
	def __init__(self, path, weight, bus, checkpoints, Graph, Adults, Children):
		self.path = path
		self.weight = weight
		self.bus = bus
		self.checkpoints = checkpoints
		self.Graph = Graph
		self.Adults = Adults
		self.Children = Children
		self.listA = zip()


	def zip(self):
		dict = {}
		i = 0
		listA = []

		for buses in self.bus:
			list2 = []
			list2.append(buses.Number)
			list2.append(self.checkpoints[i])
			list2.append(self.checkpoints[i+1])
			for v in self.Graph:
				if(v.get_id()==self.checkpoints[i]):
					for w in v.get_connections():
						if(w.get_id()==self.checkpoints[i+1]):
							list2.append(v.get_weight(w))
			if(list2[3]>0 and list2[3]<=4):
				list2.append(5)
				list2.append(3)
			elif(list2[3]>4 and list2[3]<=10):
				list2.append(10)
				list2.append(5)
			elif(list2[3]>10):
				list2.append(15)
				list2.append(8)

			listA.append(list2)
			i = i + 1
		sum = 0
		sum2=0
		for listitem in listA:
			sum = sum+listitem[4]
			sum2 = sum2+listitem[5]
		listA.append(sum*int(self.Adults)+sum2*int(self.Children))
		print listA
		return listA

def find_all_paths(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return [path]
	if not graph.has_key(start):
	    return []
	paths = []
	for node in graph[start]:
		if node not in path:
			newpaths = find_all_paths(graph, node, end, path)
			for newpath in newpaths:
				paths.append(newpath)
	return paths

def FindBusCombinations(Path,Buses,BusCombination,Stops):
	if(len(Path)==1):
		# print 1
		# print BusCombination
		return BusCombination
	else:
		# print BusCombination
		List = BusCombination[0::]
		k = 1
		Busk =  Buses[0]
		BusDB = []
		for Bus2 in Buses:
			temp = Bus2.Path.split(",")
			i=0
			BusDB = []
			flag=0
			k = 0
			# print Path[0],Path[1]
			for i in range(0,len(temp)-1):
				# print "Temps",temp[i],temp[i+1]
				if(temp[i]==Path[0] and temp[i+1]==Path[1]):
					flag=1
					j=i
					# print Path,Bus2.Number
					break
					# BusDB.append(Bus2.Number)
			i=0
			# print flag
			# print "yolo"
			if(flag==1):
				while(i<len(Path) and j<len(temp) and temp[j] == Path[i]):
					i = i+1
					j = j+1
				if(i>k):
					k = i
					Busk = Bus2
		# print "k",k
		if k<=1:
			# print 2
			return []
		RemStations = Path[k-1::]
		List.append(Busk)
		# print "YOLO", RemStations
		# print 3
		# print List
		# print RemStations
		Stops.append(RemStations[0])
		return FindBusCombinations(RemStations,Buses,List,Stops)
	

def homepage(request):
	g = Graph()
	Vertex = Vertices.objects.all()
	Buses = Bus.objects.all()
	for node in Vertex:
		g.add_vertex(node.name)

	Edge = Edges.objects.all()
	for road in Edge:
		g.add_edge(road.Vertex1,road.Vertex2,road.Weight)
	dist = []
	DICT = {}
	for v in g:
		x = g.vert_dict[v.get_id()]
		DICT[v.id] = eval(str(x))
	PATHS = []

	if request.method == 'POST':
		form = MyForm(request.POST)
		A = request.POST.get('dropdown')
		B = request.POST.get('dropdown2')
		C = request.POST.get('Adult')
		D = request.POST.get('Children')
		print D
		x = find_all_paths(DICT,A,B)
		if(D==None):
			D = 0
		print D


		i = 0
		PATHS = []
		BusDatabase =[]
		for path in x:
			Stops = []
			sum = 0
			dest = path[0]
			for i in range (1,len(path)):
				init = dest
				dest = path[i]
				for v in g:
					if(v.get_id()==init):
						for w in v.get_connections():
							if(w.get_id()==dest):
								sum = sum + v.get_weight(w)
			BusDatabase = []
			# for Bus2 in Buses:
			# 	temp = Bus2.Path.split(",")
			# 	i=0
			# 	BusDB = []
			# 	if(temp == path):
			# 		BusDB.append(Bus2.Number)
			# 		BusDatabase.append(BusDB)
			BusDB = []
			if(len(path)>1):
				BusDatabase = []
				Busk = Buses[0]
				k = 0
				for Bus2 in Buses:
					# print Bus2.Number
					temp = Bus2.Path.split(",")
					i=0
					BusDB = []
					flag=0
					# print temp
					for i in range(0,len(temp)-1):
						# print temp
						# print i
						if(temp[i]==path[0] and temp[i+1]==path[1]):
							flag=1
							# print path,Bus2.Number
							j=i
							# print path,Bus2.Number
							break
							# BusDB.append(Bus2.Number)
					i=0

					if(flag==1):
						while(i<len(path) and j<len(temp) and temp[j] == path[i]):
							i = i+1
							j = j+1
						if(i>=k):
							k = i
							Busk = Bus2
							# print k
				Stops.append(path[0])
				Stops.append(path[k-1])
				RemStations = path[k-1::]
				# print RemStations
				BusDB.append(Busk)
				BusComb = []
				# print path,"BUSKY: " + Busk.Number, k
				BusDB =  BusDB + FindBusCombinations(RemStations,Buses,BusComb,Stops)
			# print "BUS",BusDB 
			if(BusDB!=[] and BusDB[-1].Path.split(",")[-1]==path[-1]):
				BusDatabase = BusDB
			else:
				BusDatabase = []
			# print Stops
			PATHS.append(NewPath(path,sum,BusDatabase,Stops,g,C,D))


			context = {
				"text":"Showing Route From " + A + " to "  + B,
				"Method2":"POST",
				"Paths":PATHS,
				"Adults":C,
				"Children":D,
			}
	else:
		Vertex = Vertices.objects.all()
		Vertex2 = []
		for node in Vertex:
			Vertex2.append(node.name)
		form = MyForm()
		context = {
			"form":form,
			"Vertex":Vertex2,
		}

	return render(request,"home.html",context)

# Create your views here.
