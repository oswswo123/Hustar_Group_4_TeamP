#include <opencv2/opencv.hpp>
#include "image_filter.h"
#include "set_roi.h"
#include "hough_cal.h"
#include "hough_regression.h"

int main() {
	// 이미지 실행
	//Mat image = imread("./road1.jpg", 1);
	//imshow("원본", image);

	// 동영상 실행(while 실행)
	cv::Mat image;
	cv::VideoCapture cap("./input.mp4");
	cap.read(image);

	//VideoWriter cap_writer, cap_writer_hough;
	int codec = cv::VideoWriter::fourcc('X', 'V', 'I', 'D');
	double fps = 20.0;
	//cap_writer.open("./output.avi", codec, fps, image.size(), CV_8UC3);
	//cap_writer_hough.open("./output_hough.avi", codec, fps, image.size(), CV_8UC3);

	
	while (true) {
		cap >> image;

		// 색상 필터 영역
		cv::Mat img_filter;
		img_filter = color_filter(image, false);

		// Gray Scale
		cv::cvtColor(img_filter, img_filter, cv::COLOR_BGR2GRAY);
		//imshow("grayscale", img_filter);

		// Canny Edge 검출
		cv::Mat img_edges;
		cv::Canny(img_filter, img_edges, 50, 150);
		//imshow("Canny", img_edges);

		// !! ROI 지정 영역 !!
		cv::Mat img_roi;
		img_roi = setting_roi(img_edges);

		// !! 허프 연산 영역 !!
		std::vector<cv::Vec4i> lines;
		lines = hough_transform(img_roi, 30, 20, 10, false);

		// !! Linear Regression 영역 !!
		std::vector<cv::Point> detection_lanepoint(4);
		detection_lanepoint = regression_and_detection_points(img_roi, lines, 0.8);

		// !! birds_eye view 영역 !!
		cv::Point2f source_vertices[4];
		cv::Point2f changed_vertices[4];
		int width, height;
		width = image.cols;
		height = image.rows;

		source_vertices[0] = cv::Point2f((width * 0.4), height - height * 0.4);
		source_vertices[1] = cv::Point2f(width - (width * 0.4), height - height * 0.4);
		source_vertices[2] = cv::Point2f(width - (width * 0.05), height - height * 0.05);
		source_vertices[3] = cv::Point2f((width * 0.05), height - height * 0.05);

		changed_vertices[0] = cv::Point(0, 0);			// left high
		changed_vertices[1] = cv::Point(width, 0);		// right high
		changed_vertices[2] = cv::Point(width, height);	// right low
		changed_vertices[3] = cv::Point(0, height);		// left low

		cv::Mat M = cv::getPerspectiveTransform(source_vertices, changed_vertices);
		cv::Mat dst(height, width, CV_8UC3);
		cv::warpPerspective(image, dst, M, dst.size(), cv::INTER_LINEAR, cv::BORDER_CONSTANT);
		//cv::imshow("dst", dst);

		cv::Mat dst_filter;
		dst_filter = color_filter(dst, false);

		cv::cvtColor(dst_filter, dst_filter, cv::COLOR_BGR2GRAY);
		//imshow("grayscale", img_filter);

		cv::Mat dst_edges;
		cv::Canny(dst_filter, dst_edges, 50, 150);
		//cv::imshow("dst_canny", dst_filter);

		std::vector<cv::Vec4i> dst_lines;
		dst_lines = hough_transform(dst_edges, 30, 20, 5, false);

		std::vector<cv::Point> dst_lanepoint(4);
		dst_lanepoint = regression_and_detection_points(dst_edges, dst_lines, 1.5);

		std::vector<cv::Point> dstdraw_points;
		cv::Mat dst_draw;
		dst.copyTo(dst_draw);

		dstdraw_points.push_back(dst_lanepoint[0]);	// left low
		dstdraw_points.push_back(dst_lanepoint[1]);	// left high
		dstdraw_points.push_back(dst_lanepoint[3]);	// right high
		dstdraw_points.push_back(dst_lanepoint[2]);	// right low
		
		cv::fillConvexPoly(dst_draw, dstdraw_points, cv::Scalar(120, 120, 0), cv::LINE_AA, 0);
		cv::addWeighted(dst_draw, 0.3, dst, 0.7, 0, dst);

		cv::line(dst, dst_lanepoint[0], dst_lanepoint[1], cv::Scalar(230, 0, 0), 3, cv::LINE_AA);
		cv::line(dst, dst_lanepoint[2], dst_lanepoint[3], cv::Scalar(230, 0, 0), 3, cv::LINE_AA);

		cv::imshow("bird view after", dst);
		// !! birds_eye view 영역 !!

		// !! line draw 영역 !!
		// 차선 사이 색칠
		std::vector<cv::Point> draw_points;
		cv::Mat img_draw;
		image.copyTo(img_draw);

		draw_points.push_back(detection_lanepoint[0]);	// left low
		draw_points.push_back(detection_lanepoint[1]);	// left high
		draw_points.push_back(detection_lanepoint[3]);	// right high
		draw_points.push_back(detection_lanepoint[2]);	// right low

		cv::fillConvexPoly(img_draw, draw_points, cv::Scalar(0, 230, 0), cv::LINE_AA, 0);
		cv::addWeighted(img_draw, 0.3, image, 0.7, 0, image);
		// 차선 그리기
		cv::line(image, detection_lanepoint[0], detection_lanepoint[1], cv::Scalar(0, 255, 0), 3, cv::LINE_AA);
		cv::line(image, detection_lanepoint[2], detection_lanepoint[3], cv::Scalar(0, 255, 0), 3, cv::LINE_AA);
		// !! line draw 영역 !!

		//cap_writer << image;

		cv::imshow("처리 후 결과", image);
		if (cv::waitKey(10) == 27) break;
	}
	//cv::waitKey(0);
	return 0;
}