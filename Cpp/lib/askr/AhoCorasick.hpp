#ifndef ASKR_AC_TREE_H 
#define ASKR_AC_TREE_H
#include<map>
#include<string>
#include<set>
#include<list>
#include"Unicode.hpp"
namespace askr{
    class State{    // TODO 支持模板
        public:
            State(){};
            State(int _id,uint32_t _symbol=NULL,State *_parent=nullptr,bool _success=false,
            askr::Unicode keyword={},State *_fail=nullptr):id(_id),symbol(_symbol),
            parent(_parent),success(_success),
            keyword(keyword),fail(_fail){};
        public:
            int id;
            uint32_t symbol;    // unicode
            std::map<uint32_t,State*> transitions;
            State *parent;
            bool success;
            askr::Unicode keyword;
            State *fail;
    };
    class AhoCorasickTree{
        public:
            State *root_state= new State(0);
            int counter{1};
            bool finalized=false;
        void add(askr::Unicode keyword){
            if (this->finalized) return;     //TODO 增加错误机制
            if (keyword.size()==0) return;

            State *current_state=this->root_state;
            for (askr::Unicode::iterator ch = keyword.begin();ch!=keyword.end();++ch){
                std::map<uint32_t,State*>::iterator flag = current_state->transitions.find(*ch);
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

        void finalize_fail(){
            if (this->finalized)return;
            this->root_state->fail=this->root_state;
            this->search_fail_for_children(this->root_state);
            this->finalized=true;
        }

        size_t search_all(askr::Unicode str){
            if (!this->finalized) return -1;

            State * current_state = this->root_state;
            for(size_t idx=0;idx<str.size();++idx){
                if (current_state->transitions.find(str[idx])==current_state->transitions.end()){
                    if(this->root_state->transitions.find(str[idx])==this->root_state->transitions.end())
                        current_state=this->root_state;
                    else
                        current_state=this->root_state->transitions[str[idx]];
                }
                else
                    current_state=current_state->transitions[str[idx]];
                State * state=current_state;
                while(state!=this->root_state){
                    if(state->success){
                        askr::Unicode keyword = state->keyword;
                        return idx+1-keyword.size();
                    }
                    state=state->fail;
                }
            }
        }
        private:
        // 建立 单个节点的 fail指针
        void search_fail(State* state){
            if (state->fail)return;
    
            State *partent=state->parent;
            State *partent_fail = partent->fail;
            while (true){
                std::map<uint32_t,State *>::iterator flag = partent_fail->transitions.find(state->symbol);
                if (flag!=partent_fail->transitions.end() && partent_fail->transitions[state->symbol]!=state){
                    state->fail = partent_fail->transitions[state->symbol];
                    break;
                }
                else if (partent_fail == this->root_state){
                    state->fail = this->root_state;
                    break;
                }
                else
                    partent_fail = partent_fail->fail;
            }
            
            State *suffix = state->fail;
            if (suffix->fail ==nullptr)
                this->search_fail(suffix);
            
            for(std::map<uint32_t,State *>::iterator it=suffix->transitions.begin();it!=suffix->transitions.end();++it){
                if((state->transitions.find((*it).first)==state->transitions.end()) && suffix != this->root_state)
                    state->transitions[(*it).first]=(*it).second;
            }
        }

        void search_fail_for_children(State *state){
            std::set<int> processed;
            std::list<State*> to_process{this->root_state};
            while (true){
                if(to_process.empty())break;
                State * state = to_process.front();
                to_process.pop_front();
                processed.insert(state->id);
                for (std::map<uint32_t,State*>::iterator child = state->transitions.begin();child!=state->transitions.end();++child){
                    if(processed.count((*child).second->id)==0){
                        this->search_fail((*child).second);
                        to_process.push_back((*child).second);
                    }
                }
            }

        }        
    };
}
#endif