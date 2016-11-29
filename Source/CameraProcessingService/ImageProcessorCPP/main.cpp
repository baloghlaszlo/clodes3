#include <iostream>
#include <vector>
#include <random>

#include <opencv2/opencv.hpp>
#include <opencv2/bgsegm.hpp>

int main() {
    std::random_device r;
    std::default_random_engine e1(r());
    std::uniform_int_distribution<int> ud(0, 255);

    // ---------------------------------------------------

    std::vector<cv::CascadeClassifier> detectors;

    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_eye.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_eye_tree_eyeglasses.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_frontalcatface.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_frontalcatface_extended.xml"));
    detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_frontalface_alt.xml"));
    detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_frontalface_alt2.xml"));
    detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_frontalface_alt_tree.xml"));
    detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_frontalface_default.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_fullbody.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_lefteye_2splits.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_lowerbody.xml"));
    detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_profileface.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_righteye_2splits.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_smile.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/haarcascade_upperbody.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/lbpcascade_profileface.xml"));
    //detectors.emplace_back(cv::CascadeClassifier("cascade/lbpcascade_frontalface.xml"));

    cv::VideoCapture vid("rtsp://192.168.1.105:8554/unicast");
    if (!vid.isOpened()) {
        std::cout << "VideoCapture is not opened" << std::endl;
        return -1;
    }

    //for (int i = 0; i < 5; ++i) vid.grab();

    cv::Mat frame;
    while(vid.read(frame)) {
        cv::Mat gray;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        cv::equalizeHist(gray, gray);

        //cv::imshow("test", gray);
        //cv::waitKey(0);

        for(auto& detector : detectors) {
            std::vector<cv::Rect> objects;
            detector.detectMultiScale(gray, objects, 1.4, 1);

            cv::Scalar color(ud(r), ud(r), ud(r));
            for (auto& rect : objects) {
                cv::rectangle(frame, rect, color);
            }
        }

        cv::imshow("test", frame);
        cv::waitKey(1);
    }
}

//int main() {
//    cv::VideoCapture vid("test/video0.avi");
//    if (!vid.isOpened()) {
//        std::cout << "VideoCapture is not opened" << std::endl;
//        return -1;
//    }
//
//    int index = 0;
//    cv::Mat frame, mask;
//    auto pmog = cv::bgsegm::createBackgroundSubtractorGMG();
//
//    while(vid.read(frame)) {
//        if (index >= 120 && index % 10 == 0) {
//            cv::resize(frame, frame, cv::Size(), 0.5, 0.5);
//            cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
//            cv::GaussianBlur(frame, frame, cv::Size(3, 3), 2);
//            pmog->apply(frame, mask);
//
//            cv::imshow("test", frame);
//            cv::waitKey(100);
//
//            cv::imshow("test", mask);
//            cv::waitKey(100);
//        } else if (index < 120) {
//            cv::resize(frame, frame, cv::Size(), 0.5, 0.5);
//            cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
//            cv::GaussianBlur(frame, frame, cv::Size(3, 3), 2);
//            pmog->apply(frame, mask);
//        }
//
//        ++index;
//        std::cout << index << std::endl;
//    }
//}