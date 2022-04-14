// 동전 객체 검출을 위한 전처리

#include <opencv2/opencv.hpp>
#include <iostream>
using namespace std;
// using namespace cv;

bool check_match(cv::Mat, cv::Point, cv::Mat, int);
void erosion(cv::Mat, cv::Mat&, cv::Mat);
void dilation(cv::Mat, cv::Mat&, cv::Mat);


int main()
{
    int no;
    cv::Mat image = cv::imread("coin.jpeg", cv::IMREAD_COLOR);
    CV_Assert(image.data);
    cv::resize(image, image, cv::Size(480, 360));

    cv::Mat gray, sobel, th_img, morph;
    cv::Mat kernel(10, 10, CV_8UC1, cv::Scalar(1));
    cv::Size size(5, 5);
    double sigmaX = 0.3 * ((size.width - 1) * 0.5 - 1) + 0.8;
    double sigmaY = 0.3 * ((size.height - 1) * 0.5 - 1) + 0.8;
    cvtColor(image, gray, CV_BGR2GRAY);

    cv::GaussianBlur(gray, gray, size, sigmaX, sigmaY);  // 가우시안 블러링
    cv::threshold(gray, th_img, 50, 255, cv::THRESH_BINARY);    //이진화
    cv::morphologyEx(th_img, morph, cv::MORPH_OPEN, kernel);    //모폴로지 열림 연산

    cv::imshow("image", image);
    cv::imshow("Morphology opening", morph);

    cv::waitKey(0);

    return 0;
    
}

bool check_match(cv::Mat img, cv::Point start, cv::Mat mask, int mode = 0)
{
    for (int u = 0; u < mask.rows; u++){
        for (int v = 0; v < mask.cols; v++){
            cv::Point pt(v,u);
            int m = mask.at<uchar>(pt);
            int p = img.at<uchar>(start + pt);

            bool ch = (p == 255);
            if (m == 1 && ch == mode) return false;
        }
    }

    return true;
}
void erosion(cv::Mat img, cv::Mat& dst, cv::Mat mask)
{
    dst = cv::Mat(img.size(), CV_8U, cv::Scalar(0));
    if (mask.empty())
        mask = cv::Mat(3, 3, CV_8UC1, cv::Scalar(1));

    cv::Point h_m = mask.size() / 2;
    for (int i = h_m.y; i < img.rows - h_m.y; i++){
        for (int j = h_m.x; j < img.cols - h_m.x; j++){
            cv::Point start = cv::Point(j, i) - h_m;
            bool check = check_match(img, start, mask, 0);
            dst.at<uchar>(i, j) = (check) ? 255 : 0;
        }
    }
}

void dilation(cv::Mat img, cv::Mat& dst, cv::Mat mask)
{
    dst = cv::Mat(img.size(), CV_8U, cv::Scalar(0));
    if (mask.empty()) mask = cv::Mat(3, 3, CV_8UC1, cv::Scalar(0));

    cv::Point h_m = mask.size() / 2;
    for (int i = h_m.y; i < img.rows - h_m.y; i++){
        for (int j = h_m.x; j < img.cols - h_m.x; j++){
            cv::Point start = cv::Point(j, i) - h_m;
            bool check = check_match(img, start, mask, 1);
            dst.at<uchar>(i, j) = (check) ? 0 : 255;
        }
    }
}