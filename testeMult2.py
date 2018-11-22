import os
	
def doTheJob(job,state):
	for i in range(100000):
		print (job, i)
	state = True
	return state


jobs = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
imTheFather = True
children = []

for job in jobs:
	child = os.fork()
	if child:
		children.append(child)
		print (children)
	else:
    		imTheFather = False
		estado=doTheJob(job,True)
		if (estado):
			print("retornou_verdadeiro")
		break
if imTheFather:
	for child in children:
		os.waitpid(child, 0)

