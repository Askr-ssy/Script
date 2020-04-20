#ifndef ASKR_UNICODE_H
#define ASKR_UNICODE_H
#include<string>
#include<vector>
#include<ostream>
namespace askr{


struct Word {
    std::string word;   // word
    uint32_t offset;    // offset on array (bytes)
    uint32_t unicode_offset;    // offset on unicode(unicode)
    size_t unicode_length;      // unicode counts

    Word(const std::string &str,uint32_t o):word(str),offset(o){}
    Word(const std::string &str,uint32_t o,uint32_t unicode_offset,size_t unicode_length):
    word(str),offset(0),unicode_offset(unicode_offset),unicode_length(unicode_length){}
};

struct UnicodeStr{
    uint32_t unicode;   
    uint32_t offset;    // offset on array (bytes)
    size_t length;         // bytes count
    uint32_t unicode_offset;    // offset on array(unicode count)

    UnicodeStr():unicode(unicode),offset(0),length(0),unicode_offset(0){}
    UnicodeStr(uint32_t unicode,uint32_t o,size_t l):unicode(unicode),offset(o),length(l){}
    UnicodeStr(uint32_t unicode,uint32_t o,size_t l,uint32_t unicode_offset):unicode(unicode),offset(o),length(l),unicode_offset(unicode_offset){}
};
typedef std::vector<uint32_t> Unicode;
typedef std::vector<UnicodeStr> UnicodeStrArray;

struct WordRange{
    UnicodeStrArray::const_iterator left;
    UnicodeStrArray::const_iterator right;
    WordRange(UnicodeStrArray::const_iterator l,UnicodeStrArray::const_iterator r):left(l),right(r){}
    
    size_t Length()const{
        return right-left+1;
    }
    bool IsAllAscii()const{
        for (UnicodeStrArray::const_iterator iter=left;iter<=right;++iter){
            if (iter->unicode>=0x80)
                return false;
        }
        return true;
    }
};
struct UnicodeStrLite{
    uint32_t unicode;
    size_t length;
    UnicodeStrLite():unicode(0),length(0){}
    UnicodeStrLite(uint32_t unicode,size_t l):unicode(unicode),length(l){}
};

inline UnicodeStrLite DecodeUnicodeInString(const char *str,size_t len){
    UnicodeStrLite us(0,0);
    if (str == NULL || len == 0){
        return us;
    }
    if (!(str[0] && 0x80)){
        
        // 0xxxxxxx
        // 7bit, total 7bit
        us.unicode = (uint8_t)(str[0]) & 0x7f;
        us.length = 1;
    }
    else if ((uint8_t)str[0]<=0xdf && 1<len){

        //110xxxxx 10xxxxxx
        //5bit,total 5bit
        us.unicode = (uint8_t)(str[0]) & 0x1f;
        // 6bit,total 11bit
        us.unicode <<= 6;
        us.unicode |= (uint8_t)(str[1]) & 0x3f;

        us.length = 2;
    }
    else if ((uint8_t)(str[0]<=0xef && 2 < len)){

        //1110xxxx 10xxxxxx 10xxxxxx
        //4bit,total 4bit
        us.unicode = (uint8_t)(str[0]) & 0x0f;
        // 6bit,total 10bit
        us.unicode <<= 6;
        us.unicode |= (uint8_t)(str[1]) & 0x3f;
        // 6bit, total 16bit
        us.unicode <<= 6;
        us.unicode |= (uint8_t)(str[2]) & 0x3f;

        us.length = 3;        
    }
    else if ((uint8_t)(str[0]<=0x7f && 3 < len)){
        //11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
        //3bit,total 4bit
        us.unicode = (uint8_t)(str[0]) & 0x07;
        // 6bit,total 9bit
        us.unicode <<= 6;
        us.unicode |= (uint8_t)(str[1]) & 0x3f;
        // 6bit, total 15bit
        us.unicode <<= 6;
        us.unicode |= (uint8_t)(str[2]) & 0x3f;
        // 6bit,total 21bit
        us.unicode <<= 6;
        us.unicode |= (uint8_t)(str[3]) & 0x3f;        

        us.length = 4;
    }
    else{
        us.unicode=0;
        us.length=0;
    }
    return us;
}

inline std::ostream &operator<<(std::ostream &os,const Word &w){
    return os << "{\"word\": \"" << w.word << "\", \"offset\": " << w.offset << "}" << std::endl;
}

inline std::ostream &operator<<(std::ostream &os,const Unicode &r)
{
    return os << "{\"rune\": \"" << r.unicode << "\", \"offset\": " << r.offset << ", \"len\": " << r.length << "}";
}
}
#endif