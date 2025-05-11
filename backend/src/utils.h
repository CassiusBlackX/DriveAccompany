#ifndef _UTILS_H_
#define _UTILS_H_

#include <string>

#include <crow/logging.h>

enum HumanStatus {
    normal,
    sleeping,
    yawn,
    side,
    phoning,
};

namespace utils{
std::string human_status_string(HumanStatus status);
}

#endif