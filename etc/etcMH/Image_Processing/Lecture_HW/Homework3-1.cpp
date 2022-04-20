// Bluring and Sharpening Program

#include <opencv2/opencv.hpp>
#include <iostream>
using namespace std;

void filter(cv::Mat, cv::Mat&, cv::Mat);

int main()
{
    // 이미지 읽어오기 및 예외처리
    cv::Mat image = cv::imread("noze.jpg", cv::IMREAD_COLOR);
    CV_Assert(image.data);

    float data_bluring[] = {
        1 / 9.f, 1 / 9.f, 1 / 9.f,
        1 / 9.f, 1 / 9.f, 1 / 9.f,
        1 / 9.f, 1 / 9.f, 1 / 9.f};

    float data_sharpening[] = {
        0, -1, 0,
        -1, 5, -1,
        0, -1, 0};

    cv::Mat mask_blur(3, 3, CV_32F, data_bluring);
    cv::Mat mask_sharp(3, 3, CV_32F, data_sharpening);
    cv::Mat bluring[3], sharpening[3];
    cv::Mat blur, sharp;

    cv::Mat bgr_arr[3];
    cv::split(image, bgr_arr); // 0부터 2까지 BGR 순서로 image file split

    // Filtering 수행 및 image 병합
    filter(bgr_arr[0], bluring[0], mask_blur);
    filter(bgr_arr[1], bluring[1], mask_blur);
    filter(bgr_arr[2], bluring[2], mask_blur);

    filter(bgr_arr[0], sharpening[0], mask_sharp);
    filter(bgr_arr[1], sharpening[1], mask_sharp);
    filter(bgr_arr[2], sharpening[2], mask_sharp);

    merge(bluring, 3, blur);
    merge(sharpening, 3, sharp);

    // 병합된 Mat 클래스를 uchar 형식으로 변환
    blur.convertTo(blur, CV_8U);
    sharp.convertTo(sharp, CV_8U);

    cv::imshow("Original", image);
    cv::imshow("blur", blur);
    cv::imshow("sharp", sharp);
    cv::waitKey(0);

    return 0;

}

void filter(cv::Mat img, cv::Mat &dst, cv::Mat mask)
{
    dst = cv::Mat(img.size(), CV_32F, cv::Scalar(0));
    cv::Point h_m = mask.size() / 2;

    for (int i = h_m.y; i < img.rows - h_m.y; i++){
        for (int j = h_m.x; j < img.cols - h_m.y; j++){
            float sum = 0;
            for (int u = 0; u < mask.rows; u++){
                for (int v = 0; v < mask.cols; v++){
                    int y = i + u - h_m.y;
                    int x = j + v - h_m.x;
                    sum += mask.at<float>(u,v) * img.at<uchar>(y,x);
                }
            }
            dst.at<float>(i,j) = sum;
        }
    }
}