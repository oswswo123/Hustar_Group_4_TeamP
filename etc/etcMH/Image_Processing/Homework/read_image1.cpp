#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

void print_matInfo(string, Mat);

int main()
{
    string filename = "noze.jpg";
    Mat gray2gray = imread(filename, IMREAD_GRAYSCALE);
    Mat gray2color = imread(filename, IMREAD_COLOR);
    CV_Assert(gray2gray.data && gray2color.data);

    Rect roi(100,100, 1,1);
    cout << "행렬 좌표 (100,100) 화소값 " << endl;
    cout << "gray2gray " << gray2gray(roi) << endl;
    cout << "gray2color " << gray2color(roi) << endl << endl;

    print_matInfo("gray2gray", gray2gray);
    print_matInfo("gray2color", gray2color);
    imshow("gray2gray", gray2gray);    
    imshow("gray2color", gray2color);

    waitKey(0);

    return 0;
}

void print_matInfo(string name, Mat img){
    string mat_type;
    if (img.depth() == CV_8U) mat_type = "CV_8U";
    else if (img.depth() == CV_8S) mat_type = "CV_8S";
    else if (img.depth() == CV_16U) mat_type = "CV_16U";
    else if (img.depth() == CV_16S) mat_type = "CV_16S";
    else if (img.depth() == CV_32S) mat_type = "CV_32S";
    else if (img.depth() == CV_32F) mat_type = "CV_32F";
    else if (img.depth() == CV_64F) mat_type = "CV_64F";

    cout << name << endl;;
    cout << format(": depth(%d) channels(%d) -> 자료형: ", img.depth(), img.channels()) << endl;
    cout << "str" << "C" << img.channels() << endl;
}