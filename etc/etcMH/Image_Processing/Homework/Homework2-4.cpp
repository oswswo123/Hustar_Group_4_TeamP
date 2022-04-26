#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
using namespace cv;
using namespace std;

void calc_Histo(const Mat&, Mat&, int, int);
Mat make_palatte(int);
void draw_histo_hue(Mat, Mat&, Size);
// void onMouse(int, int, int, int, void *);
// void img_open(Mat img);

// Point draw_start, draw_end;

int main()
{
    Mat image = imread("flower.jpg", 1);
    CV_Assert(!image.empty());

    Rect rect(Point(100, 50), Size(100, 100));       //시작 좌표와 Size 객체로 빨간 테두리 위한 사각형 선언
    Mat ROI = image(rect);
    imshow("ROI", ROI);

    Mat HSV_img, HSV_arr[3];
    cvtColor(ROI, HSV_img, CV_BGR2HSV);
    split(HSV_img, HSV_arr);

    Mat hue_hist, hue_hist_img;
    calc_Histo(HSV_arr[0], hue_hist, 18, 180);  //계급수 18개
    draw_histo_hue(hue_hist, hue_hist_img, Size(360, 200));

    ROI = Scalar(255,255,255) - ROI;
    
    imshow("image", image);
    
    imshow("Hue_hist_img", hue_hist_img);
    waitKey(0);

    return 0;

}

void calc_Histo(const Mat& image, Mat& hist, int bins, int range_max = 256)
{
    int histSize[] = {bins};
    float range[] = {0, (float)range_max};
    int channels[] = {0};
    const float* ranges[] = {range};

    calcHist(&image, 1, channels, Mat(), hist, 1, histSize, ranges);
}

Mat make_palatte(int rows)
{
    Mat hsv(rows, 1, CV_8UC3);
    for (int i=0; i<rows; i++){
        uchar hue = saturate_cast<uchar>((float)i/rows*180);
        hsv.at<Vec3b>(i) = Vec3b(hue, 255,255);
    }

    cvtColor(hsv, hsv, CV_HSV2BGR);
    return hsv;
}

void draw_histo_hue(Mat hist, Mat &hist_img, Size size = Size(256,200))
{
    Mat hsv_palatte = make_palatte(hist.rows);

    hist_img = Mat(size, CV_8UC3, Scalar(255,255,255));
    float bin = (float)hist_img.cols / hist.rows;
    normalize(hist, hist, 0, hist_img.rows, NORM_MINMAX);

    for (int i=0; i<hist.rows; i++){
        float start_x = (i*bin);
        float end_x = (i+1)*bin;
        Point2f pt1(start_x, 0);
        Point2f pt2(end_x, hist.at<float>(i));

        Scalar color = hsv_palatte.at<Vec3b>(i);
        if (pt2.y>0) rectangle(hist_img, pt1, pt2, color, -1);
    }
    flip(hist_img, hist_img, 0);
}

// void onMouse(int event, int x, int y, int flags, void *param){
//     Point pt(x,y);
//     Size2d size(30,30);
//     Rect rect(pt, size);

//     int x2, y2;

//     switch(event){
//         case EVENT_LBUTTONDOWN: //사각형 30x30 그리기
//             draw_start = Point(x,y);
//             break;
//         case EVENT_MOUSEMOVE: //20픽셀 원 그리기

//         case EVENT_LBUTTONUP: //사각형 30x30 그리기
//             draw_end = Point(x,y);
//             break;
//     }
//     waitKey(0);
// }