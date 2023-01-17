#include<vector>
#include<iostream>

using namespace std;

int main()
{
    vector<int> v;
    //Insert values 1 to 10
    v.push_back(20);
    v.push_back(10);
    v.push_back(30);
    v.push_back(20);
    v.push_back(40);
    v.push_back(50);
    v.push_back(20);
    v.push_back(10);
    for (int i = 0; i<v.size();i++)
            if (v[i]==50) v.erase(v.begin()+i);
    cout<<v.size();
    for(int i=0;i<v.size(); i++){
        cout << v[i] << " ";
    }
    return 0;
}