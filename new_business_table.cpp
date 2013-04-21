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

string business[50000];

int main()
{
	ifstream fin;
    fin.open("yelp_training_set/business_table.txt");
    
    string str;
    int k;
    while (fin>>str>>k)
    {
    	business[k] = str;
    }

    fin.close();

    ifstream fin2; 
    fin2.open("business_conversion_list.txt");
    int x, y;

    ofstream fout;
    fout.open("official_business_table.txt");
    while (fin2>>x>>y)
    {    		
    	fout<<y<<" "<<business[x]<<endl;
    }

    fout.close();
	return 0;
}