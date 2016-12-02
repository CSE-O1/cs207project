import generateAndStoreTS, TimeSeriesDistance, buildVPDBforest, mostSimilarTS, pickle
import unittest

generateAndStoreTS.generateAndStoreTimeSeries()

VPDBList = buildVPDBforest.createVPForest()


class MyTest(unittest.TestCase):
    # all of them have test_xxx so that unittest main can run it
    
    def mostSimilarTS(self, inputFileName, VPDict, howmany = 1):
        self.assertEqual(mostSimilarTS.mostSimilarTS('./ts_1.npy', VPDBList[0].VPDict, 1), ['./ts_1.npy'])
    

if __name__ == '__main__':
    unittest.main()