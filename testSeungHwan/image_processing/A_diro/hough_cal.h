#pragma once
#include <opencv2/opencv.hpp>

std::vector<cv::Vec4i> hough_transform(cv::Mat inputimage, int point_threshold, int length_threshold, int distance_threshold, bool is_show);