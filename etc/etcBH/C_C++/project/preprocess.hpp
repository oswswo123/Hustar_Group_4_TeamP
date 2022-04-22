#include <opencv2/opencv.hpp>


void load_cascade(cv::CascadeClassifier& cascade, std::string fname)
{
    std::string path = "/home/piai/opencv/data/haarcascades/";
    std::string full_name = path + fname;
    CV_Assert(cascade.load(full_name));
}

cv::Mat preprocessing(cv::Mat image)
{
    cv::Mat gray;
    cv::cvtColor(image, gray, CV_BGR2GRAY);
    cv::equalizeHist(gray,gray);

    return gray;
}