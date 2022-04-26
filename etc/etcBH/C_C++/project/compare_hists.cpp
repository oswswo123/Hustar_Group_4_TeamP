#include <opencv2/opencv.hpp>
#include "preprocess.hpp"
#include "correct_angle.hpp"
#include "detect_area.hpp"
#include "histo.hpp"
#include <cstdlib>

cv::RNG rng(12345);

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

    cv::Mat image = cv::imread("m정우성.jpg", cv::IMREAD_COLOR);
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
                eyes_center.push_back(calc_center(eyes[0]+faces[0].tl()));
                eyes_center.push_back(calc_center(eyes[1]+faces[0].tl()));

                cv::Point2d face_center = calc_center(faces[0]);
                cv::Mat rot_mat = calc_rotMap(face_center, eyes_center);
                cv::Mat correct_img = correct_image(image, rot_mat, eyes_center);
 
                cv::circle(correct_img, eyes_center[0], 5, cv::Scalar(0,0,255),2);
                cv::circle(correct_img, eyes_center[1], 5, cv::Scalar(0,0,255),2);
 
                //detect_hair(face_center, faces[0], sub_obj);
                // sub_obj.push_back(detect_lip(face_center, faces[0]));

                sub_obj.push_back(detect_bread(face_center, faces[0]));
                sub_obj.push_back(detect_mustache(face_center, faces[0])); 
                sub_obj.push_back(detect_cheek(face_center, faces[0]));
                sub_obj.push_back(detect_forehead(face_center, faces[0]));
                sub_obj.push_back(detect_brow(eyes_center[0],eyes_center[1], faces[0]));

                // 0 아랫수염 1 윗수염 2 볼 3 이마 4 눈썹

                cv::Mat masks[5], hists[5];
                make_masks(sub_obj, correct_img.size(), masks);
                calc_histos(correct_img, sub_obj, hists, masks);  

                double criteria1 = cv::compareHist(hists[0], hists[1], CV_COMP_CORREL);
                double criteria2 = cv::compareHist(hists[1], hists[2], CV_COMP_CORREL);
                double criteria3 = cv::compareHist(hists[3], hists[4], CV_COMP_CORREL);
                
                //double criteria3 = cv::compareHist(hists[4], hists[5], CV_COMP_CORREL);
                std::cout << cv::format("눈썹부분 유사도 %4.2f\n",criteria3);
                //std::cout << cv::format("눈썹부분 유사도 %4.2f\n",criteria3);

                cv::Mat img1, img2, mustache, cmustache, dstimage;
                
                correct_img(sub_obj[0]).copyTo(img1);
                correct_img(sub_obj[1]).copyTo(img2);

                cv::cvtColor(img1, img1, cv::COLOR_BGR2GRAY);
                cv::cvtColor(img2, img2, cv::COLOR_BGR2GRAY);

                cv::threshold(img1, img1, 125, 255, cv::THRESH_BINARY);
                cv::threshold(img2, img2, 125, 255, cv::THRESH_BINARY);

                cv::resize(img2,img2, img1.size());
                cv::vconcat(img1,img2, mustache);

                cv::imshow("dd",mustache);

                std::vector<std::vector<cv::Point>> contours;
                std::vector<cv::Vec4i> hierarchy;

                findContours(mustache, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, cv::Point(0, 0));

                double count = 0;
                for (int i = 0; i < contours.size(); i++)
                    {
                        count += 1;
                        cv::Scalar color = cv::Scalar(rng.uniform(0, 255), rng.uniform(0, 255), rng.uniform(0, 255));
                        drawContours(dstimage, contours, i, color, 2, 8, hierarchy, 0, cv::Point());
                        
                    }

                // imshow("dstimage", dstimage);
                std::cout << cv::format("cnt line %4.2f\n", count);

                //cv::Canny(img1,img1,200,255);
                //cv::Canny(img2,img2,200,255);

                cv::imshow("11111", img1);
                cv::imshow("22222", img2);


                cv::imshow("sub_obj[0]", correct_img(sub_obj[0]));
                cv::imshow("sub_obj[1]", correct_img(sub_obj[1]));
                cv::imshow("sub_obj[2]", correct_img(sub_obj[2]));
                cv::imshow("sub_obj[3]", correct_img(sub_obj[3]));
                cv::imshow("sub_obj[4]", correct_img(sub_obj[4]));


                cv::rectangle(correct_img, sub_obj[0], cv::Scalar(255,0,0),2);
                cv::rectangle(correct_img, sub_obj[1], cv::Scalar(255,0,0),2);
                cv::rectangle(correct_img, sub_obj[2], cv::Scalar(255,0,0),2);
                cv::rectangle(correct_img, sub_obj[3], cv::Scalar(255,0,0),2);
                cv::rectangle(correct_img, sub_obj[4], cv::Scalar(255,0,0),2);

                cv::imshow("correct_img", correct_img);
                cv::waitKey();
                break;
            }
             i += 0.05;
            if (i > 10) break;

        }

    }
    return 0;
}