Author: Chin Hui Chew (Team 4)
Documentation by unbalanced binary tree by Nripsuta Saxena (Team 4)

Instructions on Running from Command Line to Find the Most Similar TS of a Target TS
------------------------------------------------------------------------------------
- Make the runVPDB.sh file executable by this line: 
	$ chmod +x runVPDB.sh
- Run in command line with this line:
	$ ./runVPDB.sh './newTSfilename.npy' 10

Note the target TS file should be in the format above and the second argument which represents the number of nearest neighbors is optional and defaults to one

Example input and output in terminal:

(py35) Chins-MacBook-Air-3:timeseries chinhuichew$ ./runVPDB.sh './testTS1201.npy' 10
Python starting
['./ts_272.npy', './ts_589.npy', './ts_630.npy', './ts_155.npy', './ts_25.npy', './ts_674.npy', './ts_760.npy', './ts_395.npy', './ts_232.npy', './ts_88.npy']
Done


Remarks on runVPDB.sh
---------------------
The command line program requires two input parameter, the target TS file which should be in the format './xx.npy' and the number of nearest neighbors required (optional with default of 1)

The first run of this command line program creates the timeseries, select the Vantage Points and constructs the Vantage Point Database, then run the function to find out the most similar TS. As such, the run will take longer than subsequent runs. In subsequent runs, the other steps will be skipped and it will only retrieve the most similar TS based on the existing database.