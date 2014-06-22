#!/bin/bash


for file in `find ./templates -name '*.ui'` ; do 
    py_file=`echo $file | sed 's/\.ui/.py/' ` 
    pyuic4 $file -o $py_file  
done


for file in `find ./ -name '*.qrc'` ; do 
    py_file=`echo $file | sed 's/\.qrc/_rc.py/' ` 
    pyrcc4 $file -o $py_file
done 
pylupdate4 -noobsolete -verbose domotica_client.pro
lrelease-qt4 -verbose domotica_client.pro
