#include<iostream>
#include<fstream>
#include<map>
#include<string>
#include<cstdlib>
#include<cstdio>
#include<cstring>
#include<sstream>
using namespace std;

long long word[50000];
int count[200000];
int maxc = 0;
int main()
{
    memset(word, 0, sizeof(word));
    int x,y;
    while (cin>>x>>y)
    {
        word[y]++;
        if (word[y]>maxc) maxc = word[y];
    }
    
    memset(count, 0, sizeof(count));
    for (int i=0;i<30000;i++)
    {
        count[word[i]]++;
    }
    /*
    for (int i=0;i<30000; i++)
    {
        if (word[i]>100000)
            cout<<i<<" "<<word[i]<<endl;
    }
    
    int sum = 0;
    for (int i=1;i<=maxc;i++)
    {
       
        sum += count[i];
        
        //if (count[i]>0)
            //cout<<count[i]<<" words has "<<i<<" occurances"<<endl;
            //cout<<sum<<" words has <= "<< i <<" occurances"<<endl;
    }   
    */
    ifstream fin;
    fin.open("yelp_training_set/business_to_word.txt");
    ofstream fout;
    fout.open("business_word_matrix_100.txt");
    
    map<string,int> mymap;
    while(fin>>x>>y)
    {
        if (word[y]>100)
        {
            string str;
            stringstream ss;
            ss<<x<<" "<<y<<" ";
            str = ss.str();
            if (mymap.count(str)>0)
                mymap[str] +=1;
            else
                mymap[str] = 1;
        }
    }
    
    map<string, int>::iterator iter;
    
    for (iter = mymap.begin(); iter != mymap.end(); ++iter) 
    {
        fout<< iter->first << iter->second<<endl;
    }
    
    fin.close();
    fout.close();
    
    return 0;
}