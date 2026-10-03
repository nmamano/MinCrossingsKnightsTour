// Independent row-level potential: implicit history product, no author code.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <cassert>
#include <cstdint>
using namespace std;
struct Row { int32_t u,v,W,W0,fu,eu,fd,ed,g,z; };
int main(){
 ifstream f("gap/verifier/claim27_rows.bin",ios::binary);
 uint32_t n,m; f.read((char*)&n,4); f.read((char*)&m,4);
 vector<Row> rows(m); f.read((char*)rows.data(),sizeof(Row)*m); assert(f.good());
 // State after previous row: history=(cand[-2],cand[-1],g[-2],g[-1]); counter 0..4.
 int dest[2][2][160],credit[2][2][160];
 for(int g=0;g<2;g++)for(int z=0;z<2;z++)for(int a=0;a<160;a++){
   int par=a/80,h=(a/5)%16,s=a%5;
   bool blocked=((h>>3)&1)&&g;
   int h2=((h&4)<<1)|((z&&((h>>1)&1))<<2)|((h&1)<<1)|g;
   dest[g][z][a]=(1-par)*80+h2*5+(blocked?min(4,s+1):0);
   credit[g][z][a]=blocked&&s==4;
 }
 for(int orientation=0;orientation<2;orientation++){
   vector<int> p(n*160,0); int pass;
   auto cost=[&](const Row&r,int a){
     int F=orientation?r.fd:r.fu,ex=orientation?r.ed:r.eu;
     int c=a<80?1:-1; int h=(((1+c)/2+c*(F+2))%3+3)%3;
     const int t[]={1,2,0};
     return 11*r.W+16*r.W0+44*credit[r.g==2][r.z==0][a]-32*(ex?2:t[h]);
   };
   for(pass=1;pass<1000;pass++){
     bool change=false;
     for(const auto&r:rows){
       int* from=&p[r.u*160]; int* to=&p[r.v*160];
       for(int a=0;a<160;a++){
         int b=dest[r.g==2][r.z==0][a],q=from[a]+cost(r,a);
         if(q<to[b]){to[b]=q;change=true;}
       }
     }
     if(!change)break;
   }
   assert(pass<1000);
   long long checked=0;int least=100000;
   for(const auto&r:rows)for(int a=0;a<160;a++){
      int b=dest[r.g==2][r.z==0][a];
      int slack=cost(r,a)+p[r.u*160+a]-p[r.v*160+b];
      assert(slack>=0);least=min(least,slack);checked++;
   }
   int low=*min_element(p.begin(),p.end()),high=*max_element(p.begin(),p.end());
   cout<<(orientation?"down":"up")<<" nodes "<<p.size()<<" checked arcs "<<checked<<" passes "<<pass<<" potential "<<low<<".."<<high<<" min_slack "<<least<<endl;
   assert(low==-596&&high==0);
   ofstream out(orientation?"gap/verifier/claim27_potential_down.bin":"gap/verifier/claim27_potential_up.bin",ios::binary);
   out.write((char*)p.data(),p.size()*sizeof(int));
 }
}
