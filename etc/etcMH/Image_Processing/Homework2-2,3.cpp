#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
using namespace cv;
using namespace std;

void put_string(Mat &, string, Point, int);

int main()
{
    // 비디오 캡쳐 및 수정
    Scalar red(0, 0, 255), blue(255, 0, 0), white(255, 255, 255), black(0, 0, 0);
    Point pt(30, 30), pt2(90, 90);                  // 시작좌표
    Rect red_rect(Point(30, 30), Size(320, 240));   //빨간 테두리 위한 사각형 선언
    Rect video_rect(Point(30, 30), Size(320, 240)); //영상 출력을 위한 rect 클래스
    Rect rect1(Point(30, 30), Size(100, 100));      //밝기 조절 rect 클래스
    Rect rect2(Point(250, 100), Size(80, 80));      //대비 조절 rect 클래스

    // Video 출력을 위한 선언
    VideoCapture video("cat.mp4");
    CV_Assert(video.isOpened());

    Mat image(300, 400, CV_8UC3, Scalar(blue)); // Main Window, 바탕은 Blue
    rectangle(image, red_rect, red, 3);         //빨간 사각형 그리기
   
    for (;;){
        Mat frame; // 윈도우창에 추가할 영상을 위한 Matrix
        video >> frame;
        resize(frame, frame, Size(320, 240));

        Mat Video_ROI = image(video_rect); // Video 출력을 위한 관심 영역
        Mat ROI1 = image(rect1);
        Mat ROI2 = image(rect2);

        frame.copyTo(Video_ROI); // 밝기 조절을 위한 관심 영역
        ROI1 = ROI1 + Scalar(50, 50, 50);
        ROI2 = ROI2 * 3;

        imshow("Main Window", image);
        if (waitKey(30) == 27)
            break;
    }
    video.release();
    return 0;
}

void put_string(Mat &frame, string text, Point pt, int value)
{
    text += to_string(value);
    Point shade = pt + Point(2,2);
    int font = FONT_HERSHEY_SIMPLEX;
    putText(frame, text, shade, font, 0.7, Scalar(0,0,0), 2);
    putText(frame, text, pt, font, 0.7, Scalar(120,200,90), 2);
}