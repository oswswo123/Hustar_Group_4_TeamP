#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <bits/stdc++.h>

using namespace std;

int find_intersection(cv::Vec4i l1, cv::Vec4i l2);
void extract_segments(cv::Mat img_segments[], cv::Mat img,int segments[], int n_segments);
void merge_segments(cv::Mat img_segments[],cv::Mat img, int segments[], int n_segments);
cv::Mat find_edges(cv::Mat img);