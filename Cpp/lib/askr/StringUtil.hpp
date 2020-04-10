#ifndef ASKR_STRING_UTIL_H
#define ASKR_STRING_UTIL_H 1
#include<string>
#include<vector>
namespace askr{
    inline void Split(const std::string &str,std::vector<std::string> &res,const std::string &pattern,size_t maxsplit = std::string::npos){
        res.clear();
        size_t start=0;
        size_t end=0;
        std::string sub;
        while (start<str.size()){
            end=str.find_first_of(pattern,start);
            if (std::string::npos== end || res.size()>=maxsplit){
                sub = str.substr(start);
                res.push_back(str);
                return;
            }
            sub=str.substr(start,end-start);
            res.push_back(sub);
            start = end+1;
        }
        return;
    }

    inline std::vector<std::string> Split(const std::string &str,const std::string &pattern,size maxsplit = std::string::npos){
        std::vector<std::string> res;
        Split(str,res,pattern,maxsplit);
        return res;
    }

}
#endif