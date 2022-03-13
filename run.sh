#!/bin/bash
docker build . -t safou/audiveris
docker run --rm -v $(pwd)/output:/output -v $(pwd)/input:/input -u $(id -u ${USER}):$(id -g ${USER}) safou/audiveris

OUTPUT_PATH="$(pwd)/output/*"
for f in $OUTPUT_PATH
do
    cd $f
    PROJECT_PATH="$f/*.mxl"
    for project in $PROJECT_PATH
    do
        unzip $project
        
        fullfilename=$(basename -- "$project")
        extension="${fullfilename##*.}"
        filename="${fullfilename%.*}"
        xmlfilename="$filename.xml"
        
        rm -r META-INF
        rm *.log *.mxl *.omr
        
        python3 ../../main.py $xmlfilename

        rm $xmlfilename
    done
    
done
