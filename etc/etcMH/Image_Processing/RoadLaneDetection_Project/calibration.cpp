#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

void MyCalibration()
{
    Mat images;
    const char* path = "./camera_cal/calibration*.jpg";
    vector<String> filename;

    glob(path, filename, false);
}


int main()
{
    
}
