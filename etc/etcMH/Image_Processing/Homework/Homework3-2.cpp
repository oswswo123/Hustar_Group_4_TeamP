// canny edge detection Program

#include <opencv2/opencv.hpp>
#include <iostream>
using namespace std;
// using namespace cv;

void calc_direct(cv::Mat, cv::Mat, cv::Mat&);   // 기울기 방향 계산 함수
void supp_nonMax(cv::Mat, cv::Mat, cv::Mat&);   // 비 최대치 억제 함수
void trace(cv::Mat, cv::Mat&, cv::Mat&, cv::Point, int);    //에지 추적
void hysteresis_th(cv::Mat, cv::Mat&, int, int);    // 이력 임계값 수행
void th_high_bar(int, void *);
void th_low_bar(int, void *);


int main()
{
    cv::Mat image = cv::imread("noze.png", cv::IMREAD_GRAYSCALE);  // GRAYSCALE로 입력
    CV_Assert(image.data);

    cv::Mat gau_img, Gx, Gy, direct, sobel, max_sobel, hy_img, canny;

    int th_high = 150, th_low = 100;

    cv::GaussianBlur(image, gau_img, cv::Size(5,5), 0.3);   //Bluring을 위한 클래스
    cv::Sobel(gau_img, Gx, CV_32F, 1, 0, 3);    // x방향 마스크
    cv::Sobel(gau_img, Gy, CV_32F, 0, 1, 3);    // y방향 마스크
    sobel = abs(Gx) + abs(Gy);  // 절댓값 계산

    calc_direct(Gy, Gx, direct);    // 에지의 기울기 계산
    supp_nonMax(sobel, direct, max_sobel);  // 비 최대치 억제
    hysteresis_th(max_sobel, hy_img, 100, 150); // 이력 임계값

    string title = "My_canny edge";
    cv::namedWindow(title);
    cv::createTrackbar("Thresh Hold1", title, 0, 255);
    cv::createTrackbar("Thresh Hold2", title, 0, 255);

    cv::setTrackbarPos("Thresh Hold1", title, 150);
    cv::setTrackbarPos("Thresh Hold2", title, 100);

    while(true){
        th_high = cv::getTrackbarPos("Thresh Hold1", title);
        th_low = cv::getTrackbarPos("Thresh Hold2", title);
        hysteresis_th(max_sobel, hy_img, th_low, th_high);

        cv::imshow("image", image);
        cv::imshow(title, hy_img);

        if (cv::waitKey(30) == 27) break;
    }

    // cv::imshow("image", image);
    // cv::imshow(title, hy_img);

    cv::waitKey(0);

    return 0;
    
}


void calc_direct(cv::Mat Gy, cv::Mat Gx, cv::Mat& direct)   // 기울기 방향 계산 함수
{
    direct.create(Gy.size(), CV_8U);

    for (int i = 0; i < direct.rows; i++) {
        for (int j = 0; j < direct.cols; j++) {
            float gx = Gx.at<float>(i, j);
            float gy = Gy.at<float>(i, j);
            int theat = int(cv::fastAtan2(gy, gx) / 45); // 45도 근사
            direct.at<uchar>(i, j) = theat % 4;
        }
    }
}
void supp_nonMax(cv::Mat sobel, cv::Mat direct, cv::Mat& dst)   // 비 최대치 억제 함수
{
    dst = cv::Mat(sobel.size(), CV_32F, cv::Scalar(0));

    for (int i = 0; i < sobel.rows - 1; i++){
        for (int j = 0; j < sobel.cols - 1; j++){
            int dir = direct.at<uchar>(i,j);    // 기울기 값
            float v1, v2;
            if (dir == 0){  // 기울기 0
                v1 = sobel.at<float>(i, j - 1);
                v2 = sobel.at<float>(i, j + 1);
            }
            else if (dir == 1){ // 기울기 45
                v1 = sobel.at<float>(i + 1, j + 1);
                v2 = sobel.at<float>(i - 1, j - 1);
            }
            else if (dir == 2){ // 기울기 90
                v1 = sobel.at<float>(i - 1, j);
                v2 = sobel.at<float>(i + 1, j);
            }
            else if (dir == 3){ // 기울기 135
                v1 = sobel.at<float>(i + 1, j - 1);
                v2 = sobel.at<float>(i - 1, j + 1);
            }

            float center = sobel.at<float>(i, j);
            dst.at<float>(i, j) = (center > v1 && center > v2) ? center : 0;
        }
    }
}

void trace(cv::Mat max_so, cv::Mat& pos_ck, cv::Mat& hy_img, cv::Point pt, int low)    //에지 추적
{
    cv::Rect rect(cv::Point(0, 0), pos_ck.size());
    if (!rect.contains(pt))
        return;

    if (pos_ck.at<uchar>(pt) == 0 && max_so.at<float>(pt) > low)
    {
        pos_ck.at<uchar>(pt) = 1;   //추적 완료 표시
        hy_img.at<uchar>(pt) = 255; //에지 지정

        trace(max_so, pos_ck, hy_img, pt + cv::Point(-1, -1), low); //추적 함수 재귀호출
        trace(max_so, pos_ck, hy_img, pt + cv::Point(0, -1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(1, -1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(-1, 0), low);

        trace(max_so, pos_ck, hy_img, pt + cv::Point(1, 0), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(-1, 1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(0, 1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(1, 1), low);
    }
}

void hysteresis_th(cv::Mat max_so, cv::Mat& hy_img, int low, int high)
{
    cv::Mat pos_ck(max_so.size(), CV_8U, cv::Scalar(0));
    hy_img = cv::Mat(max_so.size(), CV_8U, cv::Scalar(0));

    for (int i = 0; i < max_so.rows; i++)
    { // 에지 영상 순회
        for (int j = 0; j < max_so.cols; j++)
        {
            if (max_so.at<float>(i, j) > high)                       //높은 임계값 검사
                trace(max_so, pos_ck, hy_img, cv::Point(j, i), low); // 임계 추적 시작
        }
    }
}