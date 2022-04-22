#include <opencv2/opencv.hpp>

void calc_Histo(const cv::Mat& img, cv::Mat& hist, cv::Vec3i bins, cv::Vec3f range, cv::Mat mask)
{
    int dims = img.channels();
    int channels[] = {0,1,2};
    int histSize[] = {bins[0], bins[1], bins[2]};

    float range1[] = {0,range[0]};
    float range2[] = {0,range[1]};
    float range3[] = {0,range[2]};
    const float* ranges[] = {range1, range2, range3};

    cv::calcHist(&img, 1, channels, mask, hist, dims, histSize, ranges);
}

void draw_ellipse(cv::Mat& image, cv::Rect2d obj, cv::Scalar color, int thickness, float ratio)
{
    cv::Point2d center = obj.tl() + (cv::Point2d)obj.size() * 0.5;
    cv::Size2d size = (cv::Size2d)obj.size() * 0.45;
    cv::ellipse(image, center, size, 0, 0, 360, color, thickness);
}

void make_masks(std::vector<cv::Rect> sub_obj, cv::Size org_size, cv::Mat mask[4]) 
{
    cv::Mat base_mask(org_size, CV_8U, cv::Scalar(0));
    draw_ellipse(base_mask, sub_obj[2], cv::Scalar(255), -1, 0.45f);

    mask[0] = base_mask(sub_obj[0]);
    mask[1] = base_mask(sub_obj[1]);

    draw_ellipse(base_mask, sub_obj[3], cv::Scalar(255), -1, 0.45f);
    mask[3] = base_mask(sub_obj[3]);
    mask[2] = base_mask(sub_obj[2]);
}


void calc_histos(cv::Mat correct_img, std::vector<cv::Rect> sub_obj, cv::Mat hists[4], cv::Mat masks[4])
{
    cv::Vec3i bins(64, 64, 64);
    cv::Vec3i ranges(256, 256, 256);

    for (int i = 0; i < (int)sub_obj.size(); i++)
    {
        cv::Mat sub = correct_img(sub_obj[i]);
        calc_Histo(sub, hists[i], bins, ranges, masks[i]);
        cv::imshow(cv::format("mask[%d]",i), masks[i]);
        // cv::waitKey();
    }
}