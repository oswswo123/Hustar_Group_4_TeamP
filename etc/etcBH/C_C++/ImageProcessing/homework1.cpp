#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

VideoCapture capture;

void onMouse(int,int,int,int,void *);
void onChange(int value, void*);
void print_matInfo(string name, Mat img);
void put_string(Mat &frame, string text, Point pt, int value);
void zoom_bar(int value, void*);
void focus_bar(int value, void*);
void bright_bar(int value, void*);
void contrast_bar(int value, void*);

void hw1();
void hw2();
void hw3();
void hw4();
void hw5();
void hw6();
void open_mvi();

int main()
{   
     hw1();
     hw2();
     hw3();
     hw4();
     hw5();
     hw6();
    // open_mvi();
}


void hw1()
{
    Scalar blue(255, 0, 0), red(0,0,255), green(0, 255, 0);
    Scalar white(255,255,255);
    Point pt1(100,100), pt2(300,400);
    Mat image1(600,400, CV_8UC3, white);

    rectangle(image1, pt1, pt2, red, 3);

    imshow("1.", image1);
    waitKey(0);
}

void hw2()
{
    Scalar blue(255, 0, 0), red(0,0,255), green(0, 255, 0);
    Scalar white(255,255,255);
    
    Point pt1(100,100), pt2(400,300);
    Mat image2(400,600,CV_8UC3,white);

    Point center = (Point)image2.size() /2;
    
    ellipse(image2, center, Size(100,100), 0, 0, 180, blue,-1);
    ellipse(image2, center, Size(100,100), 0, 180, 360, red,-1);

    ellipse(image2, Point (250,200), Size(50,40),0,0,180, red, -1);
    ellipse(image2, Point (350,200), Size(50,40),0,180,360, blue, -1);

    imshow("2.", image2);
    waitKey(0);
}


int line_w = 5;
int circle_r = 25;

void hw3()
{

    Scalar blue(255, 0, 0), red(0,0,255), green(0, 255, 0);
    Scalar white(255,255,255);
    
    Point pt1(100,100), pt2(400,300);
    Mat image3(400,600,CV_8UC3,white);

    namedWindow("3.", WINDOW_AUTOSIZE);
    createTrackbar("선 굵기","3.", &line_w, 10, onChange, (void *) &image3);
    createTrackbar("원의 반지름","3.", &circle_r, 50, onChange, (void *) &image3);

    imshow("3.", image3);

    setMouseCallback("3.", onMouse, (void *) &image3);

    for(;;)
    {
        if(waitKey(100)==27)
        break;
    }
}

void onMouse(int event, int x, int y , int flags, void *image)
{
    Mat mouseimage = *(Mat*)image;
    Scalar draw_color(0,0,0);

    switch(event)
    {
        
        case EVENT_LBUTTONDOWN:
        if(flags==40)draw_color = Scalar(0,0,255);
        else if(flags==48) draw_color = Scalar(255,0,0);
        else draw_color = Scalar(0,0,0);
        circle(mouseimage, Point(x,y), circle_r, draw_color, line_w);
        imshow("3.", mouseimage);
        break;

        case EVENT_RBUTTONDOWN:
        if(flags==40)draw_color = Scalar(0,0,255);
        else if(flags==48) draw_color = Scalar(255,0,0);
        else draw_color = Scalar(0,0,0);
        rectangle(mouseimage, Point(x-15,y-15), Point(x+15,y+15),draw_color,line_w);
        imshow("3.",mouseimage);
        break;
    }
}

void onChange(int value, void * image)
{
    Mat changeimage = *(Mat*)image;
    int add_value = value;
    Mat tmp = changeimage + add_value;
    imshow("3.",tmp);
}

void print_matInfo(string name, Mat img)
{
    string mat_type;
    if (img.depth()==CV_8U) cout<<"CV_8U"<<endl;
    else if (img.depth() == CV_8S) cout<<"CV_8S"<<endl;
    else if (img.depth() == CV_16U) cout<<"CV_16U"<<endl;
    else if (img.depth() == CV_16S) cout<<"CV_16S"<<endl;
    else if (img.depth() == CV_32S) cout<<"CV_32S"<<endl;
    else if (img.depth() == CV_32F) cout<<"CV_32F"<<endl;
    else if (img.depth() == CV_64F) cout<<"CV_64F"<<endl;
    
}

void hw4()
{
    string filename = "readgray.jpeg";
    Mat gray2gray = imread(filename, IMREAD_GRAYSCALE);
    Mat gray2color = imread(filename, IMREAD_COLOR);
    CV_Assert(gray2gray.data && gray2color.data);

    vector<int> params_jpg, params_png;
    params_jpg.push_back(IMWRITE_JPEG_QUALITY);
    params_jpg.push_back(100);
    params_png.push_back(IMWRITE_PNG_COMPRESSION);
    params_jpg.push_back(9);

    imwrite("test1.jpg",gray2gray,params_jpg);
    imwrite("test1.png",gray2gray,params_png);
    imwrite("test2.jpg",gray2color,params_jpg);
    imwrite("test2.png",gray2color,params_png);
    
    imshow("gray2gray",gray2gray);
    imshow("gray2color", gray2color);
    waitKey(0);
}

void put_string(Mat &frame, string text, Point pt, int value)
{
    text += to_string(value);
    Point shade = pt + Point(2,2);
    int font = FONT_HERSHEY_SIMPLEX;
    putText(frame, text, shade, font, 0.7, Scalar(0,0,0),2);
    putText(frame, text, pt, font, 0.7, Scalar(120,200,90),2);
}



void zoom_bar(int value, void*)
{
    capture.set(CAP_PROP_ZOOM, value);
}

void focus_bar(int value, void*)
{
    capture.set(CAP_PROP_FOCUS, value);
}

void bright_bar(int value, void*)
{
    capture.set(CAP_PROP_BRIGHTNESS, value);
}

void contrast_bar(int value, void*)
{
    capture.set(CAP_PROP_CONTRAST, value);
}

void hw5()
{
    capture.open("babycat.mp4");
    CV_Assert(capture.isOpened());
    capture.set(CAP_PROP_FRAME_WIDTH, 400);
    capture.set(CAP_PROP_FRAME_HEIGHT, 300);
    capture.set(CAP_PROP_AUTOFOCUS, 0);
    capture.set(CAP_PROP_BRIGHTNESS, 0);

    int zoom = capture.get(CAP_PROP_ZOOM);
    int focus = capture.get(CAP_PROP_FOCUS);
    int bright = capture.get(CAP_PROP_BRIGHTNESS);
    int contrast = capture.get(CAP_PROP_CONTRAST);

    string title = "카메라 속성변경";
    namedWindow(title);
    createTrackbar("zoom", title, &zoom, 10, zoom_bar);
    createTrackbar("focus", title, &focus, 40, focus_bar);
    createTrackbar("bright", title, &bright, 255, bright_bar);
    createTrackbar("contrast", title, &contrast, 255, contrast_bar);


    for(;;)
    {
        Mat frame;
        capture >> frame;

        put_string(frame,"zoom: ",Point(10,240),zoom);
        put_string(frame,"focus: ",Point(10,270),focus);

        imshow(title, frame);
        if (waitKey(30) == 27){
             break;
        }
    }
}

void hw6()
{
double fps = 29.97;
int delay = cvRound(1000.0/fps);
Size size(640, 360);
int fourcc = VideoWriter::fourcc('D','X','5','0');

VideoWriter writer;
writer.open("savedmp4.mp4",fourcc,fps,size);


    capture.open("babycat.mp4");
    CV_Assert(capture.isOpened());
    string title = "동영상 반전";
    namedWindow(title);

    for(;;)
    {
        Mat frame;
        capture >> frame;
        Mat frame_fliped;
void open_mvi()
{
    capture.open("savedmp4.avi");
    CV_Assert(capture.isOpened());


     for(;;)
    {
        Mat frame;
        capture >> frame;

        imshow("동영상 열기", frame);
        if (waitKey(30) == 27){
             break;
        }
    }

}

        flip(frame,frame_fliped,1);

        // writer << frame_fliped;
        writer.write(frame_fliped);

        imshow(title, frame);
        imshow("flip", frame_fliped);

        if (waitKey(30) == 27){
             break;
        }
    }
}


void open_mvi()
{
    capture.open("savedmp4.mp4");
    CV_Assert(capture.isOpened());


     for(;;)
    {
        Mat frame;
        capture >> frame;

        imshow("동영상 열기", frame);
        if (waitKey(30) == 27){
             break;
        }
    }

}
