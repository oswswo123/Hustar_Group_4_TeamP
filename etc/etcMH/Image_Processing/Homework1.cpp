#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

void onMouse(int, int, int, int, void *);
void onChange(int, void *);
void put_string(Mat &frame, string text, Point pt, int value);
void zoom_bar(int value, void *);
void focus_bar(int value, void *);
void brightness_bar(int value, void *);
void contrast_bar(int value, void *);

VideoCapture capture;

Scalar red(0,0,255), blue(255,0,0), white(255,255,255), black(0,0,0);    //색깔 선언
Mat image_mouse(400, 600, CV_8UC3, white); // 마우스 이벤트 바탕은 화이트
int line_value = 5, radius_value = 25;

int main()
{
    Mat image_rect(400, 600, CV_8UC3, Scalar(white)); // 사각형 이미지 바탕은 화이트
    Mat image_circle(400, 600, CV_8UC3, Scalar(white)); // 태극문양 이미지2 바탕은 화이트

    Point pt1(100, 100);  // 시작좌표
    Point center = (Point)image_circle.size()/2;
    Point mini_center1(center.x-50+3.125,center.y-18.75), mini_center2(center.x+50-3.125,center.y+18.75);
    Size2d size_red_rect(200, 300); // 사각형의 사이즈
    Size2d size_circle(100,100);

    Rect red_rect(pt1, size_red_rect); //시작 좌표와 Size 객체로 빨간 사각형 선언
    rectangle(image_rect, red_rect, red, -1);    //빨간 사각형 그리기

    //태극 문양을 위한 원 그리기
    ellipse(image_circle, center, size_circle, 0, 0, 30, red, -1);
    ellipse(image_circle, center, size_circle, 0, 210, 360, red, -1);
    ellipse(image_circle, center, size_circle, 0, 30, 210, blue, -1);
    circle(image_circle, mini_center1, 50, red, -1);   //원 그리기
    circle(image_circle, mini_center2, 50, blue, -1);   //원 그리기
    
    int font = FONT_HERSHEY_COMPLEX;
    namedWindow("Drawing a red rectangle", WINDOW_AUTOSIZE);
    imshow("Drawing a red rectangle", image_rect);

    namedWindow("Drawing a Circle", WINDOW_AUTOSIZE);
    imshow("Drawing a Circle", image_circle);

    namedWindow("Mouse Event", WINDOW_AUTOSIZE);
    setMouseCallback("Mouse Event", onMouse, 0);
    createTrackbar("Thickness of Line", "Mouse Event", &line_value, 10, onChange);
    createTrackbar("Radius of Circle", "Mouse Event", &radius_value, 50, onChange);
    imshow("Mouse Event", image_mouse);

    //이미지 파일 jpg와 png로 저장
    string filename = "noze.jpg";
    Mat img_gray = imread(filename, IMREAD_GRAYSCALE);
    CV_Assert(img_gray.data);
    imshow("It's noze", img_gray);

    vector<int> params_jpg, params_png;
    params_jpg.push_back(IMWRITE_JPEG_QUALITY);
    params_jpg.push_back(100);
    params_png.push_back(IMWRITE_PNG_COMPRESSION);
    params_png.push_back(9);

    imwrite("test.jpg", img_gray, params_jpg); // jpg가 파일크기가 훨씬 적음 7.0 KB
    imwrite("test.png", img_gray, params_png);

    while(1){
        if (waitKey(30) == 27) break;
    }
    
    return 0;
}

void onMouse(int event, int x, int y, int flags, void *param){
    Point pt(x-15,y-15), center(x,y);
    Size2d size(30,30);
    Rect rect(pt, size);

    switch(event){
        case EVENT_LBUTTONDOWN: //사각형 30x30 그리기
            if(flags & EVENT_FLAG_CTRLKEY){
                rectangle(image_mouse, rect, red, line_value);    //사각형 그리기
                imshow("Mouse Event", image_mouse);
            }else if (flags & EVENT_FLAG_SHIFTKEY){
                rectangle(image_mouse, rect, blue, line_value);    //사각형 그리기
                imshow("Mouse Event", image_mouse);
            }else{
                rectangle(image_mouse, rect, black, line_value);    //사각형 그리기
                imshow("Mouse Event", image_mouse);
            }
            cout << "마우스 왼쪽버튼 누르기" << endl; break;
        case EVENT_RBUTTONDOWN: //20픽셀 원 그리기
            if(flags & EVENT_FLAG_CTRLKEY){
                circle(image_mouse, center, radius_value, red, -1);   //원 그리기
                imshow("Mouse Event", image_mouse);
            }else if (flags & EVENT_FLAG_SHIFTKEY){
                circle(image_mouse, center, radius_value, blue, -1);   //원 그리기
                imshow("Mouse Event", image_mouse);
            }else{
                circle(image_mouse, center, radius_value, black, -1);   //원 그리기
                imshow("Mouse Event", image_mouse);
            }
            cout << "마우스 오른쪽버튼 누르기" << endl; break;
    }

    waitKey(0);
}

void onChange(int value, void * userdata){
    int add_value = value;
    Mat tmp = image_mouse + add_value;
    imshow("Mouse Event", tmp);
}