from numpy import array,zeros,shape,loadtxt,savetxt,arange,mean,histogram,ones,dot,random,hstack,reshape,cumsum,around
import numpy as np
from gaussianPDF2 import *
import sys

if len(sys.argv)!=2:
	print "Please type python latentProb.py <input filename>"
	sys.exit()

numIterLC = 0
numLatentClass=2
numIteration=50
for countFile in range(1):
	filename=sys.argv[1]
	#filename='business_word_matrix_100.txt'
	#filename="businesstest.txt"
	if filename=='u1.base':
		M=loadtxt(filename,delimiter="	")
	else:
		M=loadtxt(filename,delimiter=" ")
	meta=np.max(M,axis=0)
	numUser=int(meta[0])
	numMovie=int(meta[1])
	(numRow, numCol) = shape(M)
	ratings=zeros((numUser,numMovie))
	for i in range(numRow):
		ratings[M[i][0]-1][M[i][1]-1]=M[i][2]	

	meanUser = mean(ratings,1)
	numRatingUser=np.sum(ratings!=0,axis=1)
	meanUser = np.sum(ratings,axis=1) / numRatingUser
	normalizingratings=((ratings-meanUser.reshape(numUser,1))**2)*array(ratings!=0)
	VarUser=np.sum(normalizingratings,axis=1)/np.sum(ratings!=0,axis=1)
	stdUser = (VarUser)**0.5
		
	origRatings = ratings.copy()

	ratings=(ratings-meanUser.reshape((numUser,1)))/stdUser.reshape((numUser,1))
	Q = random.rand(numUser, numMovie, numLatentClass);
	Q[:][:,:][:,:,0]=Q[:][:,:][:,:,0]/np.sum(Q,axis=2)
	Q[:][:,:][:,:,1]=Q[:][:,:][:,:,1]/np.sum(Q,axis=2)
	#Q=Q/np.sum(Q,axis=2).reshape((numUser, numMovie, numLatentClass))
	
	A=random.rand(numUser,2)
	B= np.sum(A,axis=1)		
	B=B.reshape((shape(B)[0],1))	
	C=ones((1,numLatentClass))
	D=dot(B,C)
	Pzu = A / D;
	Ms=random.rand(numMovie,2)
	Ss=random.rand(numMovie,2)
	M_yz = Ms*2-1
	Std_yz = 3*Ss+1	

	for i in range(numIteration):
		#print "iteration",i 
			#-----------------------------------------------#
			#  Expectation step
			#----------------------------------------------#
			#--------------------------------------#
			#  1.Calculate Q
			#--------------------------------------#
		PreviousQ=Q.copy()
		for countUser in range(numUser):
			for countItem in range(numMovie):
				down=0
				if (origRatings[countUser][countItem]!=0):
					for countLC in range(numLatentClass):
						up=Pzu[countUser][countLC]*gaussianPDF2(ratings[countUser][countItem],M_yz[countItem][countLC],Std_yz[countItem][countLC]);
						down=down+up
						if up==0:
							print "Q is 0"
						Q[countUser][countItem][countLC]=up
					if down!=0:
						Q[countUser][countItem][:] = Q[countUser][countItem][:]/down
		#Check That Q has been updated correctly
		#print "Q"
		#print Q[:10][:,:10][:,:,0]

			#-----------------------------------------------#
			#  Mazimization step
			#----------------------------------------------#
			#--------------------------------------#
			#  1.Calculate M_yz
			#--------------------------------------#
		PreviousM = M_yz.copy();
		for countItem in range(numMovie):
			for countLC in range(numLatentClass):
				down=0
				up=0
				for countUser in range(numUser):
					if (origRatings[countUser][countItem]!=0):
						up+=ratings[countUser][countItem]*Q[countUser][countItem][countLC]
						down+=Q[countUser][countItem][countLC]
				#Normalize for all users	
				if down!=0:
					M_yz[countItem][countLC]=up/down
				else:
					M_yz[countItem][countLC]=0
		#print "M"
		#print M_yz[:5][:5]

			#--------------------------------------#
			#  2.Calculate Std_yz
			#--------------------------------------#
		PreviousStd=Std_yz.copy()
		for countItem in range(numMovie):
			for countLC in range(numLatentClass):
				down=0
				tempup=0
				for countUser in range(numUser):
					if (origRatings[countUser][countItem]!=0):
						tempup+=(ratings[countUser][countItem]-PreviousM[countItem][countLC])**2*Q[countUser][countItem][countLC]
						down+=Q[countUser][countItem][countLC]

				if down==0:
					Std_yz[countItem][countLC]=1
				
				elif tempup/down>0.1:
					Std_yz[countItem][countLC]=(tempup/down)**0.5
				#Standard Saturation				
				else:
					Std_yz[countItem][countLC]=0.5
		#print "Std_yz"
		#print Std_yz[:5][:5]

			#--------------------------------------#
			#  3.Calculate Pzu
			#--------------------------------------#
		PreviousPzu=Pzu.copy()
		for countUser in range(numUser):
			down=0		
			for countLC in range(numLatentClass):
				up=0	
				for countItem in range(numMovie):
					if (origRatings[countUser][countItem]!=0):
						up+=Q[countUser][countItem][countLC]
						down+=Q[countUser][countItem][countLC]
				Pzu[countUser][countLC] = up
			Pzu[countUser][:] = Pzu[countUser][:]/down;
		#print "Pzu"
		#print Pzu[:5][:5]
		#print shape(Pzu)
		
	finalprob=hstack((cumsum(ones(shape(Pzu)[0])).reshape(shape(Pzu)[0],1),Pzu))
	savetxt("output_"+filename,finalprob, delimiter=",", fmt='%.5f')
	


			
	
	






