// Independent cycle-preserving 2-opt search. No solver or construction imports.
#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <random>
#include <vector>
using namespace std;
int n,N; vector<int> p,pos; vector<vector<int>> nbr;
bool knight(int a,int b){int x=abs(a/n-b/n),y=abs(a%n-b%n);return x*y==2;}
int turn(int a,int b,int c){return a/n+c/n!=2*(b/n)||a%n+c%n!=2*(b%n);}
int at(int i){return p[(i+N)%N];}
int total(){int s=0;for(int i=0;i<N;i++)s+=turn(at(i-1),at(i),at(i+1));return s;}
int delta(int i,int j){
 int a=at(i),b=at(i+1),c=at(j),d=at(j+1);
 return turn(at(i-1),a,c)+turn(d,b,at(i+2))+turn(at(j-1),c,a)+turn(b,d,at(j+2))
 -turn(at(i-1),a,b)-turn(a,b,at(i+2))-turn(at(j-1),c,d)-turn(c,d,at(j+2));
}
bool candidate(int i,int j){return i<j && j>i+1 && !(i==0&&j==N-1) && knight(at(i),at(j))&&knight(at(i+1),at(j+1));}
void apply(int i,int j){reverse(p.begin()+i+1,p.begin()+j+1);for(int k=i+1;k<=j;k++)pos[p[k]]=k;}
void validate(){vector<int> seen(N);for(int i=0;i<N;i++){assert(p[i]>=0&&p[i]<N);seen[p[i]]++;assert(knight(at(i),at(i+1)));assert(pos[p[i]]==i);}for(int x:seen)assert(x==1);}
map<int,long long> census(){map<int,long long> h;for(int i=0;i<N;i++)for(int c:nbr[at(i)]){int j=pos[c];if(candidate(i,j))h[delta(i,j)]++;}return h;}
void save(string file){ofstream f(file);f<<n<<'\n';for(int a:p)f<<a<<' ';f<<'\n';}
int main(int argc,char**argv){
 if(argc<2)return 1;ifstream f(argv[1]);f>>n;N=n*n;p.resize(N);pos.resize(N);for(int i=0;i<N;i++){f>>p[i];pos[p[i]]=i;}
 nbr.resize(N);for(int a=0;a<N;a++)for(int dx:{-2,-1,1,2})for(int dy:{-2,-1,1,2})if(abs(dx*dy)==2){int x=a/n+dx,y=a%n+dy;if(x>=0&&x<n&&y>=0&&y<n)nbr[a].push_back(x*n+y);}
 validate();int base=total(),best=base;auto seed=p;cout<<"n "<<n<<" baseline "<<base<<" census";for(auto [d,c]:census())cout<<" "<<d<<":"<<c;cout<<endl;
 mt19937_64 rng(20261004+n);long long valid=0,accepted=0,zero=0;vector<int> corners;for(int a=0;a<N;a++)if(min(a/n,n-1-a/n)<24&&min(a%n,n-1-a%n)<24)corners.push_back(a);
 if(argc>2 && string(argv[2])=="pairs"){
 vector<pair<int,int>> moves;for(int i=0;i<N;i++)for(int c:nbr[at(i)]){int j=pos[c];if(candidate(i,j))moves.push_back({i,j});}
 long long pairs=0,neutralDistinct=0,improving=0;int bestDistinct=1000000;map<int,long long> hist;
 for(auto [i,j]:moves){int d=delta(i,j);apply(i,j);validate();assert(total()==base+d);
 for(int k=0;k<N;k++)for(int c:nbr[at(k)]){int l=pos[c];if(!candidate(k,l)||(k==i&&l==j))continue;
 int diff=d+delta(k,l);pairs++;hist[diff]++;bestDistinct=min(bestDistinct,diff);neutralDistinct+=diff==0;improving+=diff<0;
 if(diff<=0){apply(k,l);validate();assert(total()==base+diff);save(string(argv[1])+".pair_level_"+to_string(diff)+".txt");apply(k,l);}
 }
 apply(i,j);assert(p==seed);
 }
 cout<<"PAIRS "<<pairs<<" min_delta "<<bestDistinct<<" neutral_distinct "<<neutralDistinct<<" improving "<<improving<<" histogram";for(auto [d,c]:hist)cout<<" "<<d<<":"<<c;cout<<endl;return 0;
 }
 int runs=argc>2?atoi(argv[2]):12;int steps=argc>3?atoi(argv[3]):3000000;
 for(int run=0;run<runs;run++){
 p=seed;for(int i=0;i<N;i++)pos[p[i]]=i;int score=base,runbest=base;
 for(int s=0;s<steps;s++){
 int a=(rng()%10<9)?corners[rng()%corners.size()]:rng()%N;int c=nbr[a][rng()%nbr[a].size()];int i=pos[a],j=pos[c];if(i>j)swap(i,j);if(!candidate(i,j))continue;valid++;int d=delta(i,j);
 // Run zero is a pure neutral/downhill walk; other runs use annealing.
 double phase=double(s)/steps;double temp=run==0?0:(0.15+0.15*(run%4))*(1-phase);
 if(d<=0||(temp>0 && generate_canonical<double,53>(rng)<exp(-d/temp))){
 apply(i,j);score+=d;accepted++;zero+=d==0;runbest=min(runbest,score);
 if(score<best){best=score;validate();assert(total()==score);save("gap/verifier/turns_search_best"+to_string(n)+".txt");cout<<"IMPROVEMENT "<<n<<" "<<best<<" run "<<run<<" step "<<s<<endl;}
 }
 if(s%100000==0){validate();assert(total()==score);}
 }
 validate();assert(total()==score);cout<<"run "<<run<<" best "<<runbest<<" final "<<score<<endl;
 }
 cout<<"SUMMARY n "<<n<<" best "<<best<<" attempted "<<1LL*runs*steps<<" valid "<<valid<<" accepted "<<accepted<<" neutral "<<zero<<endl;
}
