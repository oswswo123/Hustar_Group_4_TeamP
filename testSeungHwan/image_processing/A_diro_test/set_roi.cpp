#include <opencv2/opencv.hpp>
#include "set_roi.h""

cv::Mat setting_roi(cv::Mat inputimage) {
	cv::Mat img_roi;

	int width = inputimage.cols;
	int height = inputimage.rows;
	cv::Mat roi_filter = cv::Mat::zeros(height, width, CV_8UC1);

	cv::Point left_points[4]{
		cv::Point((width * 0.05), height - height * 0.05),
		cv::Point((width * 0.4), height - height * 0.4),
		cv::Point(width * 0.5, height - height * 0.4),
		cv::Point(width * 0.4, height - height * 0.05)
	};
	cv::Point right_points[4]{
		cv::Point((width * 0.6), height - height * 0.05),
		cv::Point((width * 0.5), height - height * 0.4),
		cv::Point(width - (width * 0.4), height - height * 0.4),
		cv::Point(width - (width * 0.05), height - height * 0.05)
	};

	cv::fillConvexPoly(roi_filter, left_points, 4, cv::Scalar(255, 0, 0));
	cv::fillConvexPoly(roi_filter, right_points, 4, cv::Scalar(255, 0, 0));
	cv::bitwise_and(inputimage, roi_filter, img_roi);
	//imshow("roi", roi_filter);

	return img_roi;
}