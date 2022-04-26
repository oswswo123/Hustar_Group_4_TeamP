#include <opencv2/opencv.hpp>
#include "hough_cal.h"

std::vector<cv::Vec4i> hough_transform(cv::Mat inputimage, int point_threshold, int length_threshold, int distance_threshold, bool is_show) {
	std::vector<cv::Vec4i> lines;
	cv::HoughLinesP(inputimage, lines, 1, CV_PI / 180, point_threshold, length_threshold, distance_threshold);
	
	// 영상 출력 부분
	if (is_show) {
		cv::Mat img_hough;
		inputimage.copyTo(img_hough);
		for (size_t i = 0; i < lines.size(); i++) {
			cv::Vec4i I = lines[i];
			cv::line(img_hough, cv::Point(I[0], I[1]), cv::Point(I[2], I[3]), cv::Scalar(0, 0, 255), 2, 8);
		}
		cv::imshow("hough", img_hough);
	}

	return lines;
}