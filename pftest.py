import pf,time
time_start = time.time()
pfprob = pf.ProteinFoldingProblem([1,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0,1,1], 1000)
#print ("calLocationVec: ", pfprob.calLocationVec(["-i","-i","-i","-i","-i"]))
#print pfprob.getNeighbors(["-i","-i","-i","-i","-i"])
alg = pf.HillClimbingWithSteepest(1e-3,599, 0)
alg.solve(pfprob)
print("-----time elapsed(minutes):", (time.time()-time_start)/60)
