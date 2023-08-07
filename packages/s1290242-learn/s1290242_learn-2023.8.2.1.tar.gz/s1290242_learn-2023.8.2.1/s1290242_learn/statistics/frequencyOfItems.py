from PAMI.frequentPattern.basic import FPGrowth as alg

class frequencyOfItems:
    def __init__(self, inputFile, minSup, sep):
        self.inputFile = inputFile
        self.minSup = minSup
        self.sep = sep

    def getFrequency(self):
        obj = alg.FPGrowth(self.inputFile, self.minSup, self.sep)
        obj.startMine()
        obj.save('frequentPatterns.txt')
        frequency_dict = {}
        with open('frequentPatterns.txt') as f:
          text = f.read()
         
        return text
         

if __name__ == "__main__":
    inputFile = 'PM24HeavyPollutionRecordingSensors.csv'
    minSup = 10
    sep = '\t'

    itemsFrequency = frequencyOfItems(inputFile, minSup, sep)
    itemsFreqDictionary = itemsFrequency.getFrequency()

    print(itemsFreqDictionary)
