#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;


void onChange(int, void*);
Mat image;

int main()
{
    int value = 128;

    image = Mat(300, 400, CV_8UC1, Scalar(120));

    namedWindow("Trackbar_Event", WINDOW_AUTOSIZE);
    createTrackbar("밝기값", "Trackbar_Event", &value, 255, onChange);
    imshow("Trackbar_Event", image);

    waitKey(0);
    return 0;
}

void onChange(int value, void *param){

    int add_value = value - 130;
    cout << "추가 화소 값 " << add_value << endl;

    Mat tmp = image + add_value;
    imshow("Trackbar_Event", tmp);
}