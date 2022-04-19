#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int main() {
	Mat image = imread("./road1.jpg", 1);
	imshow("¿øº»", image);

	Mat img_filter;
	cvtColor(image, img_filter, COLOR_BGR2GRAY);
	imshow("grayscale", img_filter);

	Mat img_edges;
	Canny(img_filter, img_edges, 50, 150);
	imshow("Canny", img_edges);
	
	vector<Vec4i> lines;
	HoughLinesP(img_edges, lines, 1, CV_PI / 180, 50, 50, 5);

	Mat img_hough;
	image.copyTo(img_hough);
	for (size_t i = 0; i < lines.size(); i++) {
		Vec4i I = lines[i];
		line(img_hough, Point(I[0], I[1]), Point(I[2], I[3]), Scalar(0, 0, 255), 2, 8);
	}
	imshow("hough", img_hough);
	

	waitKey(0);
	return 0;
}