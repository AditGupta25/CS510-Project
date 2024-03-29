import math, os, pickle, re, numpy as np, sys

class Bayes_Classifier:

	def __init__(self):
		'''This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
		cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
		the system will proceed through training.  After running this method, the classifier 
		is ready to classify input text.'''
		self.dPositive = dict()
		self.dNegative = dict()
		self.sTrainingDirectory = "tweets/"
		self.dSetData = dict()
		try:
			self.dPositive = self.load("picklePositiveDictionary")
			self.dNegative = self.load("pickleNegativeDictionary")
			self.dSetData = self.load("pickleSetData")
		except:
			self.dSetData = {
				"total" : float(0),
				"positive" : float(0),
				"negative" : float(0)
			}
			self.train()
			
	def train(self):   
		'''Trains the Naive Bayes Sentiment Classifier.'''
		lFileList=[]
		for fFileObj in os.walk(self.sTrainingDirectory):
			lFileList = fFileObj[2]
		self.dSetData["total"] = len(lFileList)
		for file in lFileList:
			#parse file name and determine if positive or negative review
			#update frequency for that word in the appropriate dictionary
			path = self.sTrainingDirectory + file
			iFileClass = self.parseFilename(file)
			#classify positive and negative documents, ignore neutral documents
			if (iFileClass == 0):
				self.updateDictionary(self.dNegative, path)
				self.dSetData["negative"] += 1
			elif (iFileClass == 1): 
				self.updateDictionary(self.dPositive, path)
				self.dSetData["positive"] += 1
		self.save(self.dPositive, "picklePositiveDictionary")
		self.save(self.dNegative, "pickleNegativeDictionary")
		self.save(self.dSetData, "pickleSetData")
	
	def parseFilename(self, sFilename):
		''' parses a file name for review and returns True if 5 star, and False if 
		1 star'''
		#print(sFilename)
		iStars = int(sFilename[sFilename.find("-")+1:sFilename.find(".")])
		#print(iStars)
		return iStars
	
	def updateDictionary(self, dDic, sFName):
		lWordList = self.tokenize(self.loadFile(sFName))
		npWordList = np.array(lWordList)
		npUniqueWordList = np.unique(npWordList, return_counts=True)
		for i in range(len(npUniqueWordList[0])):
			if npUniqueWordList[0][i] in dDic:
				dDic[npUniqueWordList[0][i]][0] += npUniqueWordList[1][i] # frequency
				dDic[npUniqueWordList[0][i]][1] += 1 # presence
			else:
				dDic[npUniqueWordList[0][i]] = [0,0] # add word to dictionary if it does not already exist
				dDic[npUniqueWordList[0][i]][0] += npUniqueWordList[1][i] # frequency
				dDic[npUniqueWordList[0][i]][1] += 1 # presence
		
	def classify(self, sText):
		'''Given a target string sText, this function returns the most likely document
		class to which the target string belongs. This function should return one of three
		strings: "positive", "negative" or "neutral".
		'''
		fMargin = 1.005
		fPriorPositive = math.log10(self.dSetData["positive"]/self.dSetData["total"])
		fPriorNegative = math.log10(self.dSetData["negative"]/self.dSetData["total"])
		fPPositive = fPriorPositive + self.conditionalProbability(sText, self.dPositive)
		fPNegative = fPriorNegative + self.conditionalProbability(sText, self.dNegative)
		#print("P_Positive= " + str(fPPositive))
		#print("P_Negative= " + str(fPNegative))
		if (fPNegative/fPPositive) > fMargin:
			return "positive"
		elif (fPPositive/fPNegative) > fMargin:
			return "negative"
		else:
			return "neutral"
		'''if fPPositive > fPNegative:
			return "positive"
		else: 
			return "negative"'''
	
	def testClassifier(self):
		fPrecision = 0.0
		fRecall = 0.0
		fFMeasure = 0.0
		iTruePositives = 0
		iFalsePositives = 0
		iFalseNegatives = 0
		sFilepath = sys.argv[1] #test file path must be given when program is run
		
		lFileList=[]
		for fFileObj in os.walk(sFilepath):
			lFileList = fFileObj[2]
		for file in lFileList:
			#get truth data
			iTruthData = self.parseFilename(file)
			#classify
			sClassResult = self.classify(self.loadFile(sFilepath + file))
			#print(str(iTruthData) + "- " + sClassResult)
			#compare and update performance measures
			if (sClassResult == "positive") & ((iTruthData == 1)):
				#print("True positive")
				iTruePositives += 1
			elif (sClassResult == "positive") & ((iTruthData == 0)):
				#print("False Positive")
				iFalsePositives += 1
			elif (sClassResult == "negative") & ((iTruthData == 1 )):
				#print("False Negative")
				iFalseNegatives += 1
		fPrecision = float(iTruePositives)/float(iTruePositives + iFalsePositives)
		fRecall = float(iTruePositives)/float(iTruePositives + iFalseNegatives)
		fFMeasure = (2*fPrecision*fRecall)/(fPrecision+fRecall)
		print("Precision: " + str(fPrecision))
		print("Recall: " + str(fRecall))
		print("F-Measure: " + str(fFMeasure))
			
		
	def conditionalProbability(self, sText, dClassDictionary):
		'''calculates conditional probability that a string of text occurs in a document class
		returns log10 of probability'''
		fTotalConditionalProbability = 1.0
		fSumAllFrequencies = float(0)
		fTrainingFrequency = 0
		fIndConditionalProbability = float(0)
		for key in dClassDictionary:
			fSumAllFrequencies += float(dClassDictionary[key][0])
		lTokens = self.tokenize(sText)
		for token in lTokens:
			#if it exists, otherwise 1
			if token in dClassDictionary:
				fTotalConditionalProbability += math.log10(float(dClassDictionary[token][0]/fSumAllFrequencies))
			else:
				'''use add-1 smoothing. Based on the equation p(w) = (C(w)+1)/(N+V)
				C(w) is the count of the unseen word (ie 0)
				V is the total number of unique words
				N is the total number of words (i.e. sum of all frequencies)
				Explanation for add-1 smoothing found here:
				https://www.quora.com/Could-someone-explain-Laplacian-smoothing-or-1-up-smoothing'''
				fTotalConditionalProbability += math.log10(1/float(len(dClassDictionary) + fSumAllFrequencies))
		return fTotalConditionalProbability
		
	def loadFile(self, sFilename):
		'''Given a file name, return the contents of the file as a string.'''
		f = open(sFilename, "r")
		sTxt = f.read()
		f.close()
		return sTxt

	def save(self, dObj, sFilename):
		'''Given an object and a file name, write the object to the file using pickle.'''
		f = open(sFilename, "wb")
		p = pickle.Pickler(f)
		p.dump(dObj)
		f.close()

	def load(self, sFilename):
		'''Given a file name, load and return the object stored in the file.''' 
		f = open(sFilename, "rb")
		u = pickle.Unpickler(f)
		dObj = u.load()
		f.close()
		return dObj

	def tokenize(self, sText): 
		'''Given a string of text sText, returns a list of the individual tokens that 
		occur in that string (in order).'''

		lTokens = []
		sToken = ""
		for c in sText:
			if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\'" or c == "_" or c == '-':
				sToken += c
			else:
				if sToken != "":
					lTokens.append(sToken)
					sToken = ""
				if c.strip() != "":
					lTokens.append(str(c.strip()))

		if sToken != "":
			lTokens.append(sToken)

		return lTokens

	
def main():
	bayes = Bayes_Classifier()
	#print(bayes.dSetData)
	lStrings = ["Go birds!", "The eagles cant even beat the cowboys", "Wow, what a beautiful eagle flying above the mountain"]
	for string in lStrings:
		print("string: \"" + string + "\"")
		print("result: " + bayes.classify(string))
		print
	bayes.testClassifier()
	

	
main()
