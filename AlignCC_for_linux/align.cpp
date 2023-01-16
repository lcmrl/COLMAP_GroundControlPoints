// gcc align.cpp -o align -I/usr/local/include/CCCoreLib -lCCCoreLib -lstdc++
// gcc align.cpp -o align -static -I/usr/local/include/CCCoreLib -lCCCoreLib -lstdc++ -lm
// export LD_LIBRARY_PATH=/usr/local/lib/ && ./align colmap.txt gt.txt

#define CC_CORE_LIB_USES_FLOAT

#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <iomanip>
#include <algorithm>
#include <RegistrationTools.h>

typedef struct data_line {
	uint id;
	double xyz[3];
} data_line;

using namespace CCCoreLib;
using ScaledTransformation = PointProjectionTools::Transformation;

bool sort_by_id(data_line i, data_line j) {
	return i.id < j.id;
}

std::vector<data_line> read_file(char *in_file_name) {
	std::ifstream in_file(in_file_name);
	std::string str; 
	std::vector<data_line> out_data; 

	while (std::getline(in_file, str)) {
		data_line c_line;
		std::stringstream ss(str);
		 ss >> c_line.id;
		 ss.get();
		 ss >> c_line.xyz[0];
		 ss.get();
		 ss >> c_line.xyz[1];
		 ss.get();
		 ss >> c_line.xyz[2]; 
//		 std::cout << std::setprecision(13) << c_line.id << " " << c_line.xyz[0] << " " << c_line.xyz[1] << " " << c_line.xyz[2] << std::endl;
		 out_data.push_back(c_line);
	}
	return out_data;
}

int main(int argc, char **argv){

	std::vector<data_line> lvec = read_file(argv[1]);
	std::vector<data_line> rvec = read_file(argv[2]);

	std::sort(lvec.begin(),lvec.end(),sort_by_id);
	std::sort(rvec.begin(),rvec.end(),sort_by_id);

	PointCloud lCloud, rCloud;
	ScaledTransformation trans;

	if (lvec.size()!=rvec.size()) {
		std::cout << "Different number of points!" << std::endl;
		exit(EXIT_FAILURE);
	}

	lCloud.reserve(lvec.size());
	rCloud.reserve(rvec.size());

	for (std::vector<data_line>::iterator it = lvec.begin(); it != lvec.end(); ++it) {
		CCVector3 xyz(it->xyz[0],it->xyz[1],it->xyz[2]);
		lCloud.addPoint(xyz);
	}

	for (std::vector<data_line>::iterator it = rvec.begin(); it != rvec.end(); ++it) {
		CCVector3 xyz(it->xyz[0],it->xyz[1],it->xyz[2]);
		rCloud.addPoint(xyz);
	}

	HornRegistrationTools::FindAbsoluteOrientation(&lCloud, &rCloud, trans);
	double rms = HornRegistrationTools::ComputeRMS(&lCloud, &rCloud, trans);

	std::cout << std::setprecision(6) << "Alignment RMS: " << rms << std::endl;
	std::cout << std::setprecision(6) << "Scale: " << trans.s << std::endl;
	std::cout << "Transformation matrix:" << std::endl;
	std::cout << std::setprecision(6) << trans.s*trans.R.getValue(0,0) << " " << trans.s*trans.R.getValue(0,1) << " " << trans.s*trans.R.getValue(0,2) << " " << trans.T[0] << std::endl;
	std::cout << std::setprecision(6) << trans.s*trans.R.getValue(1,0) << " " << trans.s*trans.R.getValue(1,1) << " " << trans.s*trans.R.getValue(1,2) << " " << trans.T[1] << std::endl;
	std::cout << std::setprecision(6) << trans.s*trans.R.getValue(2,0) << " " << trans.s*trans.R.getValue(2,1) << " " << trans.s*trans.R.getValue(2,2) << " " << trans.T[2] << std::endl;
	std::cout << "0 0 0 1" << std::endl;
}
