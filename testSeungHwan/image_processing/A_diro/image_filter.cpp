#include <opencv2/opencv.hpp>
#include "image_filter.h"

cv::Mat color_filter(cv::Mat inputimage, int is_show) {
	cv::Mat img_filter;
	cv::UMat image_hsv, white_filter, yellow_filter, white_image, yellow_image;
	inputimage.copyTo(img_filter);

	cv::cvtColor(img_filter, image_hsv, cv::COLOR_BGR2HSV);
	// 흰색 차선 색 범위(RGB)
	cv::Scalar low_white = cv::Scalar(150, 150, 150);
	cv::Scalar high_white = cv::Scalar(255, 255, 255);
	// 노란 차선 색 범위(HSV)
	cv::Scalar low_yellow = cv::Scalar(10, 100, 100);
	cv::Scalar high_yellow = cv::Scalar(40, 255, 255);
	
	cv::inRange(img_filter, low_white, high_white, white_filter);
	cv::bitwise_and(img_filter, img_filter, white_image, white_filter);

	cv::inRange(image_hsv, low_yellow, high_yellow, yellow_filter);
	cv::bitwise_and(img_filter, img_filter, yellow_image, yellow_filter);
	
	cv::addWeighted(white_image, 1.0, yellow_image, 1.0, 0.0, img_filter);

	if (is_show) {
		imshow("white", white_image);
		imshow("yellow", yellow_image);
		imshow("filtering image", img_filter);
	}

	return img_filter;
}