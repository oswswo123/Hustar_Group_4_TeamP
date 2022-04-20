#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

int main()
{
    Mat image(300, 400, CV_8U, Scalar(255));

    namedWindow("Keyboard Event", WINDOW_AUTOSIZE);
    imshow("Keyboard Event", image);

    while (1){
        int key = waitKey();
        if (key==27) break;

        switch(key){
            case 'a': cout << "a키 입력" << endl; break;
            case 'b': cout << "b키 입력" << endl; break;
            case 0x41: cout << "A키 입력" << endl; break;
            case 66: cout << "B키 입력" << endl; break;
            case 0x250000: cout << "왼쪽 화살표 키 입력" << endl; break;
            case 0x260000: cout << "위쪽 화살표 키 입력" << endl; break;
            case 0x270000: cout << "오른쪽 화살표 키 입력" << endl; break;
            case 0x280000: cout << "아래쪽 화살표 키 입력" << endl; break;
        }

    }
    destroyAllWindows();
    return 0;
}