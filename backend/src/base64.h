#ifndef _BASE64_H_
#define _BASE64_H_

#include <string>
#include <vector>
#include <stdexcept>

namespace base64 {
    std::string encode(const std::string &in);
    std::string decode(const std::string &in);
}

#endif // _BASE64_H_

