#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

void bgr2hsi(Mat img, Mat &hsv);

int main()
{
    Mat image = imread("logo.png", IMREAD_COLOR);
    CV_Assert(image.data);

    Scalar white(255,255,255);
    Mat HSI_img, HSV_img, hsi[3], hsv[3];
    
    bgr2hsi(image, HSI_img);    // 사용자 정의 HSI 변환 함수
    cvtColor(image, HSV_img, CV_BGR2HSV);   //opencv 내장 HSV 변환 함수
    split(HSI_img, hsi);
    split(HSV_img, hsv);
    
    imshow("Original Image", image);
    // imshow("RGB_image", RGB_img);
    // imshow("RGB_arr[0]-R", RGB_arr[0]);
    // imshow("RGB_arr[0]-G", RGB_arr[1]);
    // imshow("RGB_arr[0]-B", RGB_arr[2]);
    waitKey(0);

    return 0;

}

void bgr2hsi(Mat img, Mat &hsv)
{
    Mat hsi = Mat(img.size(), CV_32FC3);

    for (int i=0; i<img.rows; i++){
        for (int j=0; j<img.cols; j++){
            float B = img.at<Vec3b>(i, j)[0];
            float G = img.at<Vec3b>(i, j)[1];
            float R = img.at<Vec3b>(i, j)[2];

            float s = 1 - 3 * min(R, min(G, B)) / (R + G + B);
            float v = (R + G + B) / 3.0f;

            float tmp1 = ((R - G) + (R - B)) * 0.5;
            float tmp2 = sqrt((R - G) * (R - B) + (G - B) * (G - B));
            float angle = acos(tmp1 / tmp2) * (180.f / CV_PI);
            float h = (B <= G) ? angle : 360 - angle;

            hsi.at<Vec3f>(i, j) = Vec3f(h / 2, s * 255, v);
        }
    }
    hsi.convertTo(hsv, CV_8U);
}