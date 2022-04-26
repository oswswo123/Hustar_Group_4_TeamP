#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include <vector>
#include "RoadDetection_Warping.cpp"

using namespace std;

int main()
{
    RoadDetector RLD;
    cv::Mat frame, img_warp, img_filter, img_edges, img_mask, img_lines, img_result;
    vector<cv::Vec4i> lines, lines2;
    vector<vector<cv::Vec4i>> separated_lines, separated_lines2;
    vector<cv::Point> lane, lane2;
    string dir;

    cv::VideoCapture video("project_test.mp4");
    if(!video.isOpened()){
        cout << "ERROR!!: can not OPEN video..." << endl;
        return -1;
    }

    while (1)
    {
        video >> frame;
        if (frame.empty()){
        cout << "ERROR!!: can not READ video..." << endl;
        return -1;
        }

        resize(frame, frame, cv::Size(480, 360));
        cv::imshow("Original Frame", frame);

        RLD.transform(frame, img_warp);
        //////////////////////////////////////////////////////////
        img_filter = RLD.filtering(img_warp);
        cv::imshow("After filtering to HSV, GrayScale", img_filter);
        // Canny Edge Detection으로 에지 추출
        cv::Canny(img_filter, img_edges, 50, 150);
        cv::imshow("After Canny Edge Detection", img_edges);
        // Hough 변환, 직선 성분 추출 (vector는 imshow가 안됨)
        lines = RLD.houghLines(img_edges);

        if (lines.size() > 0){
            separated_lines = RLD.separateLine(img_edges, lines);
            lane = RLD.regression(separated_lines, frame);
            img_result = RLD.drawLine(img_warp, lane);
            cv::imshow("After Drawing Line", img_result);
        }
        
        if (cv::waitKey(30) == 27) { break; }
    }
    video.release();
    return 0;

}