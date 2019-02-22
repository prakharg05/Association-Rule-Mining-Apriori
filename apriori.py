import itertools

masterFrequentItemSets=[]
supDict={}
finalRule=[] #Hashable data structure which maps any and all frequent itemsets to its support count.
'''
'''
def load_data(path):
	transactions=[]
	with open(path) as f:
		dataset=f.readlines()

	for line in dataset:
		transactions.append(sorted(line.strip().split(",")))

	return transactions

'''
This function recursively calculates all frequent itemsets of all cardinality
starting from 2 by calculating their support and comparing it
against the minimum given support.
'''

def generateFrequentItemSets(candidateFrequentItemSets,dataset,minSupport,T):
	
	frequentItemSets=[]

	for itemset in candidateFrequentItemSets:
		c=0
		for data in dataset:
			# print(itemset)
			item=set(tuple(itemset))
			# print(item)
			if(item.issubset(set(data))):
				c+=1

		sup=c/T
		# print(itemset,sup)
		if(sup>=minSupport):
			frequentItemSets.append(itemset)
			supDict[tuple(itemset)]=c;

	if(len(frequentItemSets)!=0):
		masterFrequentItemSets.append(frequentItemSets)
		generateCandiateItemSets(frequentItemSets,dataset,minSupport,T)

		


def generateCandiateItemSets(frequentItemSets,dataset,minSupport,T):

	frequentItemSets=sorted(frequentItemSets,key=lambda x:x)

	temp=[]
	temp2=[]
	if(len(frequentItemSets)==0):
		print("NO association Rules Possible")
		return;

	l=len(frequentItemSets[0])
	candidateFrequentItemSets=[]
	for a in frequentItemSets:
		for b in frequentItemSets:
			if( a is not b):
				ta=a[:l-1]
				tb=b[:l-1]

				if(ta ==  tb):
					temp=[i for i in a]
					temp.append(b[l-1])
					temp=sorted(temp)
					if(temp not in candidateFrequentItemSets):
						candidateFrequentItemSets.append(sorted(temp))
					temp=[]
					temp2=[]

	candidateFrequentArray=[]

	for itemset in candidateFrequentItemSets:
		combinations=set(itertools.combinations(itemset,l))
		# print(itemset," Combination ",combinations)
		if(combinations.issubset(set(tuple(row) for row in frequentItemSets))):
			candidateFrequentArray.append(itemset)
	
	generateFrequentItemSets(candidateFrequentArray,dataset,minSupport,T)	

def apioriGen(itemset):
	itemset=sorted(itemset,key=lambda x:x)
	# print(itemset)
	#we get [[],[],[]]
	H=[]

	s=set()
	for i in itemset:
		for j in i:
			s.add(j)
	# print(s)

	for a in itemset:
		l=len(a)
		for b in s:
			temp=set()
			for c in a:
				temp.add(c)
			temp.add(b)
			if(len(temp)==l+1):
				t=list(temp)
				if(temp not in H):
					H.append(sorted(temp))



	return H


def generateAssociationRules(itemset,H,minConfidence):
	k=len(itemset)

	m=len(H[0])

	if k>m:

		Hm=list(H)
		Hf=list(Hm)
		# print(type(Hf))
		for h in Hf:  
			# print("Hello",len(h))
			hm=set(tuple(h))

			
			conf=supDict[tuple(itemset)]/supDict[tuple(sorted(tuple((set(tuple(itemset))-hm))))] #Calculating Confidence 
			
			if(conf >= minConfidence):
				rules=[]
				rules.append(list((set(tuple(itemset)))-hm))
				rules.append(list(hm))
				finalRule.append(rules)
				#print(((set(tuple(itemset)))-hm),"----->",hm)

				
			else:
				Hm.remove(h)
		if len(apioriGen(Hm))!=0:
			generateAssociationRules(itemset,apioriGen(Hm),minConfidence)



def callAssociationRules(minConfidence):

	# print("CallAssociationsRules")
	# print((masterFrequentItemSets))
	for cardinals in masterFrequentItemSets:
		# print("Cardinals",cardinals)
		for itemset in cardinals:
			# print("Itemset",itemset)
			H=list(itertools.combinations(itemset,1))
			# print((H))
			Hpass=[]
			# print(type(H))
			for i in H:
				# t=[]
				Hpass.append(list(i))
				# print(t)
				# Hpass.append(t)
			# print(Hpass)
			# print()
			generateAssociationRules(itemset,Hpass,minConfidence)


def generateF1(dataset,minSupport,T):

	prodDict={}
	returnSet=[]
	
	for data in dataset:
		for prod in data:
			if prod not in prodDict:
				prodDict[prod]=1 
			else:
				prodDict[prod]+=1


	for key in prodDict:
		temp=[]
		sup=prodDict[key]/T
		if sup>=minSupport:
			temp.append(key)
			returnSet.append(temp)
			supDict[tuple(temp)]=prodDict[key]
	
	return (returnSet)



def main():
	path="groceries.csv"
	transactions=load_data(path)

	noOfTransactions=(len(transactions)) #Necessary to calculate support
	
	minSupport=eval(input("Enter Minimum Support: "))
	minConfidence=eval(input("Enter Minimum Confidence: "))

	F1=generateF1(transactions,minSupport,noOfTransactions)

	generateCandiateItemSets(F1,transactions,minSupport,noOfTransactions)

	masterFrequentItemSets.sort(key=lambda x:x[0])

	callAssociationRules(minConfidence)
	count=0
	for i in masterFrequentItemSets:
		for a in i:
			count+=len(a)

	print("Final Frequent ItemSets Count: ",count)
	print(masterFrequentItemSets,end='\n\n)
	print("Final Rule count: ",len(finalRule))
	
	for i in finalRule:
		print(i)






if __name__ == '__main__':
	main()
