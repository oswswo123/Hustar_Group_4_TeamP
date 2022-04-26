#include <opencv2/opencv.hpp>
#include <iostream>
using namespace cv;
using namespace std;

int main()
{
    Mat image = imread("logo2.png", IMREAD_COLOR);
    CV_Assert(image.data);

    Mat zFillM(image.rows, image.cols, CV_8UC1, Scalar(0));
    Mat bgr_arr[3];
    split(image, bgr_arr);

    Mat R[] = {zFillM, zFillM, bgr_arr[2]};
    Mat G[] = {zFillM, bgr_arr[1], zFillM};
    Mat B[] = {bgr_arr[0], zFillM, zFillM};

    merge(R, 3, bgr_arr[2]);
    merge(G, 3, bgr_arr[1]);
    merge(B, 3, bgr_arr[0]);


    imshow("Original Image", image);
    // imshow("RGB_image", RGB_img);
    imshow("bgr_arr[0]-B", bgr_arr[0]);
    imshow("bgr_arr[0]-G", bgr_arr[1]);
    imshow("bgr_arr[0]-R", bgr_arr[2]);
    waitKey(0);

    return 0;

}