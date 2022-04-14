#include <opencv2/opencv.hpp>

void calc_histo();
void draw_histo();
void make_palatte();
void calc_histo();
void draw_histo_hue();

void hw1();
void hw2();
void hw3();
void hw4();

cv::VideoCapture capture;

int main()
{
    // hw1();
    hw2();
    // hw3();
    // hw4();
}


void hw1()
{
    cv::Mat image = cv::imread("cvimage.png", cv::IMREAD_COLOR);
    CV_Assert(image.data);
    cv::Scalar black(0,0,0);
    cv::Mat bgr[3];

    cv::Mat v_image((cv::Point)image.size(),CV_8U, cv::Scalar(0)); 
    
    cv::split(image, bgr);
    cv::Mat b_image[] = {bgr[0], v_image, v_image};
    cv::Mat g_image[] = {v_image, bgr[1], v_image};
    cv::Mat r_image[] = {v_image, v_image, bgr[2]};


    cv::Mat blue,green,red;

    cv::merge(b_image,3,blue);
    cv::merge(g_image,3,green);
    cv::merge(r_image,3,red);

    cv::imshow("image",image);
    
    cv::imshow("blue채널", blue);
    cv::imshow("green채널", green);
    cv::imshow("red채널", red);
    cv::waitKey(0);
}

void hw2()
{   
    capture.open("babycat.mp4");
    std::string title = "메인 윈도우";
    cv::Mat blue (300,400,CV_8UC3,(0,0,255));

    cv::imshow(title,blue);
    cv::rectangle(blue,cv::Rect(30,30,320,240),cv::Scalar(0,0,255), 10);

    cv::Mat frame, small_frame, roi;
    
    for(;;)
    {
        capture >> frame;
        cv::resize(frame,small_frame,cv::Size(320,240));
        roi = blue(cv::Rect(30,30,320,240));
        
        small_frame.copyTo(roi);

        cv::imshow(title, blue);
        if (cv::waitKey(10)==27) break;
    }
    
}

void hw3()
{
    cv::Mat image = cv::imread("good.jpg", cv::IMREAD_COLOR);
    cv::Mat roi1, roi2;
    cv::Mat sroi1[3], sroi2[3];

    roi1 = image(cv::Rect(200,200,200,200));
    roi2 = image(cv::Rect(500,200,200,200));
    cv::split(roi1, sroi1);
    cv::split(roi2, sroi2);

    sroi1[0] += 50;
    sroi1[1] += 50;
    sroi1[2] += 50;

    sroi2[0] *= 2;
    sroi2[1] *= 2;
    sroi2[2] *= 2;

    cv::merge(sroi1,3,roi1);
    cv::merge(sroi2,3,roi2);

    cv::imshow("hw3",image);
    cv::waitKey(0);
}

void calc_histo(cv::Mat &image, cv::Mat &hist, int bins, int range_max = 256)
{
    hist = cv::Mat(bins, 1, CV_32F, cv::Scalar(0));
    float gap = range_max / (float)bins;

    for (int i = 0; i<image.rows; i++)
    {
        for (int j = 0; j<image.cols;j++)
        {
            int idx = int(image.at<uchar>(i,j)/gap);
            hist.at<float>(idx)++;
        }
    }
}

void calc_histo1(const cv::Mat& image, cv::Mat& hist, int bins, int range_max = 256)
{
    int histSize[] = {bins};
    float range[] = {0, (float)range_max};
    int channels[] = {0};
    const float* ranges[] = {range};
    
    cv::calcHist(&image, 1, channels, cv::Mat(), hist, 1, histSize, ranges);
}

void draw_histo(cv::Mat hist, cv::Mat &hist_img, cv::Size size = cv::Size(256,200))
{
    hist_img = cv::Mat(size, CV_8U, cv::Scalar(255));
    float bin = (float)hist_img.cols / hist.rows;
    cv::normalize(hist, hist, 0, hist_img.rows, cv::NORM_MINMAX);
    
    for (int i = 0;i<hist.rows;i++)
    {
        float start_x = i * bin;
        float end_x = (i+1) * bin;
        cv::Point2f pt1(start_x,0);
        cv::Point2f pt2(end_x,hist.at<float>(i));

        if (pt2.y >0)
        {
            rectangle(hist_img, pt1, pt2, cv::Scalar(0), -1);
        }
        flip(hist_img, hist_img,0);
    }
}

cv::Mat make_palatte(int rows)
{
    cv::Mat hsv(rows,1, CV_8UC3);
    for (int i = 0; i<rows;i++)
    {
        uchar hue = cv::saturate_cast<uchar>((float)i/rows*180);
        hsv.at<cv::Vec3b>(i) = cv::Vec3b(hue,255,255);
    }
    cv::cvtColor(hsv,hsv,CV_HSV2BGR);
    return hsv;
}

void draw_histo_hue(cv::Mat hist, cv::Mat &hist_img, cv::Size size = cv::Size (256,200))
{
    cv::Mat hsv_palatte = make_palatte(hist.rows);

    hist_img = cv::Mat(size, CV_8UC3, cv::Scalar(255, 255, 255));
    float bin = (float)hist_img.cols / hist.rows;
    cv::normalize(hist, hist, 0, hist_img.rows, cv::NORM_MINMAX);

    for(int i = 0; i<hist.rows;i++)
    {
        float start_x = (i*bin);
        float end_x = (i+1) * bin;
        cv::Point2f pt1(start_x,0);
        cv::Point2f pt2(end_x, hist.at <float>(i));

        cv::Scalar color = hsv_palatte.at<cv::Vec3b>(i);
        if (pt2.y>0) cv::rectangle(hist_img, pt1, pt2, color, -1);

    }
    flip(hist_img, hist_img, 0);
}
void hw4()
{
    cv::Mat image = cv::imread("good.jpg");
    cv::Mat roi;
    cv::Mat sroi[3], roi2[3];
    cv::Mat hist, hist_img;
    cv::Mat HSV_img, HSV_arr[3];

    roi = image(cv::Rect(800,600,200,200));

    cv::cvtColor(roi, HSV_img, CV_BGR2HSV);
    cv::split(HSV_img, HSV_arr);
    
    calc_histo1(HSV_arr[0], hist,18,180);
    draw_histo_hue(hist, hist_img, cv::Size(360,200));

    cv::imshow("ROI",roi);
    cv::split(roi,sroi);

    sroi[0] *= 2;
    sroi[1] *= 2;
    sroi[2] *= 2;

    cv::merge(sroi,3,roi);
    cv::imshow("histogram",hist_img);
    cv::imshow("image",image);
    cv::waitKey(0);

}