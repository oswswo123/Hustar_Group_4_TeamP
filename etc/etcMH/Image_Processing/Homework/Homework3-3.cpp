// Word 침식, 팽창 연산 수행하기

#include <opencv2/opencv.hpp>
#include <iostream>
using namespace std;
// using namespace cv;

bool check_match(cv::Mat, cv::Point, cv::Mat, int);
void erosion(cv::Mat, cv::Mat&, cv::Mat);
void dilation(cv::Mat, cv::Mat&, cv::Mat);

int main()
{
    cv::Mat image = cv::imread("word2.jpeg", 0);
    CV_Assert(image.data);
    cv::resize(image, image, cv::Size(360, 480));


    cv::Mat th_img, dst1, dst2;
    cv::threshold(image, th_img, 128, 255, cv::THRESH_BINARY);

    uchar data1[] = {
        0, 1, 0,
        1, 1, 1,
        0, 1, 0};

    uchar data2[] = {
        0, 1, 0,
        1, 1, 1,
        0, 1, 1};

    cv::Mat mask(3, 3, CV_8UC1, data1);

    erosion(th_img, dst1, (cv::Mat)mask);
    dilation(th_img, dst2, (cv::Mat)mask);

    cv::imshow("Original image", image);
    cv::imshow("Binary_Image", th_img);
    cv::imshow("My_Erosion", dst1);
    cv::imshow("My_Dilation", dst2);

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