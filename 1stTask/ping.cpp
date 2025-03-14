#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdlib>
#include <vector>
using namespace std;

void readSitesFromFile(const string& filename, vector<string>& sites) {
    ifstream file(filename);
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            line.erase(line.find_last_not_of("\n\r") + 1);
            sites.push_back(line);
        }
        file.close();
    } else {
        cout << "Unavailable file: " << filename << endl;
    }
}
int main() {
    ofstream csvFile("ping_results.csv");
    csvFile << "Site, Packet Count,Response Time (ms)\n";

    vector<string> sites;
    readSitesFromFile("sites.txt", sites);

    cout << "Data from file:" << endl;
    for (const auto& site : sites) {
        cout << site << endl;
    }

    for (const auto& site : sites) {
        string command = "ping -c 4 " + site;
        FILE* stream = popen(command.c_str(), "r");
        if (stream) {
            char buffer[128];
            string output;
            while (fgets(buffer, sizeof(buffer), stream) != nullptr) {
                output += buffer;
            }
            pclose(stream);
            int packetCount = 0;
            int responseTime = 0;
            stringstream ss(output);
            string line;
            while (getline(ss, line)) {
                if (line.find("packets transmitted") != string::npos) {
                    size_t pos = line.find("received");
                    packetCount = stoi(line.substr(0, pos - 1));
                }
                if (line.find("time=") != string::npos) {
                    size_t pos = line.find("time=");
                    responseTime = stoi(line.substr(pos + 5, line.find("ms") - pos - 5));
                }
            }

            csvFile << site << "," << packetCount << "," << responseTime;
            csvFile << "\n";
        } else {
            cout << "Failed to execute ping command for " << site << endl;
        }
    }

    csvFile.close();
    return 0;
}