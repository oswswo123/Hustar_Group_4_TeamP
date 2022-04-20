#pragma once
#include <opencv2/opencv.hpp>

cv::Mat color_filter(cv::Mat inputimage, int is_show);
std::vector<cv::Point> regression_and_detection_points(cv::Mat inputimage, std::vector<cv::Vec4i> inputlines);
cv::Mat setting_roi(cv::Mat inputimage);
std::vector<cv::Vec4i> hough_transform(cv::Mat inputimage, int point_threshold, int length_threshold, int distance_threshold, bool is_show);
