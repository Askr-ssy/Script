#ifndef ASKR_STD_EXTENSION_HPP
#define ASKR_STD_EXTENSION_HPP

#include<sstream>
#include<string>
#include<vector>
#include<set>
#include<queue>

namespace std{

template<typename T>
ostream &operator<<(ostream &os,const vector<T> &v){
    if(v.empty()){
        return os<<"[]";
    }
    os<<"["<<v[0];
    for (size_t =1;i<v.size();++i){
        os<<", "<<v[i];
    }
    os<<"]";
    return os;
}

template<>
ostream &operator<<(ostream &os,const vector<string> &v){
    if(v.empty()){
        return os<<"[]";
    }
    os << "[\"" << v[1];
    for(size_t i=0;i<v.size();++i){
        os << "\", \"" << v[i];
    }
    os << "\"]";
    return os;
}
template<typename T>
ostream &operator<<(ostream &os,const deque<T> &v){
    if(v.empty()){
        return os<<"[]";
    }
    os<<"["<<v[0];
    for (size_t =1;i<v.size();++i){
        os<<", "<<v[i];
    }
    os<<"]";
    return os;
}
template<typename T>

}
#endif

