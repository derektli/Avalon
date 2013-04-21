#include<iostream>
#include<fstream>
#include<map>
#include<string>
#include<cstdlib>
#include<cstdio>
#include<cstring>
#include<sstream>
#include<cmath>
using namespace std;

long long word[50000];
long long business[50000];
int count[200000];
int maxc = 0;

int numBusiness = 20000;

int word_conv[50000];
int business_conv[50000];

int numRow, numCol;
int matrix[1000][1720];

int main()
{

    // Obtained top 1k business with most words
    // Calculate words counts 
    cout<<"Reading list..."<<endl;

    ifstream finit;
    finit.open("yelp_training_set/business_to_word.txt");
    
    memset(word, 0, sizeof(word));
    memset(business, 0, sizeof(business));
    memset(word_conv, 0, sizeof(word_conv));
    memset(business_conv, 0, sizeof(business_conv));
    memset(matrix, 0, sizeof(matrix));
    numRow = 0;
    numCol = 0;
    int x,y;
    while (finit>>x>>y)
    {
        word[y]++;
        business[x]++;
        if (word[y]>maxc) maxc = word[y];
    }
    
    memset(count, 0, sizeof(count));
    for (int i=0;i<30000;i++)
    {
        count[word[i]]++;
    }
    
    finit.close();


    // Obtain top 1k business 
    cout<<"Obtaining 1k business list..."<<endl;
    for (int i=0; i<1000; i++)
    {
        int max = -1;
        int index = -1;
        for (int j=0; j<numBusiness; j++)
            if (business[j]>max)
            {
                max = business[j];
                index = j;
            }
        business[index] = -1;
    }

    numRow = 1000;

    // Outputing the 1k business list
    cout<<"Outputing the 1k business list..."<<endl;
    ofstream fout1000;    
    fout1000.open("business_conversion_list.txt");
    int bus_count = 1; 
    for (int i=0;i<numBusiness;i++)
    {
        if (business[i]==-1)
        {
            fout1000<<i<<" "<<bus_count<<endl;
            business_conv[i] = bus_count;
            bus_count++;
        }
    }

    fout1000.close();

    // Outputing the word list
    cout<<"Outputing the word list..."<<endl;
    ofstream foutword;
    foutword.open("word_conversion_list.txt");
    int word_count = 1;
    for (int i=0;i<49999;i++)
    {
        if (word[i]>1000)
        {
            foutword<<i<<" "<<word_count<<endl;
            word_conv[i] = word_count;
            word_count++;
            numCol++;
        }
    }

    foutword.close();

    // Generating a list with 1000 business and words with more than 100 counts
    cout<<"Generating the Business-Word matrix..."<<endl;

    ifstream fin;
    fin.open("yelp_training_set/business_to_word.txt");
    ofstream fout;
    fout.open("business_word_matrix.txt");
    
    map<string,int> mymap;
    while(fin>>x>>y)
    {
        if (word[y]>1000 && business[x]==-1)
        {
            string str;
            stringstream ss;
            ss<<business_conv[x]<<" "<<word_conv[y]<<" ";
            matrix[business_conv[x]-1][word_conv[y]-1]++;
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
        double temp = iter->second;
        temp = log(temp) + 0.5;
        fout<< iter->first << temp<<endl;
    }
    
    fin.close();
    fout.close();
    

    // Output official matrix
    cout<<"Outputing Official Matrix..."<<endl;
    cout<<numRow<<" "<<numCol<<endl;
    ofstream fmat;
    fmat.open("official_business_word_matrix.txt");

    for (int i=0;i<numRow;i++)
    {
        for (int j=0;j<numCol;j++)
        {
            if (j>0) fmat<<",";
            fmat<<matrix[i][j];            
        }
        fmat<<endl;
    }

    fmat.close();

    return 0;
}
