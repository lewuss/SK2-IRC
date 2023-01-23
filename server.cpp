#include <iostream>
#include <string>
#include <cstring>
#include <cstdio>
#include <unistd.h>
#include <arpa/inet.h>
#include <cstdlib>
#include <string>
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
void delete_user(int clnt_sock);

void delete_user(int clnt_sock)
{
            for (int i = 0; i<channels.size();i++) //run through all the clients and delete the wanted one
            {
                for (int j=0; j<channels[i].size();j++)
                {
                    if (channels[i][j]==clnt_sock) channels[i].erase(channels[i].begin()+j); 
                }
            }
}
void *handle_clnt(void *arg) //main function that handles every client connection in a thread
{
    int clnt_sock = *((int *)arg);
    int str_len = 0;
    int quit = 0;
    char msg_with_cmd[BUF_SIZE];
    int active_channel = -1;
    int command;
    while ((str_len = read(clnt_sock, msg_with_cmd, sizeof(msg_with_cmd))) != 0) //listen to messages
    {
        string tmp(msg_with_cmd);
        command = stoi(string(1, msg_with_cmd[0])); //get command char from msg and change it to int
        string msg = tmp.substr(1); //get message with command char
        cout<<msg_with_cmd<<" "<<msg<<endl;
        switch (command)
        {
        case 1: //create a new room and add current client to it
        {
            delete_user(clnt_sock);
            vector<int>users;
            users.push_back(clnt_sock);
            channels.push_back(users);
            active_channel = atoi(&msg_with_cmd[1]);
            cout<<"created room"<<endl;
            break;

        }
        case 2: //leave other channels and join a new one
            delete_user(clnt_sock);
            active_channel = atoi(&msg_with_cmd[1]);
            channels[active_channel].push_back(clnt_sock);
            cout<<"added user "<<clnt_sock<<"to room "<<active_channel<<endl;
            break;
        case 3: //delete a channel
            for (int i = 0; i<channels[active_channel].size();i++)
                {
                    if (channels[active_channel][i]==clnt_sock) channels[active_channel].erase(channels[active_channel].begin()+i);

                }
            active_channel = -1;
            cout<<"room deleted";
            break;
        case 4: //send a message to a room user's currently in
            cout << "Client message: " << msg << " to "<< active_channel <<endl;         
            send_msg(msg, str_len, active_channel);
            break;
        case 5: //get info about all the connected clients to all rooms
        {
            string all_channels = "";
            for(int i = 0; i<channels.size();i++)
            {
                
                all_channels+=to_string(i);
                all_channels+=":";
                all_channels+=to_string(channels[i].size());
                all_channels+="/";
                
            }
            write(clnt_sock, all_channels.c_str(), all_channels.size());
            cout<<"sent";
            break;
        }
        case 6: //break out of the loop
            quit = 1;
        case 7: //handle direct messages
            msg = '9'+msg;
            for(int i =0; i<clnt_cnt;i++)
            {
                write(clnt_socks[i], msg.c_str(), msg.size());
            }
        default:
            break;
        }
        memset(msg_with_cmd, 0, 100); //clear the buffer
        if (quit) break;
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
    for (int i = 0; i<channels.size();i++)
            {
                for (int j=0; j<channels[i].size();j++)
                {
                    if (channels[i][j]==clnt_sock) channels[i].erase(channels[i].begin()+j); 
                }
            }
    clnt_cnt--;
    pthread_mutex_unlock(&mutx);
    close(clnt_sock);
    return NULL;
}

void send_msg(string msg, int len, int active_channel) //handle sending out messages
{
    msg = '9'+msg;
    pthread_mutex_lock(&mutx);
    for (int i = 0; i < channels[active_channel].size(); i++)
    {
        write(channels[active_channel][i], msg.c_str(), len);
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
        cout << "Connected client IP: " << inet_ntoa(clnt_addr.sin_addr) << " "<<clnt_sock<<endl;
    }
    close(serv_sock);

    return 0;
}


