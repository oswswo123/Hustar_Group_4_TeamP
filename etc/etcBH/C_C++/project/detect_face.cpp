#include <opencv2/opencv.hpp>
#include "preprocess.hpp"

cv::Point2d calc_center(cv::Rect obj)
{
    cv::Point2d c = (cv::Point2d)obj.size() / 2.0;
    cv::Point2d center = (cv::Point2d)obj.tl() + c;
    return center;
}

int main()
{
    cv::CascadeClassifier face_cascade, eyes_cascade;
    load_cascade(face_cascade, "haarcascade_frontalface_alt2.xml");
    load_cascade(eyes_cascade, "haarcascade_eye.xml");

    cv::Mat image = cv::imread("photo.jpg", cv::IMREAD_COLOR);
    CV_Assert(image.data);
    cv::Mat gray = preprocessing(image);

    std::vector<cv::Rect>  faces, eyes;
    std::vector<cv::Point2d> eyes_center;
    face_cascade.detectMultiScale(gray, faces, 1.1, 2, 0, cv::Size(100, 100));

    if (faces.size()>0)
    {
        eyes_cascade.detectMultiScale(gray(faces[0]),eyes,3,7,0,cv::Size(25,20));

        if (eyes.size() == 2)
        {
            for (size_t i = 0; i < eyes.size(); i++)
            {
                cv::Point2d center = calc_center(eyes[i] + faces[0].tl());
                cv::circle(image, center, 5, cv::Scalar(0,255,0), 2);
            }
        }
        cv::rectangle(image, faces[0], cv::Scalar(255,0,0),2);
        cv::imshow("image", image);
        cv::waitKey();
    }
    return 0;
}