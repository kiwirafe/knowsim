import os
import re
import math
import sys
import logging
import jieba
import random
import hashlib
import binascii
import time

OutsideLogger = logging.getLogger('KnowSim')
OutsideLogger.setLevel(logging.DEBUG)
# Create file handler that logs debug and higher level messages
fh = logging.FileHandler('knowsim.log')
fh.setLevel(logging.DEBUG)
# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# Create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(name)s Log: %(asctime)s - %(levelname)s: %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
OutsideLogger.addHandler(ch)
OutsideLogger.addHandler(fh)


class calculator(object):
    def __init__(self):
        self.logger = OutsideLogger
        self.logger.info("Starting up KnowSim")
        self.SysPath = os.path.dirname(os.path.abspath(__file__))
        self.weight = None
        self.UseLog = True
        self.FileDir = ""
        self.InputTarget = 0
        self.feature = 64
        self.HashNums = 16
        self.prime = 4294967311

    #中文分词
    def SegDepart(self, sentence):
        StopWords = [line.strip() for line in open(self.SysPath + \
            "/stoptext.txt", encoding='utf-8').readlines()]
        SentenceDepart = jieba.cut(sentence.strip())

        output = []
        for word in SentenceDepart:
            if word not in StopWords:
                if word != '\n':
                    output.append(word)
        return output

    def dict2file(self, result, name="result.txt"):
        open(name, "w").close()
        f = open(name, "a")
        
        for key, value in result.items():
            f.write(str(key) + ": " + str(value) + "\n")
        f.close()
        self.logger.info("Result saved in" + name)

    def input2list(self, input):
        result = []
        try:
            with open(input, encoding='utf-8') as f:
                corpus = f.read()
        except:
            with open(input, encoding='gbk') as f:
                corpus = f.read()

        LineSplit = re.split(r'[。！；？，]', corpus.strip()) #按符号分句

        for line in LineSplit:
            temp = self.SegDepart(line)
            result.extend(temp)
        return result

    def dir2list(self, input):
        files = {}
        if self.FileDir == "":
            TempDir = input.rsplit('/', 1)[0] + "/"
        else:
            TempDir = self.FileDir
        for inputname in os.listdir(TempDir):
            files[TempDir + inputname] = self.input2list(TempDir + inputname)

        return files

    def SortDict(self, input):
        return dict(sorted(input.items(), \
            key=lambda kv: kv[1], reverse=True))

    def HashString(self, s):
        h = hashlib.sha256(s.encode('utf-8'))
        return bin(int(h.hexdigest(), 16))[-self.feature:]

    #公式 h(x) = (a*x + b) % c
    def HashAlg(self, k):
        MaxHash = 2**32 - 1
        # Create a list of 'k' random values.
        RandomList = []
        
        while k > 0:
            # Get a random shingle ID.
            random.seed(k)
            RandIndex = random.randint(0, MaxHash) 
        
            #确保数字唯一
            while RandIndex in RandomList:
                RandIndex = random.randint(0, MaxHash) 
            
            #Append值
            RandomList.append(RandIndex)
            k = k - 1
            
        return RandomList

    #计算TF值 
    def GetTF(self, corpus):
        tf = {}
        for x in corpus:
            tf[x] = corpus.count(x)
        
        wordsSum = sum(tf.values())
        for key, value in tf.items(): 
            tf[key] = value / wordsSum
        return tf

    def Get1(self, corpus):
        tf = {}
        for x in corpus:
            tf[x] = 1
        return tf

    def GetTFIDF(self, input):
        if isinstance(input, list) == True:
            tf = self.GetTF(input[self.InputTarget])
            one = self.Get1(input[self.InputTarget])
        elif isinstance(input, str) == True:
            files = self.dir2list(input)
            tf = self.GetTF(files[input])
            one = self.Get1(files[input])
        
        if self.weight == "TF":
            return tf
        elif self.weight == None:
            return one
        else:
            raise Exception("self.weight can onle be set as \"TF\" or None")
        

    def cossim(self, input1, input2):
        #取TFIDF值
        result = self.GetTFIDF(input1)
        result2 = self.GetTFIDF(input2)

        merge = result.copy()
        merge.update(result2)
        WordSet = list(dict.fromkeys(merge.keys()))
        WordDict = {}

        for i, x in enumerate(WordSet):
            WordDict[x] = i

        Result1Cut = [0] * len(WordDict)
        Result2Cut = [0] * len(WordDict)

        for word in result.keys():
            Result1Cut[WordDict[word]] = result[word]

        for word in result2.keys():
            Result2Cut[WordDict[word]] = result2[word]

        TopSum = 0
        sq1 = 0
        sq2 = 0
        for i in range(len(result)):
            TopSum += Result1Cut[i] * Result2Cut[i]
            sq1 += pow(Result1Cut[i], 2)
            sq2 += pow(Result2Cut[i], 2)

        FinalResult = round(TopSum / (math.sqrt(sq1) * math.sqrt(sq2)), 4)
        return FinalResult
    
    def ngram(self, input1, input2, num=2):
        result = [] 
        for i in range(len(input1) - num + 1):
            result.append(input1[i:i + num]) 

        result2 = [] 
        for i in range(len(input2) - num + 1):
            result2.append(input2[i:i + num]) 

        cnt = 0 
        for i in result:
            for j in result2:
                if i == j:
                    cnt += 1

        return (cnt / len(result) + cnt / len(result2)) / 2

    def simhash(self, input1, input2):
        TFIDFResult = self.GetTFIDF(input1)
        TFIDFResult2 = self.GetTFIDF(input2)

        FirstResults = {}
        FirstResults2 = {}

        #取前feature个词
        i = 0
        for key, value in TFIDFResult.items():
            FirstResults[key] = value
            i += 1
            if i >= self.feature:
                break

        i = 0
        for key, value in TFIDFResult2.items():
            FirstResults2[key] = value
            i += 1
            if i >= self.feature:
                break

        result = FirstResults
        result2 = FirstResults2

        HashResults = {}
        HashResults2 = {}
        
        for key, value in result.items():
            HashResults[self.HashString(key)] = value
        for key, value in result2.items():
            HashResults2[self.HashString(key)] = value

        result = []
        result2 = []

        i = 0
        for key, value in HashResults.items():
            result.append([])
            for x in key:
                if int(x) == 0:
                    result[i].append(value * -1)
                else:
                    result[i].append(value)
            i += 1

        i = 0
        for key, value in HashResults2.items():
            result2.append([])
            for x in key:
                if int(x) == 0:
                    result2[i].append(value * -1)
                else:
                    result2[i].append(value)
            i += 1

        FinalResult = []
        FinalResult2 = []
        
        for i in range(self.feature):
            FinalResult.append(0)
            for x in result:
                FinalResult[i] += x[i]

            FinalResult2.append(0)
            for x in result2:
                FinalResult2[i] += x[i]

        FinalString = ""
        for x in FinalResult:
            if x > 0:
                FinalString += "1"
            else:
                FinalString += "0"

        FinalString2 = ""
        for x in FinalResult2:
            if x > 0:
                FinalString2 += "1"
            else:
                FinalString2 += "0"

        hamming = 0
        for i, x in enumerate(FinalString):
            if x != FinalString2[i]:
                hamming += 1

        return 1 - hamming / self.feature

    def minhash(self, input1, input2):
        result = self.GetTFIDF(input1)
        result2 = self.GetTFIDF(input2)

        coeff1 = self.HashAlg(self.HashNums)
        coeff2 = self.HashAlg(self.HashNums)

        signature = set()
        signature2 = set()

        MinhashNum = self.prime
        MinhashNum2 = self.prime
        for i in range(0, self.HashNums):
            for x in result.keys():
                crc = binascii.crc32(x.encode('utf-8')) & 0xffffffff
                #Generating Hash
                HashCode = (coeff1[i] * crc + coeff2[i]) % self.prime
                # Track the lowest hash code seen.
                if HashCode < MinhashNum:
                    MinhashNum = HashCode

                signature.add(MinhashNum)

            for y in result2.keys():
                crc = binascii.crc32(y.encode('utf-8')) & 0xffffffff
                HashCode2 = (coeff1[i] * crc + coeff2[i]) % self.prime
                if HashCode2 < MinhashNum2:
                    MinhashNum2 = HashCode2

                signature2.add(MinhashNum2)

        intersect = 0
        total = 0
        for x in signature:
            if x in signature2:
                intersect += 1
            total += 1

        return intersect / total