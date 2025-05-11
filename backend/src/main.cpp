#include <iostream>
#include <string>
#include <fstream>
#include <crow/app.h>
#include <crow/logging.h>
#include <mutex>
#include <vector>
#include <unordered_map>

#include "yolo_detect.h"
#include "base64.h"
#include "utils.h"

#ifndef CMAKE_LISTS_PATH
#define CMAKE_LISTS_PATH "."
#endif

std::string backup_server_uri = "ws://202.114.212.195:50511/detect";
std::mutex error_mutex;
bool catastrophic_error_occurred = false;

void forward_to_backup(crow::websocket::connection& client_conn, const std::string& data, bool is_binary) {
    std::cout << "forward to backup" << std::endl;
    // try {
    //     auto ws = crow::websocket::connection::new_connection(client_conn.get_app(), backup_server_uri);
    //     ws->onopen([&](crow::websocket::connection& backup_conn) {
    //         if (is_binary) {
    //             backup_conn.send_binary(data);
    //         } else {
    //             backup_conn.send_text(data);
    //         }
    //     });
    //     ws->onmessage([&](crow::websocket::connection& backup_conn, const std::string& backup_data, bool backup_is_binary) {
    //         if (backup_is_binary) {
    //             client_conn.send_binary(backup_data);
    //         } else {
    //             client_conn.send_text(backup_data);
    //         }
    //     });
    //     ws->onclose([&](crow::websocket::connection& backup_conn, const std::string& reason, uint16_t code) {
    //         CROW_LOG_INFO << "Forwarded connection closed: " << reason << " with code: " << code;
    //     });
    //     ws->onerror([&](crow::websocket::connection& backup_conn, const std::string& message) {
    //         CROW_LOG_ERROR << "Forwarded connection error: " << message;
    //     });
    //     ws->connect();
    // } catch (const std::exception& e) {
    //     CROW_LOG_ERROR << "Error forwarding to backup server: " << e.what();
    // }
}

int main()
{
    // YoloDetector
    std::string weights_path = std::string(CMAKE_LISTS_PATH) + "/cfg/best.onnx";
    std::cout << "weight path: " << weights_path << std::endl;
    YoloDetector yolo_detector(weights_path, true);

    crow::SimpleApp app;
    CROW_WEBSOCKET_ROUTE(app, "/detect")
        .onopen([&](crow::websocket::connection &conn) {
            auto client_ip = conn.get_remote_ip();
            CROW_LOG_INFO << "new websocket connection from " << client_ip;
        })
        .onclose([&](crow::websocket::connection &conn, const std::string &reason, uint16_t code) {
            auto client_ip = conn.get_remote_ip();
            CROW_LOG_INFO << "websocket connection closed: " << reason << " with code: " << code << " from " << client_ip;
        })
        .onerror([&](crow::websocket::connection &conn, const std::string &message) {
            CROW_LOG_ERROR << "websocket connection error: " << message;
        })
        .onmessage([&yolo_detector](crow::websocket::connection &conn, const std::string &data, bool is_binary) {
            std::lock_guard<std::mutex> lock(error_mutex);
            if (catastrophic_error_occurred) {
                forward_to_backup(conn, data, is_binary);
                return;
            }

            if (!is_binary) {
                conn.send_text("Expected binary data!");
                return;
            }

            // decode the base64 encoded image data
            std::string decoded_data = base64::decode(data);
            std::vector<uchar> img_data(decoded_data.begin(), decoded_data.end());
            cv::Mat frame = cv::imdecode(img_data, cv::IMREAD_COLOR);

            if (frame.empty()) {
                CROW_LOG_ERROR << "Error: Could not decode image data.";
                conn.send_text("Error: Could not decode image data.");
                return;
            }

            try {
                // yolo detect
                HumanStatus status = yolo_detector.detect(frame);

                // encode the frame
                std::vector<uchar> buf;
                cv::imencode(".jpg", frame, buf);
                std::string bit_data(buf.begin(), buf.end());
                std::string encoded_frame = base64::encode(bit_data);

                // send the result to the client, in the form of strings, no bit data
                crow::json::wvalue result;
                result["detected_class"] = static_cast<int>(status);
                result["image"] = encoded_frame;
                conn.send_text(result.dump());
                
                // conn.send_binary(bit_data);  // do not send bit data
                CROW_LOG_INFO << "cur status: " << utils::human_status_string(static_cast<HumanStatus>(status));
            } catch (const std::exception &e) {
                CROW_LOG_ERROR << "Error: " << e.what();
                conn.send_text(e.what());
            }
        });

    // 捕获灾难性错误
    try {
        app.port(50511).multithreaded().run();
    } catch (const std::exception& e) {
        std::lock_guard<std::mutex> lock(error_mutex);
        CROW_LOG_ERROR << "Catastrophic error occurred: " << e.what();
        catastrophic_error_occurred = true;
    }

    return 0;
}