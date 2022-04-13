#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
using namespace cv;
using namespace std;

int main()
{
    // 비디오 캡쳐 및 수정
    double fps = 15;
    Size size(640, 480);
    int fourcc = VideoWriter::fourcc('D','I','V','X');
    VideoCapture capture(0);
    VideoWriter writer("flip_test.avi", fourcc, fps, size);
    
    CV_Assert(capture.isOpened());
    CV_Assert(writer.isOpened());

    // capture.set(CAP_PROP_FRAME_WIDTH, 400);
    // capture.set(CAP_PROP_FRAME_HEIGHT, 300);

    for (;;){
        Mat frame;
        capture >> frame;
        flip(frame, frame, 1);
        resize(frame, frame, Size(640, 480));
        writer << frame;

        imshow("Reverse original video file", frame);
        if (waitKey(30) == 27) break;
    }
    capture.release();
    return 0;
}