#pragma once
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

void load_cascade(CascadeClassifier& cascade, string fname)
{
	String path = "C:/opencv/sources/data/haarcascades/";
	String full_name = path + fname;

	CV_Assert(cascade.load(full_name));

}
Mat preprocessing(Mat image)
{
	Mat gray;
	cvtColor(image, gray, COLOR_BGR2GRAY);  // 명암도 영상 변환
	equalizeHist(gray, gray); // 히스토그램 평활화 (영상 화질 개선)

	return gray;
}
