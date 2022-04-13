#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

void onMouse(int, int, int, int, void*);

int main()
{
    Mat image(300, 400, CV_8U, Scalar(255));

    imshow("Mouse Event1", image);
    imshow("Mouse Event2", image);

    setMouseCallback("Mouse Event1", onMouse, 0);
    setMouseCallback("Mouse Event2", onMouse, 0);
    waitKey(0);

    return 0;
}

void onMouse(int event, int x, int y, int flags, void *param){

    switch(event){
        case EVENT_LBUTTONDOWN: cout << "마우스 왼쪽버튼 누르기" << endl; break;
        case EVENT_RBUTTONDOWN: cout << "마우스 오른쪽버튼 누르기" << endl; break;
        case EVENT_LBUTTONUP: cout << "마우스 왼쪽버튼 떼기" << endl; break;
        case EVENT_RBUTTONUP: cout << "마우스 오른쪽버튼 떼기" << endl; break;
        case EVENT_LBUTTONDBLCLK: cout << "마우스 왼쪽버튼 더블클릭" << endl; break;
    }
}