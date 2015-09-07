import collections,re,sys,time,os,random,numpy,math
class ProteinFoldingProblem:
	def __init__(self, HPsequence, numIteration):
		self.HPsequence = HPsequence
		self.numIteration = numIteration
		self.numAcids = len(HPsequence)
		self.availableDirection = ["1","-1","i","-i"]
	def randomState(self):
		
		confirmation = ["1" for x in range(self.numAcids-1)]
		while(True):
			for i in range(0, self.numAcids-1):
				confirmation[i] = random.choice(self.availableDirection)
			if (not self.isConflict(confirmation)):
				return confirmation
	def getNeighbors(self, confirmation):
		neighbors = []
		for i in range(0,len(confirmation)):
			newConf = confirmation[:]
			candidates = [y for y in self.availableDirection if y!=confirmation[i]]
			#print(confirmation[i], candidates)
			for k in candidates:
				newConf[i] = k
				if (not self.isConflict(newConf)):
					newnewConf = newConf[:]
					neighbors.append(newnewConf)			
		return neighbors

	def calLocationVec(self, confirmation):
		locationVec =[(0,0)]
		locAccDic={"1":(1,0), "-1":(-1,0),"i":(0,1),"-i":(0,-1)}
		for x in confirmation:
			preLoc = locationVec[-1]
			locAcc = locAccDic[x]
			locationVec.append((preLoc[0]+locAcc[0], preLoc[1]+locAcc[1]))
		return locationVec
		
	def isConflict(self, confirmation):
		locVec = self.calLocationVec(confirmation)
		return len(set(locVec)) < len(locVec)

	def qualityFunc(self, confirmation):
		locationVec = self.calLocationVec(confirmation)
		redLocs = [i for (i,e) in enumerate(self.HPsequence) if e]
		l = len(redLocs)
		cost = 0
		for i in range(0, l):
			for j in range(i+1,l):
				(x1, y1) = locationVec[redLocs[i]]
				(x2, y2) = locationVec[redLocs[j]]
				cost = cost + math.sqrt( (x1-x2)*(x1-x2)+ (y1-y2)*(y1-y2) )
		# negate the cost value to reflect its quality 
		return -cost


class HillClimbingWithSteepest:
	def __init__(self, epsilon, pathLength, verbose=0):
		self.verbose = verbose
		self.averagePathLength=0
		self.epsilon = epsilon
		self.pathLength = pathLength

	def solve(self, problem):
		solution = problem.randomState()
		solutionQuality = problem.qualityFunc(solution)
		if (self.verbose >=1):
			print("The random solution is "+str(solution)+" with quality "+str(solutionQuality))
		totalStatesExplored = 0
		for x in range(0, problem.numIteration):
			if (self.verbose >=1 ):
				print("=========== Round "+str(x)+" ===========")
			current = problem.randomState()
			currentQuality = problem.qualityFunc(current)
			numStatesExplored = 0
			while(True):
				numStatesExplored = numStatesExplored+1
				neighbors = problem.getNeighbors(current)
				
				if (len(neighbors)==0):
					break;
				neighborsWithQuality = map(lambda x: (x, problem.qualityFunc(x)), neighbors)
				#print(neighborsWithQuality)
				(maxNeighbor, maxQuality) = max(neighborsWithQuality, key = lambda (x,y):y)
				if (maxQuality > currentQuality or abs(maxQuality-currentQuality) < self.epsilon):
					current = maxNeighbor
					currentQuality = maxQuality					
				elif(numStatesExplored < self.pathLength):
					(current,currentQuality) = random.choice(neighborsWithQuality)
				else:
					break;
			if(currentQuality > solutionQuality):
				solution = current
				solutionQuality = currentQuality
				if (self.verbose >=1):
					print("Find a better solution "+ str(solution)+" quality "+ str(solutionQuality))
					print("New State:")
					self.display(problem.calLocationVec(solution), problem.HPsequence)
			totalStatesExplored = totalStatesExplored+ numStatesExplored
		self.averagePathLength = totalStatesExplored/problem.numIteration		
		print("Final solution "+ str(solution)+" quality "+ str(solutionQuality))
		#self.display(problem.calLocationVec(solution), problem.HPsequence)
		return (solution, -solutionQuality)

	def display(self, locVec, HPsequence):
		m=len(locVec)
		n = 2*(m+1)
		panel = [["*" for x in range(n)] for x in range(n) ]
		for (i,loc) in enumerate(locVec):
			if (HPsequence[i]==1):
				panel[loc[0]+m-1][loc[1]+m-1] = "1"
			else:
				panel[loc[0]+m-1][loc[1]+m-1] = "0" 
		for x in panel:
			print x



		




