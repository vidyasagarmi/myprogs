#include <iostream>

using namespace std;

int main() {
    std::string key_uuid = "sc:poolserver:123452";
    std::string key;
    std::string uuid;
    std::string delim(":");

    std::size_t found = key_uuid.rfind(delim);
    key = key_uuid.substr(0, found);
    uuid = key_uuid.substr(found+1, key_uuid.length());
    cout << "KEY=" << key << endl;
    cout << "UUID=" << uuid << endl;
}
