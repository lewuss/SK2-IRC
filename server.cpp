#include <iostream>
#include <string>
#include <cstring>
#include <cstdio>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <pthread.h>
#include <map>
#include <vector>

using namespace std;

const int BUF_SIZE = 100;
const int MAX_CLIENT = 5;
int clnt_socks[MAX_CLIENT];
int clnt_cnt = 0;
pthread_mutex_t mutx;
vector<vector<int>>channels;

void *handle_clnt(void *arg);
void send_msg(string msg, int len, int active_channel);
void *handle_clnt(void *arg)
{
    int clnt_sock = *((int *)arg);
    int str_len = 0;
    char msg_with_cmd[BUF_SIZE];
    int active_channel = -1;
    int command;
    while ((str_len = read(clnt_sock, msg_with_cmd, sizeof(msg_with_cmd))) != 0)
    {
        string tmp(msg_with_cmd);
        command = stoi(string(1, msg_with_cmd[0]));
        string msg = tmp.substr(1);
        switch (command)
        {
        case 1:
        {
            vector<int>users;
            users.push_back(clnt_sock);
            channels.push_back(users);
            cout<<"created room";
            break;

        }
        case 2:
            active_channel = msg[1]-'0'+48;
            channels[active_channel].push_back(clnt_sock);
            cout<<"added user to room"<<active_channel<<clnt_sock;
            break;
        case 3:
            for (int i = 0; i<channels[active_channel].size();i++)
                {
                    if (channels[active_channel][i]==clnt_sock) channels[active_channel].erase(channels[active_channel].begin()+i);

                }
            active_channel = -1;
            cout<<"room deleted";
            break;
        case 4:
            cout << "Client message: " << msg << " to "<< active_channel <<endl;         
            send_msg(msg, str_len, active_channel);
            break;
        default:
            break;
        }
    }

    // Remove disconnected client
    pthread_mutex_lock(&mutx);
    for (int i = 0; i < clnt_cnt; i++)
    {
        if (clnt_socks[i] == clnt_sock)
        {
            while (i++ < clnt_cnt - 1)
                clnt_socks[i] = clnt_socks[i + 1];
            break;
        }
    }
    clnt_cnt--;
    pthread_mutex_unlock(&mutx);
    close(clnt_sock);
    return NULL;
}

void send_msg(string msg, int len, int active_channel)
{
    pthread_mutex_lock(&mutx);
    for (int i = 0; i < channels[active_channel].size(); i++)
    {
        cout<<channels[active_channel][i]<< " "<< clnt_socks[i]<<" ";
        write(clnt_socks[i], msg.c_str(), len);
    }
    pthread_mutex_unlock(&mutx);
}

int main(int argc, char *argv[])
{
    // Create socket
    int serv_sock = socket(AF_INET, SOCK_STREAM, 0);

    // Bind socket to an IP address and port
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(1234);
    bind(serv_sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr));

    // Listen for incoming connections
    listen(serv_sock, 5);

    // Initialize mutex
    pthread_mutex_init(&mutx, NULL);

    // Accept incoming connections and create thread to handle each client
    while (1)
    {
        struct sockaddr_in clnt_addr;
        socklen_t clnt_addr_size = sizeof(clnt_addr);

        int clnt_sock = accept(serv_sock, (struct sockaddr *)&clnt_addr, &clnt_addr_size);
        pthread_mutex_lock(&mutx);
        clnt_socks[clnt_cnt++] = clnt_sock;
        pthread_mutex_unlock(&mutx);

        pthread_t t_id;
        pthread_create(&t_id, NULL, handle_clnt, (void *)&clnt_sock);
        pthread_detach(t_id);
        cout << "Connected client IP: " << inet_ntoa(clnt_addr.sin_addr) << endl;
    }

    // Close server socket
    close(serv_sock);

    return 0;
}


