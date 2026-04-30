#pragma GCC optimize("O3,unroll-loops")
#include <bits/stdc++.h>
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
using namespace std;
#define ll long long
#define pii pair<ll,ll>
#define SZ(x) ((ll)(x).size())
#define ALL(x) (x).begin(),(x).end()
#define fo(i,n) for(ll i = 0 ; i < (n) ; i++)
#define foo(i,a,b) for(ll i = (a) ; i <= (b) ; i++)
#define F first
#define S second
#define pb push_back
ll t;
ll n,k;
vector<pii> a;
vector<ll> b,c;
bool check(ll x){
    fo(i,SZ(b)){
        b[i] = a[i].F + x * a[i].S;
    }

    sort(ALL(b));

    ll wins = 0;
    ll j = 0;

    fo(i,SZ(b)){
        if(j < SZ(c) && b[i] > c[j]){
            wins++;
            j++;
        }
    }
    return wins >= k;
}
void input(){
    cin >> t;
}
void solve(){
    cin >> n >> k;
    a.assign(n, {0, 0});
    b.resize(n);
    c.resize(n);
    fo(i,n) cin >> a[i].F >> a[i].S;
    fo(i,n) cin >> c[i];

    sort(ALL(c));

    ll l = 0 , r = 2e10;
    ll ans = r;
    while(l <= r){
        ll mid = (l + r) >> 1;
        if(check(mid)){
            ans = r;
            r = mid-1;
        }
        else{
            l = mid+1;
        }
    }
    cout << ((ans == 20000000000) ? -1 : ans) << '\n';
}
void output(){
    
}
int main(){
    ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
    input();
    while(t--){
        solve();
        output();
    }
    return 0;
}