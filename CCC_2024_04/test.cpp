#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>
using namespace std;
ifstream f("citire.in");
ofstream g("iesire.out");

int a[200][200],aux[200][200];
struct pozitie{
    int lin,col;
};

pozitie dir[]={{1,0},{0,1},{-1,0},{0,-1}};
pozitie c[40001];

int n,m;
int xtree,ytree;

bool validate(int i, int j)
{
    if(i<1 || j<1 || i>n || j>m ) return false;
    if(i==xtree && j==ytree) return false;
    if(aux[i][j]!=0) return false;
    return true;
}
int main()
{
    int scenarii,xstart,ystart;
    f>>scenarii;
    int ok=1;
    char enter[1001];
    for(int integ=1;integ<=scenarii;integ++)
    {
        f>>m>>n;
        ok=1;
        char sir[1001],path[1001];
        f.getline(enter,1001);
        for(int i=1;i<=n;i++)
        {
            f.getline(sir,1001);
            for(int j=0;j<strlen(sir);j++)
                if(sir[j]=='.') a[i][j+1]=0;
                else if(sir[j]=='X')
                    a[i][j+1]=1, xtree=i, ytree=j+1;
        }

        f.getline(path,1001);
//        if(strlen(path)!=(n*m-2))
//        {
//            g<<"INVALID"<<"\n";
//            ok=0;
//            continue;
//        }
        int gasit=1;
        for(int i=1;i<=n&&gasit==1;i++)
            for(int j=1;j<=m;j++){

                if(i==xtree&&j==ytree) {
                    continue;
                }
                else
                {
                    for(int o=1;o<=n;o++)
                        for(int oo=1;oo<=m;oo++)
                            aux[o][oo]=a[o][oo];

                    xstart=i,ystart=j;
                    ok=1;
                    aux[xstart][ystart]=-1;
                    for(int ooo=0;ooo<strlen(path);ooo++)
                        if(path[ooo]=='S')
                        {
                            xstart++;
                            if(validate(xstart,ystart)== false)
                            {
                                //cout<<"INVALID"<<'\n';
                                ok=0;
                                break;
                            }
                            aux[xstart][ystart]=-1;
                        }
                       else if(path[ooo]=='W')
                        {
                           xstart--;
                            //aux[xstart][ystart]=-1;
                            if(validate(xstart,ystart)== false)
                            {
                                //cout<<"INVALID"<<'\n';
                                ok=0;
                                break;
                            }
                            aux[xstart][ystart]=-1;
                        }
                       else if(path[ooo]=='A')
                        {
                           ystart--;

                            if(validate(xstart,ystart)== false)
                            {
                                //cout<<"INVALID"<<'\n';
                                ok=0;
                                break;
                            }
                            aux[xstart][ystart]=-1;
                        }
                       else
                        {
                           ystart++;
                            if(validate(xstart,ystart)== false)
                            {
                                //cout<<"INVALID"<<'\n';
                                ok=0;
                                break;
                            }
                            aux[xstart][ystart]=-1;
                        }

                    if(ok==1){
                        gasit=0;
                        for(int pp=1;pp<=n&&gasit==0;pp++)
                            for(int ppp=1;ppp<=m;ppp++)
                                if(aux[pp][ppp]==0)
                                {
                                    gasit=1;
                                    break;
                                }

                        if (gasit == 0) {
                            // All cells are visited
                            g << "VALID" << '\n';
                        } else {
                            // Some cells are not visited
                            g << "INVALID" << '\n';
                        }


                    }
                }
            }

        if(gasit==1)
            g<<"INVALID"<<'\n';

    }
    return 0;
}