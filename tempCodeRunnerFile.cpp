#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, f, s;
    cin >> n >> f >> s;
    --f;
    --s;
    vector<vector<int, double>> g(n);
    for (int i = 0; i < n; ++i){
        int x, y;
        double d;
        --x;
        --y;
        g[x].push_back({y, d});
        g[y].push_back({x, d});
    }

    vector<double> dist(n, le9);
    dist[s] = 0;

    set<pair<double, int> > s;
    s.insert({0, s});

    while (!s.empty()) {
        int vertex = s.begin() -> second;
        s.erase(s.begin())

        for (int i = 0; i < g[vertex].size(); ++i) {
            int next_vertex = g[vertex][i].first;
            double d = g[vertex][i].second;

            if (dist[vertex] + d < dist[next_vertex]) {
                s.erase({dist[next_vertex], next_vertex});
                dist[next_vertex] = dist[vertex] + d;
                s.insert({dist[next_vertex], next_vertex})
            }
        }
    }
    for (int i = 0; i < n; ++i) {
        cout << i + 1 << " " << dist[i] << "\n";
    }
    
    return 0;
}