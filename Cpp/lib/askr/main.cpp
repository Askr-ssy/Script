// #include "AcTree.hpp"
#include<string>
#include<typeinfo>
#include<iostream>
#include<map>
using namespace std;
int main(void){
    std::string str{"知122344"};
    std::map<uint32_t,double> m{{'知',1}};
    m.find(str[0])==m.end();
    for (std::string::iterator at=str.begin();at!=str.end();at++){
        cout<<typeid(str[0]).name()<<endl;
        std::cout<<typeid((*at)).name()<<" :"<<*at<<std::endl;
    }
    // askr::KeywordTree act;
    // act.add("苹果");
    // act.add("香蕉");
    // act.add("波罗");
    // act.finalize_fail();


    // act.search_all("吃香蕉不吐菠萝皮");

    return 0;
}