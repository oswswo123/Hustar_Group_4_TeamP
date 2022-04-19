#include <opencv2/opencv.hpp>

cv::Rect detect_lip(cv::Point2d face_center, cv::Rect face)
{
    cv::Point2d lip_center = face_center + cv::Point2d(0, face.height*0.3);
    cv::Point2d gap_size(face.width * 0.18, face.height * 0.1);

    cv::Point lip_start = lip_center - gap_size;
    cv::Point lip_end = lip_center + gap_size;

    return cv::Rect(lip_start, lip_end);
}

cv::Rect detect_forehead(cv::Point2d face_center, cv::Rect face)
{
    cv::Point2d forehead_center = face_center - cv::Point2d(0, face.height*0.4);
    cv::Point2d gap_size(face.width * 0.4, face.height * 0.1);

    cv::Point forehead_start = forehead_center - gap_size;
    cv::Point forehead_end = forehead_center + gap_size;

    return cv::Rect(forehead_start, forehead_end);
}

cv::Rect detect_brow(cv::Point2d eye_center1, cv::Point2d eye_center2, cv::Rect face)
{
    cv::Point2d brow_center = (eye_center1+eye_center2)*0.5 - cv::Point2d(0, face.height*0.1);
    cv::Point2d gap_size(face.width * 0.4, face.height * 0.05);

    cv::Point brow_start = brow_center - gap_size;
    cv::Point brow_end = brow_center + gap_size;

    return cv::Rect(brow_start, brow_end);
}

void detect_hair(cv::Point2d face_center, cv::Rect face, std::vector<cv::Rect> &hair_rect)
{
    cv::Point2d h_gap(face.width * 0.45, face.height*0.65);
    cv::Point2d pt1 = face_center - h_gap;
    cv::Point2d pt2 = face_center + h_gap;
    cv::Rect hair(pt1, pt2);

    cv::Size size(hair.width, hair.height*0.4);
    cv::Rect hair1(hair.tl(), size);
    cv::Rect hair2(hair.br() - (cv::Point)size, size);

    hair_rect.push_back(hair1);
    hair_rect.push_back(hair2);
    // hair_rect.push_back(hair);
}