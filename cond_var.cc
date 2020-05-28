#include <iostream>
#include <thread>
#include <functional>
#include <mutex>
#include <condition_variable>
using namespace std::placeholders;
class Application
{
    std::mutex m_mutex;
    std::condition_variable m_condVar;
    bool m_bDataLoaded;
    public:
    Application()
    {
        m_bDataLoaded = false;
    }
    void loadData()
    {
        // Make This Thread sleep for 1 Second
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        std::cout<<std::this_thread::get_id() << "::" << "Loading Data from XML"<<std::endl;
        // Lock The Data structure
        std::lock_guard<std::mutex> guard(m_mutex);
        
        std::cout<<std::this_thread::get_id() << "::" <<"Loaded Data from XML"<<std::endl;
        // Set the flag to true, means data is loaded
        m_bDataLoaded = true;
        // Notify the condition variable
        m_condVar.notify_one();
    }
    bool isDataLoaded()
    {
        return m_bDataLoaded;
    }
    void mainTask()
    {
        PRINTF << "printing here" << std::endl;
        for (int i=0; i < 10; i++) {
            m_bDataLoaded = false;
            std::cout<<std::this_thread::get_id() << "::" <<"Do Some Handshaking"<<std::endl;
            // Acquire the lock

            std::unique_lock<std::mutex> mlock(m_mutex);
            // Start waiting for the Condition Variable to get signaled
            // Wait() will internally release the lock and make the thread to block
            // As soon as condition variable get signaled, resume the thread and
            // again acquire the lock. Then check if condition is met or not
            // If condition is met then continue else again go in wait.
            std::thread thread_2(&Application::loadData, this);
            thread_2.detach();
            m_condVar.wait(mlock, std::bind(&Application::isDataLoaded, this));

            std::cout<<std::this_thread::get_id() << "::" <<"Do Processing On loaded Data"<<std::endl;

        }
    }
};
int main()
{
    Application app;
    std::thread thread_1(&Application::mainTask, &app);
    thread_1.join();
    return 0;
}
