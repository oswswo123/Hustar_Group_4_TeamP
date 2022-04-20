#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <bits/stdc++.h>
#include <opencv2/core/core.hpp>
#include <opencv2/video/tracking.hpp>
#include <opencv2/video/video.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/objdetect/objdetect.hpp>
//#include <opencv2/videoio.hpp>
#include <iostream>
#include <cstring>
#include <vector>

using namespace std;

int lowThreshold = 70;
int highThreshold = 150;

int find_intersection(cv::Vec4i l1, cv::Vec4i l2)
{
	double m1, m2, c1, c2;

	m1 = ((double)l1[3] - l1[1]) / ((double)l1[2] - l1[0]);
	c1 = (double)l1[3] - m1 * l1[2];

	m2 = ((double)l2[3] - l2[1]) / ((double)l2[2] - l2[0]);
	c2 = (double)l2[3] - m2 * l2[2];

	double yi, xi;
	if (m1 != 0 || m2 != 0)
	{
		xi = (c1 - c2) / (m2 - m1);
		yi = m2 * xi + c2;
	}
	else
	{
		return 10000;
	}

	// if lines are parallel and on road surface but orientation not correct
	if (int(xi) < -200 || int(xi) > 1200)
		return 10000;

	return (int)yi;
}

void extract_segments(cv::Mat img_segments[], cv::Mat img,int segments[], int n_segments)
{
	int i, cum_length = 0;

	img_segments[0] = img(cv::Rect(0, 0, 1000, segments[0])).clone();
	cum_length += segments[0];

	for (i = 1; i <= n_segments - 2; i++)
	{
		img_segments[i] = img(cv::Rect(0, cum_length, 1000, segments[i])).clone();
		cum_length += segments[i];
	}

	img_segments[n_segments - 1] = img(cv::Rect(0, cum_length, 1000, 1000 - cum_length)).clone();
	return;
}

void merge_segments(cv::Mat img_segments[],cv::Mat img, int segments[], int n_segments)
{
	int i, cum_length=0;
	img_segments[0].copyTo(img(cv::Rect(0, 0, 1000, segments[0])));
	cum_length+=segments[0];

	for(i=1;i<=n_segments-2;i++)
	{
		img_segments[i].copyTo(img(cv::Rect(0, cum_length, 1000, segments[i])));
		cum_length+=segments[i];
	}

	img_segments[n_segments-1].copyTo(img(cv::Rect(0, cum_length, 1000, 1000-cum_length)));
	return;
}

cv::Mat find_edges(cv::Mat img)
{
	//dynamic canny
	
	cv::Mat edges;
    cv::cvtColor(img, img, CV_BGR2GRAY);
    cv::medianBlur(img, img, 9);

	/*int maxci,maxcj,count,maxcount;
	maxci=-99;
	maxcj=-99;
	cout<<"hi"<<endl;
	maxcount=-99;
	for(int i=0;i<500;i++)
		{
			for(int j=i;j<500;j++)
			{
				count=0;
				cout<<"hi2"<<endl;
				Canny( img, edges, i, j, 3 );
				vector<Vec4i> lines;
				HoughLinesP(edges, lines, 1, CV_PI/180, 500, 100, 50 );
				cout<<lines.size();		
			for(int k=0;k<lines.size();k++)
				{
					double m=((double)lines[k][3]-lines[k][1])/((double)lines[k][2]-lines[k][0]);
					if((m<0.4&&m>0)||(m>-0.4&&m<0))
					{

						count++;
					}
					if(count>maxcount)
						{count=maxcount;
							maxci=i;
							maxcj=j;
						}

				}
			}
		}
	cout<<maxci<<" "<<maxcj;
	Canny( img, edges,maxci, maxcj, 3 );*/
	cv::Canny( img, edges, lowThreshold, highThreshold, 3);
	cv::imshow("bw", img);
	cv::imshow("edges", edges);

	return edges;
}