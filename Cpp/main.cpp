// #include "AcTree.hpp"
#include<string>
#include<typeinfo>
#include<iostream>
#include"Unicode.hpp"
#include"AhoCorasick.hpp"
#include<map>
using namespace std;
int main(void){
    std::string str{"知"};
    std::map<uint32_t,double> m{{'知',1}};
    uint32_t unico = askr::DecodeUnicodeInString(str.c_str());
    askr::AhoCorasickTree actree;
    actree.add({1,2});
    actree.add({3,4,5});
    actree.finalize_fail();
    int result = actree.search_all({3,4,5,6,7});
    askr::DecodeUnicodeInString(str.c_str(),str.size());
    // askr::Word();
    m.find(str[0])==m.end();
    // for (std::string::iterator at=str.begin();at!=str.end();at++){
    //     cout<<typeid(str[0]).name()<<endl;
    //     std::cout<<typeid((*at)).name()<<" :"<<*at<<std::endl;
    // }
    // askr::KeywordTree act;
    // act.add("苹果");
    // act.add("香蕉");
    // act.add("波罗");
    // act.finalize_fail();


    // act.search_all("吃香蕉不吐菠萝皮");

    return 0;
}