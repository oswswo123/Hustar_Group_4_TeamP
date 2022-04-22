#include <opencv2/opencv.hpp>

void filter();
void cal_direct();
void supp_nonMax();
void trace();
void onChange();
void erosion();
void check_match();

void hw1();
void hw2();
void hw3();
void hw4();

int main()
{
    hw1();
    hw2();
    hw3();
    hw4();
}

void filter(cv::Mat img, cv::Mat& dst, cv::Mat mask)
{
    dst = cv::Mat(img.size(), CV_32F, cv::Scalar(0));
    cv::Point h_m = mask.size() / 2;

    for (int i = h_m.y; i<img.rows - h_m.y; i++)
    {
        for (int j = h_m.x; j < img.cols - h_m.x;j++)
        {
            float sum = 0;
            for (int u = 0; u < mask.rows; u++)
            {
                for (int v = 0; v < mask.cols; v++)
                {
                    int y = i + u - h_m.y;
                    int x = j + v - h_m.x;
                    sum += mask.at<float>(u,v) * img.at<uchar>(y,x);
                }
            }
            dst.at<float>(i,j) = sum;
        }
    }
}


void calc_direct(cv::Mat Gy, cv::Mat Gx, cv::Mat& direct)
{
    direct.create(Gy.size(),CV_8U);

    for (int i = 0; i<direct.rows;i++)
    {
        for (int j = 0; j<direct.cols;j++)
        {
            float gx = Gx.at<float>(i,j);
            float gy = Gy.at<float>(i,j);
            int theat = int(cv::fastAtan2(gy,gx)/45);
            direct.at<uchar>(i,j) = theat % 4;
        }
    }
}

void supp_nonMax(cv::Mat sobel, cv::Mat direct, cv::Mat& dst)
{
    dst = cv::Mat(sobel.size(), CV_32F, cv::Scalar(0));

    for (int i = 1; i < sobel.rows - 1; i++)
    {
        for (int j = 1; j < sobel.cols - 1; j++)
        {
            int dir = direct.at<uchar>(i,j);
            float v1, v2;
            if (dir == 0)
            {
                v1 = sobel.at<float>(i,j-1);
                v2 = sobel.at<float>(i,j+1);
            }
            else if (dir == 1)
            {
                v1 = sobel.at<float>(i+1,j+1);
                v2 = sobel.at<float>(i-1,j-1);
            }
            else if (dir == 2)
            {
                v1 = sobel.at<float>(i-1,j);
                v2 = sobel.at<float>(i+1,j);
            }
            else if (dir == 3)
            {
                v1 = sobel.at<float>(i+1,j-1);
                v2 = sobel.at<float>(i-1,j+1);
            }
            float center = sobel.at<float>(i,j);
            dst.at<float>(i,j) = (center > v1 && center > v2) ? center : 0 ;
        }
    }
}

void trace(cv::Mat max_so, cv::Mat& pos_ck, cv::Mat& hy_img, cv::Point pt, int low)
{
    cv::Rect rect(cv::Point(0,0), pos_ck.size());
    if (!rect.contains(pt)) return;

    if (pos_ck.at<uchar>(pt) == 0 && max_so.at<float>(pt) > low)
    {
        pos_ck.at<uchar>(pt) = 1;
        hy_img.at<uchar>(pt) = 255;

        trace(max_so, pos_ck, hy_img, pt + cv::Point(-1, -1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(0, -1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(+1, -1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(-1, 0), low);

        trace(max_so, pos_ck, hy_img, pt + cv::Point(+1, 0), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(-1, +1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(0, +1), low);
        trace(max_so, pos_ck, hy_img, pt + cv::Point(+1, +1), low);
    }
}

void hysteresis_th(cv::Mat max_so, cv::Mat& hy_img, int low, int high)
{
    cv::Mat pos_ck(max_so.size(),CV_8U,cv::Scalar(0));

    hy_img = cv::Mat(max_so.size(), CV_8U, cv::Scalar(0));

    for(int i = 0; i < max_so.rows; i++)
    {
        for (int j = 0; j < max_so.cols; j++)
        {
            if (max_so.at<float>(i, j) > high)
            {
                trace(max_so, pos_ck, hy_img, cv::Point(j,i), low);
            }
        }
    }
}

bool check_match(cv::Mat img, cv::Point start, cv::Mat mask, int mode = 0)
{
    for (int u = 0; u<mask.rows;u++)
    {
        for (int v = 0; v<mask.cols;v++)
        {
            cv::Point pt(v,u);
            int m = mask.at<uchar>(pt);
            int p = img.at<uchar>(start + pt);

            bool ch = (p == 255);
            if (m == 1 && ch == mode) return false;
        }
    }
    return true;
}

void erosion(cv::Mat img, cv::Mat& dst, cv::Mat mask)
{
    dst = cv::Mat(img.size(), CV_8U, cv::Scalar(0));
    if (mask.empty()) mask = cv::Mat(3, 3, CV_8UC1, cv::Scalar(1));
    cv::Point h_m = mask.size() / 2 ;
    for (int i = h_m.y; i < img.rows - h_m.y; i++)
    {
        for (int j = h_m.x; j < img.cols - h_m.x; j++)
        {
            cv::Point start = cv::Point(j,i) - h_m;
            bool check = check_match(img, start, mask, 0);
            dst.at<uchar>(i,j) = (check) ?255 : 0;
        }
    }
}

void hw1()
{
    cv::Mat image(cv::imread("road.jpg"));
    cv::Mat s_img[3];
    CV_Assert(image.data);

    float blur_filter[] = {1/9.f,1/9.f,1/9.f,1/9.f,1/9.f,1/9.f,1/9.f,1/9.f,1/9.f};
    float sharp_filter[] = {-1,-1,-1,-1,9,-1,-1,-1,-1};

    cv::split(image, s_img);
    

    cv::Mat blur_mask(3,3,CV_32F, blur_filter);
    cv::Mat sharp_mask(3,3,CV_32F, sharp_filter);

    cv::Mat blur_image[3];
    cv::Mat sharp_image[3];

    cv::Mat blur_image1;
    cv::Mat sharp_image1;

    for (int i = 0; i<3;i++)
    {
        filter(s_img[i],blur_image[i],blur_mask);
        filter(s_img[i],sharp_image[i],sharp_mask);
        blur_image[i].convertTo(blur_image[i],CV_8U);
        sharp_image[i].convertTo(sharp_image[i],CV_8U);
    }
    
    cv::merge(blur_image,3,blur_image1);
    cv::merge(sharp_image,3,sharp_image1);

    cv::imshow("origin",image);
    cv::imshow("blur", blur_image1);
    cv::imshow("sharp", sharp_image1);
    cv::waitKey(0);

    

}

void hw2()
{
    cv::Mat image = cv::imread("road.jpg",0);
    CV_Assert(image.data);
    cv::Mat gau_img, Gx, Gy, direct, sobel, canny, hy_img, max_sobel;

    int th1 = 150;
    int th2 = 100;

    cv::GaussianBlur(image, gau_img, cv::Size(5,5), 0.3);
    cv::Sobel(gau_img, Gx, CV_32F, 1, 0, 3);
    cv::Sobel(gau_img, Gy, CV_32F, 0, 1, 3);
    sobel = abs(Gx) + abs(Gy);
    // cv::magnitude(Gx,Gy,sobel);
    
    cv::namedWindow("canny");
    cv::createTrackbar("th1 :", "canny", &th1, 200);
    cv::createTrackbar("th2 :", "canny", &th2, 200);

    calc_direct(Gy,Gx,direct);
    supp_nonMax(sobel, direct, max_sobel);
    // cv::Canny(image, canny, 150, 100);
    // cv::imshow("opencv_canny", canny);


    while(true)
    {
        hysteresis_th(max_sobel, hy_img, th1, th2);
        cv::imshow("image", image);
        cv::imshow("canny", hy_img);
        if (cv::waitKey(30)==27) break;
    }
    
}

void hw3()
{
    cv::Mat image(cv::imread("textimg.jpeg"));
    CV_Assert(image.data);

    cv::Mat th_img, dst1, dst2, dst3;
    cv::threshold(image, th_img, 128, 255, cv::THRESH_BINARY);

    uchar data[] = {0, 1, 0, 1, 1, 1, 0, 1, 0};
    cv::Mat mask(3,3, CV_8UC1, data);
    erosion(th_img, dst1, (cv::Mat)mask);
    cv::morphologyEx(th_img, dst2, cv::MORPH_ERODE, mask);
    cv::morphologyEx(th_img, dst3, cv::MORPH_DILATE, mask);


    cv::imshow("image", image);
    //cv::imshow("이진 이미지", th_img);
    //cv::imshow("User_dilation", dst1);
    cv::imshow("침식 연산", dst2);
    cv::imshow("팽창 연산", dst3);

    cv::waitKey();
    
}

void hw4()
{
    cv::Mat image(cv::imread("coin.jpeg",0));
    cv::Matx<uchar,3,3> mask;
    mask << 0,1,0,1,1,1,0,1,0;
    cv::Mat blur_img, bin_img, mor_img;
    cv::GaussianBlur(image, blur_img, cv::Size(5,5), 0.3);
    cv::threshold(blur_img,bin_img,50,255,cv::THRESH_BINARY);
    cv::morphologyEx(bin_img, mor_img, cv::MORPH_OPEN, mask);

    cv::imshow("result",mor_img);
    cv::waitKey();

}