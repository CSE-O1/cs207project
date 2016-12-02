#!/bin/bash
echo "Python starting"

file="./VPDict.pickle"

if [ -f "$file" ]
then
# delete the existing VPDB
#	rm ./VPDB*.dbdb	
python - << EOF
import generateAndStoreTS, TimeSeriesDistance, buildVPDBforest, mostSimilarTS, pickle
with open('VPDict.pickle', 'rb') as handle:
  	VPDict = pickle.load(handle)
mostSimilarTS.mostSimilarTS('$1', VPDict, $2)
EOF
else

python - << EOF
import generateAndStoreTS, TimeSeriesDistance, buildVPDBforest, mostSimilarTS, pickle
generateAndStoreTS.generateAndStoreTimeSeries()
VPDBList = buildVPDBforest.createVPForest()
with open('VPDict.pickle', 'wb') as handle:
  	pickle.dump(VPDBList[0].VPDict, handle)
mostSimilarTS.mostSimilarTS('$1', VPDBList[0].VPDict, $2)
EOF
fi


#EOF

echo "Done"
