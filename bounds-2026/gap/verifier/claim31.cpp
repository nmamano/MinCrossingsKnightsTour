// Independent fixed-beta R3 verifier, 2026-10-03.
// No producer code imports. Direct total crossing counts; row-first pending-edge
// order; all row-start states seeded; implicit endpoint product; no parent graph.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <chrono>
using namespace std;
using U=uint64_t;
struct Edge{int x,y,X,Y,c;};
struct Key{U mask,labels;bool operator==(const Key&k)const{return mask==k.mask&&labels==k.labels;}};
vector<Edge> slots; int sid[6][3][6][3];
vector<Key> nodes;vector<uint32_t> table,beginArc,dest;vector<uint16_t> costs;
U maskTable; const uint32_t NONE=UINT32_MAX;
bool slab(const Edge&e){return min(e.x,e.X)<2;}
bool allowed(int x,int z){int a=min(x,z),b=max(x,z);return (a==0&&(b==1||b==2))||(a==1&&(b==2||b==3))||(a==2&&b==3)||(a==3&&(b==4||b==5));}
int determinant(int ax,int ay,int bx,int by,int cx,int cy){return (bx-ax)*(cy-ay)-(by-ay)*(cx-ax);}
bool crosses(const Edge&a,const Edge&b){return determinant(a.x,a.y,a.X,a.Y,b.x,b.y)*determinant(a.x,a.y,a.X,a.Y,b.X,b.Y)<0&&determinant(b.x,b.y,b.X,b.Y,a.x,a.y)*determinant(b.x,b.y,b.X,b.Y,a.X,a.Y)<0;}
U hashkey(Key k){U z=k.mask+0x9e3779b97f4a7c15ULL;z^=k.labels*0xbf58476d1ce4e5b9ULL;z^=z>>30;z*=0xbf58476d1ce4e5b9ULL;z^=z>>27;z*=0x94d049bb133111ebULL;return z^(z>>31);}
void rehash(size_t size){table.assign(size,NONE);maskTable=size-1;for(uint32_t i=0;i<nodes.size();i++){U q=hashkey(nodes[i])&maskTable;while(table[q]!=NONE)q=(q+1)&maskTable;table[q]=i;}}
uint32_t intern(Key k){U q=hashkey(k)&maskTable;while(table[q]!=NONE){if(nodes[table[q]]==k)return table[q];q=(q+1)&maskTable;}uint32_t i=nodes.size();nodes.push_back(k);table[q]=i;if(nodes.size()*2>table.size())rehash(table.size()*2);return i;}
int phase(Key k){return k.mask>>56;}
void decode(Key k,vector<Edge>&v){v.clear();int j=0;U bits=k.mask&((1ULL<<56)-1);while(bits){int i=__builtin_ctzll(bits);bits&=bits-1;Edge e=slots[i];e.c=slab(e)?int((k.labels>>(4*j++))&15):-1;v.push_back(e);}assert(j<=16);}
int slotof(const Edge&e){assert(e.y>=-2&&e.y<=0&&e.Y>=0&&e.Y<=2);int i=sid[e.x][e.y+2][e.X][e.Y];assert(i>=0);return i;}
Key encode(int x,vector<Edge>&v){sort(v.begin(),v.end(),[](const Edge&a,const Edge&b){return slotof(a)<slotof(b);});Key k{U(x)<<56,0};int rename[101];fill(rename,rename+101,-1);int next=0,j=0;for(auto&e:v){int i=slotof(e);assert(!(k.mask>>i&1));k.mask|=1ULL<<i;if(slab(e)){assert(e.c>=0&&e.c<=100);if(rename[e.c]<0)rename[e.c]=next++;assert(next<=15&&j<16);k.labels|=U(rename[e.c])<<(4*j++);}}return k;}
struct Term{int x,y,X,Y,c;};
vector<Term> test;vector<int> forgotten;int exceptions[2];
Term normalize(Term e){if(e.y>e.Y){swap(e.x,e.X);swap(e.y,e.Y);}return e;}
int addtest(Term t){t=normalize(t);for(int i=0;i<(int)test.size();i++)if(test[i].x==t.x&&test[i].y==t.y&&test[i].X==t.X&&test[i].Y==t.Y){test[i].c+=t.c;return i;}test.push_back(t);return test.size()-1;}
int testmask(const vector<Edge>&v,int shift){int m=0;for(auto&e:v)for(int j=0;j<(int)test.size();j++){auto&t=test[j];if(e.x==t.x&&e.y+shift==t.y&&e.X==t.X&&e.Y+shift==t.Y)m|=1<<j;}return m;}
int main(){
 setvbuf(stdout,nullptr,_IONBF,0);auto start=chrono::steady_clock::now();auto seconds=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};
 fill(&sid[0][0][0][0],&sid[0][0][0][0]+6*3*6*3,-1);
 for(int y=-2;y<=0;y++)for(int x=0;x<6;x++)for(int Y=0;Y<=2;Y++)for(int X=0;X<6;X++)if(Y>y&&allowed(x,X)&&abs(X-x)+Y-y==3&&abs(X-x)>0&&abs(X-x)<=2&&Y-y<=2){sid[x][y+2][X][Y]=slots.size();slots.push_back({x,y,X,Y,-1});}
 assert(slots.size()==36);nodes.reserve(36000000);beginArc.reserve(36000001);dest.reserve(72000000);costs.reserve(72000000);rehash(1<<20);intern({0,0});beginArc.push_back(0);
 vector<Edge> pend,inc,rest,candidates,selected,next;vector<pair<uint32_t,uint16_t>> arcs;
 for(uint32_t u=0;u<nodes.size();u++){
  int x=phase(nodes[u]);decode(nodes[u],pend);inc.clear();rest.clear();
  for(auto&e:pend)(e.X==x&&e.Y==0?inc:rest).push_back(e);
  int label=100,merge=-1,nlab=0;for(auto&e:inc)if(slab(e)){if(nlab++==0)label=e.c;else merge=e.c;}
  arcs.clear();
  if(inc.size()<=2&&!(nlab==2&&label==merge)){
   candidates.clear();for(int dy=1;dy<=2;dy++)for(int X=0;X<6;X++)if(allowed(x,X)&&abs(X-x)+dy==3)candidates.push_back({x,0,X,dy,-1});
   for(unsigned bits=0;bits<(1u<<candidates.size());bits++){
    int degree=inc.size()+__builtin_popcount(bits);if(degree>2||((x==0||x==1||x==3)&&degree!=2))continue;
    selected.clear();for(int j=0;j<(int)candidates.size();j++)if(bits>>j&1)selected.push_back(candidates[j]);
    int load[6][3]={};bool good=true;for(auto&e:rest)load[e.X][e.Y]++;for(auto&e:selected)if(++load[e.X][e.Y]>2)good=false;if(!good)continue;
    int total=0,boundary=0;for(auto&e:selected)for(auto&f:rest)if(crosses(e,f)){total++;boundary+=(e.x==0||e.X==0)&&(f.x==0||f.X==0);}
    // New edges all share the current endpoint, hence cannot cross each other.
    next=rest;for(auto&e:next)if(slab(e)&&e.c==merge)e.c=label;
    for(auto e:selected){if(slab(e))e.c=label;next.push_back(e);}
    if(x==5)for(auto&e:next){e.y--;e.Y--;}
    uint32_t v=intern(encode((x+1)%6,next));assert(total<32&&boundary<=total);arcs.emplace_back(v,4*total+8*boundary);
   }
  }
  sort(arcs.begin(),arcs.end());for(size_t i=0;i<arcs.size();i++){if(i&&arcs[i].first==arcs[i-1].first){assert(arcs[i].second==arcs[i-1].second);continue;}dest.push_back(arcs[i].first);costs.push_back(arcs[i].second);}
  beginArc.push_back(dest.size());if(u&&u%4000000==0)printf("base processed %u discovered %zu arcs %zu seconds %.1f\n",u,nodes.size(),dest.size(),seconds());
 }
 printf("BASE states %zu arcs %zu seconds %.1f\n",nodes.size(),dest.size(),seconds());assert(nodes.size()==35372696&&dest.size()==71090636);vector<uint32_t>().swap(table);
 size_t NB=nodes.size();vector<uint8_t> ph(NB);for(size_t b=0;b<NB;b++)ph[b]=phase(nodes[b]);
 for(int orientation=0;orientation<2;orientation++){
  test.clear();forgotten.clear();int sign=orientation?-1:1;
  Term raw[]={{0,-1,1,1,-1},{0,0,1,-2,-1},{0,0,2,-1,-1},{0,1,1,-1,1},{0,1,2,0,1},{0,2,1,0,-1},{1,0,2,2,-1},{1,1,2,-1,-1}};
  for(auto e:raw){e.y*=sign;e.Y*=sign;addtest(e);}exceptions[0]=addtest({0,0,2,sign,0});exceptions[1]=addtest({0,sign,2,0,0});
  for(int i=0;i<(int)test.size();i++)if(test[i].Y==0)forgotten.push_back(i);assert(forgotten.size()<=4);
  int expand[16]={};for(int h=0;h<(1<<forgotten.size());h++)for(int j=0;j<(int)forgotten.size();j++)if(h>>j&1)expand[h]|=1<<forgotten[j];
  uint8_t penalty[1024][2];for(int m=0;m<(1<<test.size());m++)for(int p=0;p<2;p++){int F=0;for(int j=0;j<(int)test.size();j++)if(m>>j&1)F+=test[j].c;int c=1-2*p,h=(((1+c)/2+c*(F+2))%3+3)%3;penalty[m][p]=((m>>exceptions[0]&1)&&(m>>exceptions[1]&1))?2:array<int,3>{1,2,0}[h];}
  vector<uint8_t> lost(NB);vector<uint16_t> previous(NB);vector<uint32_t> reach(NB),offset(NB+1);
  for(size_t b=0;b<NB;b++)if(ph[b]==0){decode(nodes[b],pend);int bits=testmask(pend,0);for(int j=0;j<(int)forgotten.size();j++)if(bits>>forgotten[j]&1)lost[b]|=1<<j;previous[b]=testmask(pend,1);reach[b]=3;}
  auto successor=[&](uint32_t b,int v,uint32_t d){if(ph[b]==0)return int(lost[b])*2+(v&1);if(ph[b]==5)return (v&1)^1;return v;};
  for(int phase=0;phase<6;phase++)for(uint32_t b=0;b<NB;b++)if(ph[b]==phase)for(uint32_t i=beginArc[b];i<beginArc[b+1];i++)for(uint32_t bits=reach[b];bits;bits&=bits-1){int v=__builtin_ctz(bits);reach[dest[i]]|=1u<<successor(b,v,dest[i]);}
  uint64_t NA=0;for(size_t b=0;b<NB;b++){assert(reach[b]);offset[b+1]=offset[b]+__builtin_popcount(reach[b]);NA+=U(__builtin_popcount(reach[b]))*(beginArc[b+1]-beginArc[b]);}
  printf("%s AUGMENTED nodes %u arcs %llu seconds %.1f\n",orientation?"down":"up",offset[NB],(unsigned long long)NA,seconds());
  auto id=[&](uint32_t b,int v){assert(reach[b]>>v&1);return offset[b]+__builtin_popcount(reach[b]&((1u<<v)-1));};
  vector<int16_t> potential(offset[NB],0);int pass;
  for(pass=1;pass<200;pass++){
   bool change=false;for(uint32_t b=0;b<NB;b++)for(uint32_t bits=reach[b];bits;bits&=bits-1){int v=__builtin_ctz(bits),p=v&1;int from=potential[id(b,v)];for(uint32_t i=beginArc[b];i<beginArc[b+1];i++){
    uint32_t d=dest[i];int nv=successor(b,v,d);int w=costs[i];if(ph[b]==5)w-=12+4*penalty[expand[v>>1]|previous[d]][p];
    uint32_t to=id(d,nv);int value=from+w;if(value<potential[to]){assert(value>=-30000);potential[to]=value;change=true;}
   }}
   printf("%s pass %d changed %d seconds %.1f\n",orientation?"down":"up",pass,change,seconds());if(!change)break;
  }
  assert(pass<200);int low=0,high=-30000,rowlow=0,rowhigh=-30000,slack=100000;U checked=0,checksum=1469598103934665603ULL;
  for(uint32_t b=0;b<NB;b++)for(uint32_t bits=reach[b];bits;bits&=bits-1){int v=__builtin_ctz(bits),p=v&1;int value=potential[id(b,v)];low=min(low,value);high=max(high,value);if(ph[b]==0){rowlow=min(rowlow,value);rowhigh=max(rowhigh,value);}checksum=(checksum^uint16_t(value))*1099511628211ULL;
   for(uint32_t i=beginArc[b];i<beginArc[b+1];i++){uint32_t d=dest[i];int w=costs[i];if(ph[b]==5)w-=12+4*penalty[expand[v>>1]|previous[d]][p];int reduced=w+value-potential[id(d,successor(b,v,d))];assert(reduced>=0);slack=min(slack,reduced);checked++;}
  }
  assert(checked==NA&&rowlow==-104&&rowhigh==0);printf("%s PASS checked %llu potential %d..%d row %d..%d minimum_slack %d checksum %llu seconds %.1f\n",orientation?"down":"up",(unsigned long long)checked,low,high,rowlow,rowhigh,slack,(unsigned long long)checksum,seconds());
 }
}
