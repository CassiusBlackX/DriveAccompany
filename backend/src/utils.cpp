#include "utils.h"

namespace utils{
std::string human_status_string(HumanStatus status) {
    switch (status) {
        case HumanStatus::normal:
            return std::string("normal");
        case HumanStatus::sleeping:
            return std::string("sleeping");
        case HumanStatus::yawn:
            return std::string("yawn");
        case HumanStatus::side:
            return std::string("side");
        case HumanStatus::phoning:
            return std::string("phoning");
        default:
            return std::string("unknown");
    }
}
}