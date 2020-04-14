#ifndef ASKR_AC_TREE_H 
#define ASKR_AC_TREE_H
#include<map>
#include<string>
namespace askr{
    class State{    // TODO 支持模板
        public:
            State(){};
            State(int _id,char _symbol=NULL,State *_parent=nullptr,bool _success=false,
            std::string _keyword="",State *_fail=nullptr):id(_id),symbol(_symbol),
            parent(_parent),success(_success),
            keyword(_keyword),fail(_fail){};
        public:
            int id;
            char symbol;
            std::map<std::string,State*> transitions();
            State *parent;
            bool success;
            std::string keyword;
            State *fail;
    };
    class KeywordTree{
        public:
            State *root_state= new State(0);
            int counter{1};
            bool finalized=false;
        void add(std::string keyword){
            if (this->finalized) return;     //TODO 增加错误机制
            if (keyword.size()==0) return;

            State *current_state=this->root_state;
            for (std::string::const_iterator ch=keyword.cbegin();ch!=keyword.cend();++ch){
                std::map<std::string,int>::iterator flag = current_state->transitions.find(*ch);
                if (flag!=current_state->transitions.end()){
                    current_state = current_state->transitions[*ch];
                }
                else{
                    current_state->transitions[*ch] = new State(this->counter,*ch,current_state);
                    current_state=current_state->transitions[*ch];
                    counter++;
                }
            }
            current_state->success=true;
            current_state->keyword=keyword;
        }

    }
}

#endif