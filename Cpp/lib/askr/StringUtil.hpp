#ifndef ASKR_STRING_UTIL_H
#define ASKR_STRING_UTIL_H 1
#include<string>
#include<vector>
#include<algorithm>
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
                res.push_back(sub);
                return;
            }
            sub=str.substr(start,end-start);
            res.push_back(sub);
            start = end+1;
        }
        return;
    }

    inline std::vector<std::string> Split(const std::string &str,const std::string &pattern,size_t maxsplit = std::string::npos){
        std::vector<std::string> res;
        Split(str,res,pattern,maxsplit);
        return res;
    }
    inline std::string & LTrim(std::string &s,char x){
        s.erase(s.begin(),std::find_if(s.begin(),s.end(),[x](char ch){
            return ch != x;
        }));
        return s;
    }    
    inline std::string &RTrim(std::string &s,char x){
        s.erase(std::find_if(s.rbegin(),s.rend(),[x](char ch){
            return ch != x;
        }).base(),s.end());
        return s;        
    }
    inline std::string &Trim(std::string &s,char x){
        return RTrim(LTrim(s,x),x);
    } 
    inline bool IsSpace(unsigned c){
        // when passing large int as the argument of isspace, it core dump, so here need a type cast.
        return c > 0xff ? false : std::isspace(c & 0xff);
    }
    inline std::string & LTrim(std::string &s){
        s.erase(s.begin(),std::find_if(s.begin(),s.end(),[](char ch){
            return !IsSpace(ch);
        }));
        return s;
    }    
    inline std::string &RTrim(std::string &s){
        s.erase(std::find_if(s.rbegin(),s.rend(),[](char ch){
            return !IsSpace(ch);
        }).base(),s.end());
        return s;        
    }
    inline std::string &Trim(std::string &s){
        return RTrim(LTrim(s));
    }
}
#endif