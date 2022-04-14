#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

void put_string(Mat &frame, string text, Point pt, int value);
void zoom_bar(int value, void *);
void focus_bar(int value, void *);
void brightness_bar(int value, void *);
void contrast_bar(int value, void *);

VideoCapture capture;

Scalar red(0,0,255), blue(255,0,0), white(255,255,255), black(0,0,0);    //색깔 선언

int main()
{
    // 비디오 캡쳐 및 수정
    capture.open(0);
    CV_Assert(capture.isOpened());

    capture.set(CAP_PROP_FRAME_WIDTH, 400);
    capture.set(CAP_PROP_FRAME_HEIGHT, 300);
    capture.set(CAP_PROP_AUTOFOCUS, 0);
    capture.set(CAP_PROP_BRIGHTNESS, 150);

    int zoom = capture.get(CAP_PROP_ZOOM);
    int focus = capture.get(CAP_PROP_FOCUS);
    int brightness = capture.get(CAP_PROP_BRIGHTNESS);
    int contrast = capture.get(CAP_PROP_CONTRAST);

    string title = "Set_Video file";
    namedWindow(title);
    createTrackbar("zoom", title, &zoom, 10, zoom_bar);
    createTrackbar("focus", title, &focus, 40, focus_bar);
    createTrackbar("brightness", title, &brightness, 255, brightness_bar);
    createTrackbar("contrast", title, &contrast, 255, contrast_bar);

    for (;;){
        Mat frame;
        capture >> frame;

        put_string(frame, "zoom: ", Point(10,240), zoom);
        put_string(frame, "focus: ", Point(10,270), focus);
        put_string(frame, "brightness: ", Point(10,300), brightness);
        put_string(frame, "contrast: ", Point(10,330), contrast);

        imshow(title, frame);
        if (waitKey(30) == 27) break;
    }

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

void zoom_bar(int value, void *) {capture.set(CAP_PROP_ZOOM, value);}
void focus_bar(int value, void *) {capture.set(CAP_PROP_FOCUS, value);}
void brightness_bar(int value, void *) {capture.set(CAP_PROP_BRIGHTNESS, value);}
void contrast_bar(int value, void *) {capture.set(CAP_PROP_CONTRAST, value);}