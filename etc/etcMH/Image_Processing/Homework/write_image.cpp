#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

int main()
{
    Mat img8 = imread("flower.jpg", IMREAD_COLOR);
    CV_Assert(img8.data);

    vector<int> params_jpg, params_png;
    params_png.push_back(IMWRITE_PNG_COMPRESSION);
    params_png.push_back(9);

    resize(img8, img8, Size(360, 203));
    // imwrite("noze.jpg", img8, params_jpg); // jpg가 파일크기가 훨씬 적음 7.0 KB
    imwrite("flower.jpg", img8, params_png);

    return 0;
}