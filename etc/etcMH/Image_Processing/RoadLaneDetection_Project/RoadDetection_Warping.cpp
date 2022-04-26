#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
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

        //사다리꼴 관심 영역 범위 계산을 위한 백분율
        double trap_bottom_width = 0.1;
        double trap_top_width = 0.4;
        double trap_height = 0.55;

public:
        void transform(cv::Mat& src, cv::Mat& dst)
        {
            int width = src.cols;
            int height = src.rows;

            cv::Point2f src_vertices[4];
            src_vertices[0] = cv::Point((width * trap_bottom_width), height - 30);
            src_vertices[1] = cv::Point((width * trap_top_width), height * 0.6);
            src_vertices[2] = cv::Point(width - (width * trap_top_width), height * 0.6);
            src_vertices[3] = cv::Point(width - (width * trap_bottom_width), height - 30);

            cv::Point2f dst_vertices[4];
            dst_vertices[0] = cv::Point(0, height);
            dst_vertices[1] = cv::Point(0, 0);
            dst_vertices[2] = cv::Point(width, 0);
            dst_vertices[3] = cv::Point(width, height);
            
            // 두 이미지간 관계 계산 후 warping
            cv::Mat M = cv::getPerspectiveTransform(src_vertices, dst_vertices);
            cv::warpPerspective(src, dst, M, dst.size(), cv::INTER_LINEAR, cv::BORDER_CONSTANT);

            cv::imshow("Result of Warping", dst);
        }

        cv::Mat filtering(cv::Mat img)
        {
            cv::Mat res, myROI;
            cv::UMat img_hsv;
            cv::UMat white_mask, white_image, yellow_mask, yellow_image;
            int threshHold = 128;
            img.copyTo(res);
            
            cv::Scalar lower_white = cv::Scalar(180,180,180);   //흰 차선
            cv::Scalar upper_white = cv::Scalar(255,255,255);
            cv::Scalar lower_yellow = cv::Scalar(10,100,100);   //노란 차선
            cv::Scalar upper_yellow = cv::Scalar(40,255,255);

            inRange(res, lower_white, upper_white, white_mask); // 지정값 이외에는 다 0으로 만들기
            cv::bitwise_and(res, res, white_image, white_mask); // mask 씌워진 부분만 출력
            
            cvtColor(res, img_hsv, cv::COLOR_BGR2HSV);

            inRange(img_hsv, lower_yellow, upper_yellow, yellow_mask);
            cv::bitwise_and(res, res, yellow_image, yellow_mask);

            cv::addWeighted(white_image, 1.0, yellow_image, 1.0, 0.0, res);

            cvtColor(res, res, cv::COLOR_BGR2GRAY);

            res = res * 1.2;

            return res;
        }

        cv::Mat limit_region(cv::Mat img_edges)
        {
            int width = img_edges.cols;
            int height = img_edges.rows;

            cv::Mat output;
            cv::Mat mask = cv::Mat::zeros(height, width, CV_8UC1);

            //관심 영역 정점 계산
            cv::Point points[4]{
                cv::Point((width * trap_bottom_width), height - 30),
                cv::Point((width * trap_top_width), height * trap_height),
                cv::Point(width - (width * trap_top_width), height * trap_height),
                cv::Point(width - (width * trap_bottom_width), height - 30)};

            cv::fillConvexPoly(mask, points, 4, cv::Scalar(255, 0, 0));
            cv::imshow("ROI", mask);

            cv::bitwise_and(img_edges, mask, output);

            return output;
        }

        vector<cv::Vec4i> houghLines(cv::Mat img_mask)
        {
            vector<cv::Vec4i> line;

            // 허프 변환, threshold: 라인 검출을 위한 최소 교차 수
            //          minLineLength: 직선의 최소 길이 (픽셀 단위)
            //          maxLineGap: 점들 사이 최대 거리 (이값보다 크면 다른 선으로 간주)
            cv::HoughLinesP(img_mask, line, 1, CV_PI/180, 20,10,5);
            return line;
        }

        vector<vector<cv::Vec4i>> separateLine(cv::Mat img_edges, vector<cv::Vec4i> lines)
        {
            vector<vector<cv::Vec4i>> output(2);
            cv::Point p1, p2;
            vector<double> slopes;
            vector<cv::Vec4i> selected_lines, left_lines, right_lines;
            double slope_thresh = 0.3;

            for (int i=0; i < lines.size(); i++){
                cv::Vec4i line = lines[i];
                p1 = cv::Point(line[0], line[1]);
                p2 = cv::Point(line[2], line[3]);

                double slope;
                if (p2.x - p1.x == 0)
                    slope = 999.0;
                else
                    slope = (p2.y - p1.y) / (double)(p2.x - p1.x);

                if (abs(slope) > slope_thresh)
                {
                    slopes.push_back(slope);
                    selected_lines.push_back(line);
                }
            }

            img_center = (double)(img_edges.cols / 2);

            for (int i = 0; i < selected_lines.size(); i++){
                p1 = cv::Point(selected_lines[i][0], selected_lines[i][1]);
                p2 = cv::Point(selected_lines[i][2], selected_lines[i][3]);

                if (slopes[i] > 0 && p1.x > img_center && p2.x > img_center){
                    right_lines.push_back(selected_lines[i]);
                    right_detect = true;
                }
                else if (slopes[i] < 0 && p1.x < img_center && p2.x < img_center)
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
            int y2 = 0;

            double right_x1 = ((y1 - right_b.y) / right_m ) + right_b.x;
            double right_x2 = ((y2 - right_b.y) / right_m ) + right_b.x;
            
            double left_x1 = ((y1 - left_b.y) / left_m ) + left_b.x;
            double left_x2 = ((y2 - left_b.y) / left_m ) + left_b.x;
            
            output[0] = cv::Point(right_x1, y1);
            output[1] = cv::Point(right_x2, y2);
            output[2] = cv::Point(left_x1, y1);
            output[3] = cv::Point(left_x2, y2);

            return output;
        }
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
            
            cv::fillConvexPoly(output, poly_points, cv::Scalar(255, 144, 30), cv::LINE_AA, 0);
            cv::addWeighted(output, 0.3, img_input, 0.7, 0, img_input); //영상 합치기

            cv::line(img_input, lane[0], lane[1], cv::Scalar(50,204,255), 2, cv::LINE_AA);
            cv::line(img_input, lane[2], lane[3], cv::Scalar(50,204,255), 2, cv::LINE_AA);
            
            return img_input;
        }
        
};