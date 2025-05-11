#include <iostream>
#include <string>
#include <vector>
#include <array>

#include "yolo_detect.h"

constexpr float YOLO_INPUT_WIDTH = 640.0F;
constexpr float YOLO_INPUT_HEIGHT = 640.0F;

namespace {
    const std::array<cv::Scalar, 6> colors = {
        cv::Scalar(0, 0, 255),  // closed_eyes
        cv::Scalar(0, 255, 0),  // open_eyes
        cv::Scalar(255, 0, 0),  // closed_mouth
        cv::Scalar(255, 255, 0),  // open_mouth
        cv::Scalar(255, 0, 255),  // side_face
        cv::Scalar(0, 255, 255),  // phone
    };

    std::string yolo_status_string(YoloStatus status) {
        switch (status) {
            case YoloStatus::closed_eyes:
                return "closed_eyes";
            case YoloStatus::open_eyes:
                return "open_eyes";
            case YoloStatus::closed_mouth:
                return "closed_mouth";
            case YoloStatus::open_mouth:
                return "open_mouth";
            case YoloStatus::side_face:
                return "side_face";
            case YoloStatus::phone:
                return "phone";
            default:
                return "unknown";
        }
    }
}

YoloDetector::YoloDetector(std::string net_path, bool use_cuda) {
    auto result = cv::dnn::readNet(net_path);
    if (use_cuda) {
        result.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
        result.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA);
        std::cout << "Using CUDA backend" << std::endl;
    }
    else {
        result.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
        result.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);
        std::cout << "Using OpenCV backend" << std::endl;
    }
    net = result;
    nms_threshold = 0.4f;
    confidence_threshold = 0.4f;
    score_threshold = 0.4f;
    std::cout << "num_classes: " << num_classes << " nms_threshold: " << nms_threshold << " confidence_threshold: " << confidence_threshold << " score_threshold: " << score_threshold << std::endl;
}

YoloDetector::YoloDetector(std::string net_path, bool use_cuda, double nms_threashold, double confidence_threshold, double score_threshold) {
    auto result = cv::dnn::readNet(net_path);
    if (use_cuda) {
        result.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
        result.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA);
        std::cout << "Using CUDA backend" << std::endl;
    }
    else {
        result.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
        result.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);
        std::cout << "Using OpenCV backend" << std::endl;
    }
    net = result;
    nms_threshold = nms_threashold;
    confidence_threshold = confidence_threshold;
    score_threshold = score_threshold;
    std::cout << "num_classes: " << num_classes << " nms_threshold: " << nms_threshold << " confidence_threshold: " << confidence_threshold << " score_threshold: " << score_threshold << std::endl;
}

cv::Mat YoloDetector::format_yolov5(const cv::Mat& source){
    int col = source.cols;
    int row = source.rows;
    int _max = std::max(col, row);
    cv::Mat result = cv::Mat::zeros(_max, _max, CV_8UC3);
    source.copyTo(result(cv::Rect(0, 0, col, row)));
    return result;
}

void YoloDetector::drawBoundingBoxes(cv::Mat& image, std::vector<Detection> detections) {
    for (auto detection : detections) {
        // 画矩形框
        cv::rectangle(image, detection.box, colors[detection.class_id], 2);

        // 生成标签
        std::string label = yolo_status_string(static_cast<YoloStatus>(detection.class_id)) + ": " + std::to_string(detection.confidence);
        int baseLine;
        cv::Size labelSize = cv::getTextSize(label, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
        int top = std::max(detection.box.y, labelSize.height);

        // 画标签
        cv::putText(image, label, cv::Point(detection.box.x, top), cv::FONT_HERSHEY_SIMPLEX, 0.5, colors[detection.class_id], 1);
    }
}

HumanStatus YoloDetector::detect(cv::Mat& image) {
    cv::Mat blob;
    auto input_image = format_yolov5(image);

    cv::dnn::blobFromImage(input_image, blob, 1.0 / 255.0, cv::Size(YOLO_INPUT_WIDTH, YOLO_INPUT_HEIGHT), cv::Scalar(), true, false);
    net.setInput(blob);
    std::vector<cv::Mat> outputs;
    net.forward(outputs, net.getUnconnectedOutLayersNames());

    float x_factor = static_cast<float>(input_image.cols) / YOLO_INPUT_WIDTH;
    float y_factor = static_cast<float>(input_image.rows) / YOLO_INPUT_HEIGHT;

    float *data = (float*)outputs[0].data;

    static const int dimensions = num_classes + 5;
    static constexpr int rows = 25200;  // INPUT_WIDTH = INPUT_HEIGHT = 640

    std::vector<int> class_ids;
    std::vector<float> confidences;
    std::vector<cv::Rect> boxes;
    std::vector<Detection> detections;

    for(int i=0; i < rows; i++) {
        float confidence = data[4];
        if (confidence >= confidence_threshold) {
            float* classes_scores = data + 5;
            cv::Mat scores(1, num_classes, CV_32FC1, classes_scores);
            cv::Point class_id;
            double max_class_score;
            minMaxLoc(scores, 0, &max_class_score, 0, &class_id);
            if(max_class_score > score_threshold) {
                confidences.push_back(confidence);
                class_ids.push_back(class_id.x);

                float x = data[0];
                float y = data[1];
                float w = data[2];
                float h = data[3];
                int left = int((x - 0.5 * w) * x_factor);
                int top = int((y - 0.5 * h) * y_factor);
                int width = int(w * x_factor);
                int height = int(h * y_factor);
                boxes.push_back(cv::Rect(left, top, width, height));
            }
        }
        data += dimensions;
    }

    std::vector<int> nms_result;
    cv::dnn::NMSBoxes(boxes, confidences, score_threshold, nms_threshold, nms_result);

    // draw bounding boxes
    // drawBoundingBoxes(image, boxes, class_ids, confidences);

    for (size_t i=0; i<nms_result.size(); i++) {
        int idx = nms_result[i];
        detections.emplace_back(class_ids[idx], confidences[idx], boxes[idx]);
    }
    drawBoundingBoxes(image, detections);
    sort(detections.begin(), detections.end());

    bool eyes_closed = false;
    bool mouth_closed = false;
    bool mouth_open = false;
    for (int i=detections.size()-1; i >= 0; i--) {
        int index = nms_result[i];
        switch (class_ids[index]) {
            case YoloStatus::phone:  // if phone is detected, than HumanStatus must be phone, directly return
                return HumanStatus::phoning;
            case YoloStatus::side_face:  // if side_face is detected, than HumanStatus must be side_face
                return HumanStatus::side;
            case YoloStatus::open_mouth:
                mouth_open = true;
                break;
            case YoloStatus::closed_eyes:
                eyes_closed = true;
                break;
            case YoloStatus::closed_mouth:
                mouth_closed = true;
                break;
        }
        // whether one is closing eyes or is normal
        if (eyes_closed && mouth_closed) {
            // only when two eyes are closed and mouth is open, the status is yawn
            return HumanStatus::sleeping;
        }
    }
    if (mouth_open) {  
        // only when there is no other status but mouth open, it is yawn
        return HumanStatus::yawn;
    }
    return HumanStatus::normal;
}