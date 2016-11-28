Author: Chin Hui Chew (Team 4)

Run the following on terminal window/command line window in the same directory where ArrayTimeSeries is stored

1) Run 'Python generateAndStoreTS.py' to generate 1000 TS
2) Run 'buildVPDBforest.py' to create 20 database indexes
3) Run 'Python' in command line
4) Run 'import mostSimilarTS'
5) Search for the most similar TS by the following command:

	'mostSimilarTS.mostSimilarTS('./ts_100.npy', 10)'
	
	Output: 
	Nodes in search region =  1472
	['./ts_100.npy', './ts_586.npy', './ts_813.npy', './ts_106.npy', './ts_283.npy', './ts_283.npy', './ts_478.npy', './ts_478.npy', './ts_665.npy', './ts_248.npy']
