#include <opencv2/opencv.hpp>

cv::Mat calc_rotMap(cv::Point2d face_center, std::vector<cv::Point2d> pt)
{
    cv::Point2d delta = (pt[0].x > pt[1].x) ? pt[0]-pt[1] : pt[1] - pt[0];
    double angle = cv::fastAtan2(delta.y, delta.x);

    cv::Mat rot_mat = getRotationMatrix2D(face_center, angle, 1);
    return rot_mat;
}

cv::Mat correct_image(cv::Mat image,cv::Mat rot_mat, std::vector<cv::Point2d>& eyes_center)
{
    cv::Mat correct_img;
    cv::warpAffine(image, correct_img, rot_mat, image.size(), cv::INTER_CUBIC);

    for(int i = 0 ; i < eyes_center.size(); i++)
    {
        cv::Point3d coord(eyes_center[i].x, eyes_center[i].y, 1);
        cv::Mat dst = rot_mat * (cv::Mat)coord;
        eyes_center[i] = (cv::Point2d)dst;
    }
    return correct_img;
}