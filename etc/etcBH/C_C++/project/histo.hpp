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

void make_masks()