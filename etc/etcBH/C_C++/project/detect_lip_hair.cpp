#include <opencv2/opencv.hpp>
#include "preprocess.hpp"
#include "correct_angle.hpp"
#include "detect_area.hpp"

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
    std::vector<cv::Rect>  sub_obj;


    if (faces.size()>0)
    {
        float i = 1.15;
        while(true)
        {
            eyes_cascade.detectMultiScale(gray(faces[0]),eyes,i,7,0,cv::Size(25,20));
            if (eyes.size() == 2)
            {
                std::cout<<"눈 찾았다."<<std::endl;
                eyes_center.push_back(calc_center(eyes[0]+faces[0].tl()));
                eyes_center.push_back(calc_center(eyes[1]+faces[0].tl()));

                cv::Point2d face_center = calc_center(faces[0]);
                cv::Mat rot_mat = calc_rotMap(face_center, eyes_center);
                cv::Mat correct_img = correct_image(image, rot_mat, eyes_center);
                cv::circle(correct_img, eyes_center[0], 5, cv::Scalar(0,255,0),2);
                cv::circle(correct_img, eyes_center[1], 5, cv::Scalar(0,255,0),2);

                detect_hair(face_center, faces[0], sub_obj);
                sub_obj.push_back(detect_lip(face_center, faces[0]));
                sub_obj.push_back(detect_brow(eyes_center[0],eyes_center[1], faces[0]));

                cv::imshow("sub_obj[0]", correct_img(sub_obj[0]));
                cv::imshow("sub_obj[1]", correct_img(sub_obj[1]));
                cv::imshow("sub_obj[2]", correct_img(sub_obj[4]));

                cv::rectangle(correct_img, sub_obj[2], cv::Scalar(255,0,0),2);
                cv::rectangle(correct_img, sub_obj[3], cv::Scalar(255,0,0),2);

                cv::imshow("correct_img", correct_img);
                cv::waitKey();
                break;
            }
            else
            {
                std::cout<<"눈 못 찾았다."<<i<<std::endl;
            }
            i += 0.05;
            if (i > 10) break;

        }

    }
    return 0;
}