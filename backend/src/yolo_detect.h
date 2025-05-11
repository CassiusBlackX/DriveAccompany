#ifndef YOLO_DETECT_H
#define YOLO_DETECT_H

#include <vector>
#include <string>
#include <array>

#include <opencv2/opencv.hpp>

#include "utils.h"

// 本来为了通用性考虑，这里其实应该能够从一个list中读出yolo的各个类，但是在本任务中，为了方便，直接枚举定义死了
enum YoloStatus {
    closed_eyes = 0,
    open_eyes = 1,
    closed_mouth = 2,
    open_mouth = 3,
    side_face = 4,
    phone = 5,
};

struct Detection {
    int class_id;
    double confidence;
    cv::Rect box;
    Detection() {}
    Detection(int class_id, double confidence, cv::Rect box) : class_id(class_id), confidence(confidence), box(box) {}
    bool operator<(const Detection& other) const {
        return confidence < other.confidence;
    }
};


class YoloDetector {
public:
    YoloDetector(std::string net_path, bool use_cuda);
    YoloDetector(std::string net_path, bool use_cuda, double nms_threashold, double confidence_threshold, double score_threshold);
    HumanStatus detect(cv::Mat& image);
private:
    cv::dnn::Net net;
    double nms_threshold;
    double confidence_threshold;
    double score_threshold;
    size_t num_classes = 6;
    // TODO should every status needs an additional threshold in case some specific status is more difficult to be detected

    cv::Mat format_yolov5(const cv::Mat& source);
    void drawBoundingBoxes(cv::Mat& image, std::vector<Detection> detections);

};

#endif // YOLO_DETECT_H