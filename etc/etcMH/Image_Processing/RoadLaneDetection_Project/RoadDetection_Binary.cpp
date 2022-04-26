#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class RoadDetector
{
private:
        double img_size, img_center;
        double left_m, right_m;
        cv::Point left_b, right_b;
        bool left_detect = false, right_detect = false;

public:
        cv::Mat filter_binary(cv::Mat img)  // HSV 필터 변환
        {
            cv::Mat src, res;
            int threshHold = 140;

            img.copyTo(src);
            
            cvtColor(src, res, cv::COLOR_BGR2GRAY); // 명암도 영상으로 변환
            cv::threshold(res, res, threshHold, 255, cv::THRESH_BINARY);    // 0,1로 이진화
            return res;
        }

        cv::Mat limit_region(cv::Mat img_edges)
        {
            int width = img_edges.cols;
            int height = img_edges.rows;

            //사다리꼴 관심 영역 범위 계산을 위한 백분율
            double p11_width = 0.15, p21_width = 0.6;
            double p12_width = 0.4, p22_width = 0.5;
            double p13_width = 0.5, p23_width = 0.6;
            double p14_width = 0.4, p24_width = 0.85;
            double trap_height = 0.6;

            cv::Mat output;
            cv::Mat mask = cv::Mat::zeros(height, width, CV_8UC1);

            //관심 영역 정점 계산
            cv::Point points1[4]{
                cv::Point(width * p11_width, height),
                cv::Point(width * p12_width, height * trap_height),
                cv::Point(width * p13_width, height * trap_height),
                cv::Point(width * p14_width, height)};

            cv::Point points2[4]{
                cv::Point(width * p21_width, height),
                cv::Point(width * p22_width, height * trap_height),
                cv::Point(width * p23_width, height * trap_height),
                cv::Point(width * p24_width, height)};

            // cv::Point points[4]{
            //     cv::Point((width * (1 - trap_bottom_width)) / 2, height),
            //     cv::Point((width * (1 - trap_top_width)) / 2 , height - height * trap_height),
            //     cv::Point(width - (width * (1 - trap_top_width)) / 2, height - height * trap_height),
            //     cv::Point(width - (width * (1 - trap_bottom_width)) / 2, height)};
            
            // cv::fillConvexPoly(mask, points, 4, cv::Scalar(255, 0, 0));
            cv::fillConvexPoly(mask, points1, 4, cv::Scalar(255, 0, 0));
            cv::fillConvexPoly(mask, points2, 4, cv::Scalar(255, 0, 0));

            cv::imshow("ROI", mask);
            cv::bitwise_and(img_edges, mask, output);

            return output;
        }

        vector<cv::Vec4i> houghLines(cv::Mat img_mask)
        {
            vector<cv::Vec4i> line;

            cv::HoughLinesP(img_mask, line, 1, CV_PI/180, 30,15,10);
            return line;
        }

        vector<vector<cv::Vec4i>> separateLine(cv::Mat img_edges, vector<cv::Vec4i> lines)
        {
            vector<vector<cv::Vec4i>> output(2);
            cv::Point ini, fini;
            vector<double> slopes;
            vector<cv::Vec4i> selected_lines, left_lines, right_lines;
            double slope_thresh = 0.6;

            for (int i=0; i < lines.size(); i++){
                cv::Vec4i line = lines[i];
                ini = cv::Point(line[0], line[1]);
                fini = cv::Point(line[2], line[3]);

                double slope;
                if (fini.x - ini.x == 0)
                    slope = 999.0;
                else
                    slope = (static_cast<double>(fini.y) - static_cast<double>(ini.y)) / (static_cast<double>(fini.x) - static_cast<double>(ini.x));

                if (abs(slope) > slope_thresh)
                {
                    slopes.push_back(slope);
                    selected_lines.push_back(line);
                }
            }

            img_center = static_cast<double>((img_edges.cols / 2));

            for (int i = 0; i < selected_lines.size(); i++){
                ini = cv::Point(selected_lines[i][0], selected_lines[i][1]);
                fini = cv::Point(selected_lines[i][2], selected_lines[i][3]);

                if (slopes[i] > 0 && ini.x > img_center && fini.x > img_center){
                    right_lines.push_back(selected_lines[i]);
                    right_detect = true;
                }
                else if (slopes[i] < 0 && ini.x < img_center && fini.x < img_center)
                {
                    left_lines.push_back(selected_lines[i]);
                    left_detect = true;
                }
            }

            output[0] = right_lines;
            output[1] = left_lines;
            return output;
        }
        vector<cv::Point> regression(vector<vector<cv::Vec4i>> separated_lines, cv::Mat img_input)
        {
            // 선형 회귀를 통해 적합한 선 찾기
            vector<cv::Point> output(4);
            cv::Point p1, p2, p3, p4;
            cv::Vec4d left_line, right_line;
            vector<cv::Point> left_pts, right_pts;

            if(right_detect){
                for (auto i : separated_lines[0]){
                    p1 = cv::Point(i[0], i[1]);
                    p2 = cv::Point(i[2], i[3]);

                    right_pts.push_back(p1);
                    right_pts.push_back(p2);
                }

                if (right_pts.size() > 0){
                    cv::fitLine(right_pts, right_line, cv::DIST_L2, 0, 0.01, 0.01);
                    right_m = right_line[1] / right_line[0];
                    right_b = cv::Point(right_line[2], right_line[3]);
                }
            }

            if(left_detect){
                for (auto j : separated_lines[1]){
                    p3 = cv::Point(j[0], j[1]);
                    p4 = cv::Point(j[2], j[3]);

                    left_pts.push_back(p3);
                    left_pts.push_back(p4);
                }

                if (left_pts.size() > 0){
                    cv::fitLine(left_pts, left_line, cv::DIST_L2, 0, 0.01, 0.01);
                    left_m = left_line[1] / left_line[0];
                    left_b = cv::Point(left_line[2], left_line[3]);
                }
            }

            // 각각의 두점 계산
            int y1 = img_input.rows;
            int y2 = img_input.rows / 1.5;

            double right_x1 = ((y1 - right_b.y) / right_m ) + right_b.x;
            double right_x2 = ((y2 - right_b.y) / right_m ) + right_b.x;
            
            double left_x1 = ((y1 - left_b.y) / left_m ) + left_b.x;
            double left_x2 = ((y2 - left_b.y) / left_m ) + left_b.x;
            
            output[0] = cv::Point(right_x1, y1);
            output[1] = cv::Point(right_x2, y2);
            output[2] = cv::Point(left_x1, y1);
            output[3] = cv::Point(left_x2, y2);

            // cout << "output[0] is : " << output[0] << endl;
            // cout << "output[1] is : " << output[1] << endl;
            // cout << "output[2] is : " << output[2] << endl;
            // cout << "output[3] is : " << output[3] << endl;

            return output;
        }
        // string predictDir();
        cv::Mat drawLine(cv::Mat img_input, vector<cv::Point> lane)
        {
            //내부 다각형 그리는 함수
            vector<cv::Point> poly_points;
            cv::Mat output;

            img_input.copyTo(output);
            poly_points.push_back(lane[2]);
            poly_points.push_back(lane[0]);
            poly_points.push_back(lane[1]);
            poly_points.push_back(lane[3]);
            
            cv::fillConvexPoly(output, poly_points, cv::Scalar(0, 230, 30), cv::LINE_AA, 0);
            cv::addWeighted(output, 0.3, img_input, 0.7, 0, img_input); //영상 합치기

            cv::line(img_input, lane[0], lane[1], cv::Scalar(0,255,255), 5, cv::LINE_AA);
            cv::line(img_input, lane[2], lane[3], cv::Scalar(0,255,255), 5, cv::LINE_AA);
            // cv::putText(img_input, dir, cv::Point(520, 100), cv::FONT_HERSHEY_PLAIN, 3, cv::Scalar(255,255,255), 3, cv::LINE_AA);
            return img_input;
        }
        
};

int main()
{
    RoadDetector RLD;
    cv::Mat frame, img_filter, img_edges, img_mask, img_Hough_lines, img_lines, img_result;
    vector<cv::Vec4i> lines;
    vector<vector<cv::Vec4i>> separated_lines;
    vector<cv::Point> lane;
    string dir;

    vector<cv::Vec2f> hough_lines;

    cv::VideoCapture video("project_test.mp4");
    if(!video.isOpened()){
        cout << "ERROR!!: can not OPEN video..." << endl;
        return -1;
    }

    // cv::Mat image = cv::imread("road.jpeg", cv::IMREAD_COLOR);
    // CV_Assert(image.data);
    // cv::resize(image, image, cv::Size(480, 360));
    // cv::imshow("Original image", image);

    while (1)
    {
        video >> frame;
        if (frame.empty()){
        cout << "ERROR!!: can not READ video..." << endl;
        return -1;
        }

        resize(frame, frame, cv::Size(480, 360));
        cv::imshow("Original Frame", frame);

        // 흰색, 노란색 차선만 필터링
        img_filter = RLD.filter_binary(frame);
        cv::imshow("After filtering by GrayScale and binary", img_filter);
        // Canny Edge Detection으로 에지 추출
        cv::Canny(img_filter, img_edges, 50, 150);
        cv::HoughLines(img_edges, hough_lines, 1, CV_PI/180, 100);
        cv::imshow("After Canny Edge Detection, HoughLines", img_edges);
        // 바닥의 차선 검출을 위한 관심 영역
        img_mask = RLD.limit_region(img_edges);
        cv::imshow("After ROI processing", img_mask);
        // Hough 변환, 직선 성분 추출 (vector는 imshow가 안됨)
        lines = RLD.houghLines(img_mask);
        

        if (lines.size() > 0){
            separated_lines = RLD.separateLine(img_mask, lines);
            lane = RLD.regression(separated_lines, frame);
            img_result = RLD.drawLine(frame, lane);
            cv::imshow("After Drawing Line", img_result);
        }
        // cv::imshow("img_filter", img_filter);
        

        if (cv::waitKey(30) == 27) { break; }
    }
    video.release();
    return 0;

}