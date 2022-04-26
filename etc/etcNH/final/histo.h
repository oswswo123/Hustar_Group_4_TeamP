#pragma once
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

// 선택된 영역만 히스토그램 계산
void draw_ellipse(cv::Mat& image, Rect2d obj, Scalar color, int thickness, float ratio)
{
	Point2d center = obj.tl() + (Point2d)obj.size() * 0.5; // 타원 중심
	Size2d size = (Size2d)obj.size() * 0.45; // 타원 크기
	ellipse(image, center, size, 0, 0, 360, color, thickness);

}

void calc_histo(const cv::Mat& img, cv::Mat& hist, Vec3i bins, Vec3f range, cv::Mat mask)
{
	int dims = img.channels(); // 히스토그램 차원 수 
	int channels[] = { 0, 1, 2 }; // 채널 목록
	int histSize[] = { bins[0], bins[1], bins[2] };

	float range1[] = { 0, range[0] };
	float range2[] = { 0, range[1] };
	float range3[] = { 0, range[2] };
	const float* ranges[] = { range1, range2, range3 }; // 모든 채널 화소범위

	calcHist(&img, 1, channels, mask, hist, dims, histSize, ranges);

}

// 마스크의 검은색 부분은 빈도를 계산하지 않는다
void calc_histos(cv::Mat correct_img, vector<Rect> sub_obj, Mat hists[4], Mat masks[4])
{
	Vec3i bins(64, 64, 64); // 히스토그램 계급 개수
	Vec3f ranges(256, 256, 256); // 각 채널 화소 범위

	for (int i = 0; i < (int)sub_obj.size(); i++) {
		Mat sub = correct_img(sub_obj[i]); // 검출 서브 영상 
		calc_histo(sub, hists[i], bins, ranges, masks[i]); // 히스토그램 계산
		//imshow(format("mask[%d]", i), masks[i]); // 마스크 영상 출력
		waitKey();
	}
}

void make_masks(vector<Rect> sub_obj, Size org_size, cv::Mat mask[4])
{
		cv::Mat base_mask(org_size, CV_8U, Scalar(0)); // 기본마스크
		draw_ellipse(base_mask, sub_obj[2], Scalar(255), -1, 0.45f); // 기본 마스크에 타원 그리기

		mask[0] = ~base_mask(sub_obj[0]);
		mask[1] = ~base_mask(sub_obj[1]);

		draw_ellipse(base_mask, sub_obj[3], Scalar(0), -1, 0.45f);
		mask[3] = ~base_mask(sub_obj[3]);
		mask[2] = base_mask(sub_obj[2]);
}

void make_masks_brow(std::vector<cv::Rect> sub_obj, cv::Size org_size, cv::Mat mask[1])
{
	cv::Mat base_mask(org_size, CV_8U, cv::Scalar(0));
	// draw_ellipse(base_mask, sub_obj[2], cv::Scalar(255), -1, 0.45f);

	mask[0] = base_mask(sub_obj[0]);
	// mask[1] = base_mask(sub_obj[1]);

	// draw_ellipse(base_mask, sub_obj[3], cv::Scalar(255), -1, 0.45f);
	// mask[3] = base_mask(sub_obj[3]);
	// mask[2] = base_mask(sub_obj[2]);
}


void calc_histos_brow(cv::Mat correct_img, std::vector<cv::Rect> sub_obj, cv::Mat hists[4], cv::Mat masks[1])
{
	cv::Vec3i bins(64, 64, 64);
	cv::Vec3i ranges(256, 256, 256);

	for (int i = 0; i < (int)sub_obj.size(); i++)
	{
		cv::Mat sub = correct_img(sub_obj[i]);
		calc_histo(sub, hists[i], bins, ranges, masks[i]);
		cv::imshow(cv::format("mask[%d]", i), masks[i]);
		// cv::waitKey();
	}
}
