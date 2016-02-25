#!/bin/bash

# Amir Yazdanbakhsh
# Feb. 18, 2016

. ../include/bash_color.h
. ../include/gpgpu_sim.mk



#%%%%%%%%%%%%%%%%%%%%%%% Configs %%%%%%%%%%%%%%%%%%%%%%%
APP_NAME=newton-raph
APP_BIN=${APP_NAME}.out

MICROARCH=GTX480 # GPU Configuration
SIM_TYPE=baseline
GPGPUSIM_CONFIG_DIR=${MICROARCH,,} # GPGPUSIM configuration directory
EXTENSION=${GPGPUSIM_CONFIG_DIR}
LOG_DIR=${SIM_TYPE}
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


Usage()
{
	echo -e "${Red}./run-baseline.sh${White}"
	exit 1
}


echo -e "${Blue}(1) Create the log directory.${White}"	
if [ ! -d log ]; then
	mkdir log
fi
if [ ! -d log/${LOG_DIR} ]; then
	mkdir log/${LOG_DIR}
fi
if [ ! -d log/${LOG_DIR}/${EXTENSION} ]; then
	mkdir log/${LOG_DIR}/${EXTENSION}
fi

echo -e "${Blue}(2) Create the simulation directory.${White}"
if [ ! -d gpgpusim-runs ]; then
	mkdir gpgpusim-runs
fi
if [ ! -d gpgpusim-runs/${LOG_DIR} ]; then
	mkdir gpgpusim-runs/${LOG_DIR}
fi
if [ ! -d gpgpusim-runs/${LOG_DIR}/${EXTENSION} ]; then
	mkdir gpgpusim-runs/${LOG_DIR}/${EXTENSION} 
fi

# copy config files
echo -e "${Blue}(3) Copying the ${MICROARCH} config files.${White}"
cp ${SIM_DIR}/configs/${MICROARCH}/* ./gpgpusim-runs/${LOG_DIR}/${EXTENSION}


echo -e "${Blue}(4) Make the source file.${White}"
make clean > /dev/null
make > make_log 2>&1
if [ "$?" -ne 0 ]; then
	echo -e "${Red}We have a bad news :( We could not build your application. For more information, please check the make_log file${White}"
	exit
fi

echo -e "${Blue}(5) Copying the binary into the execution folder.${White}"
cp ./bin/${APP_BIN} ./gpgpusim-runs/${LOG_DIR}/${EXTENSION}

echo -e "${Blue}(6) Enjoy your coffee! We are working hard to simulate your benchmark.${White}"
cd ./gpgpusim-runs/${LOG_DIR}/${EXTENSION}

for f in ../../../test-data/input/*.txt
do
	echo -e "${Blue}\t(1) Running the simulation for ${f}.${White}"
	filename=$(basename "$f")
	extension="${filename##*.}"
	filename="${filename%.*}"
			
	rm -rf gpgpusim_power_report__*.log

	./${APP_BIN} $f ../../../test-data/output/${filename}_${EXTENSION}.txt 0.1 > ../../../log/${LOG_DIR}/${EXTENSION}/${filename}_${EXTENSION}.log

	echo -e "${Blue}\t(2) Processing the power file.${White}"
	cp gpgpusim_power_report__*.log ../../../log/${LOG_DIR}/${EXTENSION}/${filename}_${EXTENSION}.pwr
	echo -e "\t-----------------------------------------------"
done


