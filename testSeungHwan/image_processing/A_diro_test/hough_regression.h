#pragma once
#include <opencv2/opencv.hpp>

std::vector<cv::Point> regression_and_detection_points(cv::Mat inputimage, std::vector<cv::Vec4i> inputlines);
