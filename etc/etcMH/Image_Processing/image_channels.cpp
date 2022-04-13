#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

int main()
{
    Mat image = imread("noze.jpg", IMREAD_COLOR);
    CV_Assert(image.data);

    Mat bgr[3];
    split(image, bgr);

    imshow("image", image);
    imshow("blue channels", bgr[0]);
    imshow("green channels", bgr[1]);
    imshow("red channels", bgr[2]);
    waitKey();

    return 0;

}