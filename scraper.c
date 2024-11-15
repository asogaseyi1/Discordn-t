#include <stdio.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")  // Link with ws2_32.lib

int main(void) {
    WSADATA wsa;
    SOCKET s;
    struct sockaddr_in server;
    char server_reply[2000];

    printf("\nInitialising Winsock...");
    if (WSAStartup(MAKEWORD(2,2),&wsa) != 0) {
        printf("Failed. Error Code : %d",WSAGetLastError());
        return 1;
    }

    printf("Initialised.\n");

    // Create socket
    if((s = socket(AF_INET , SOCK_STREAM , 0 )) == INVALID_SOCKET) {
        printf("Could not create socket : %d" , WSAGetLastError());
    }

    printf("Socket created.\n");

    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 8080 );

    // Connect to remote server
    if (connect(s , (struct sockaddr *)&server , sizeof(server)) < 0) {
        printf("connect error");
        return 1;
    }

    printf("Connected\n");

    // Send data
    char *message = "GET /api/messages HTTP/1.1\r\nHost: localhost\r\n\r\n";
    if(send(s , message , strlen(message) , 0) < 0) {
        printf("Send failed");
        return 1;
    }
    printf("Data Sent\n");

    // Receive a reply from the server
    if(recv(s, server_reply, 2000, 0) < 0) {
        printf("recv failed");
    }

    printf("Reply received\n");
    printf("%s", server_reply);

    closesocket(s);
    WSACleanup();

    return 0;
}
