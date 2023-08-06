class DataLoader(object):
    def __init__(self, localTrains=None, localVals=None, localTests=None, globalTrain=None, globalVal=None,
                 globalTest=None):
        self._localTrains = localTrains
        self._localVals = localVals
        self._localTests = localTests
        self._globalTrain = globalTrain
        self._globalVal = globalVal
        self._globalTest = globalTest

    @property
    def localTrains(self):
        return self._localTrains

    @property
    def localVals(self):
        return self._localVals

    @property
    def localTests(self):
        return self._localTests

    @property
    def globalTrain(self):
        return self._globalTrain

    @property
    def globalVal(self):
        return self._globalVal

    @property
    def globalTest(self):
        return self._globalTest
