// Create a C program that listens in a TCP port, receives one integer number from one TCP connection, replies with the double of that number and closes the connection.
// To compile use: gcc double_integer.c -o double
// Usage: ./double [port]
// Default port 2323
#include<stdio.h>
#include<stdlib.h> // atoi
#include<string.h>	//strlen
#include<sys/socket.h>
#include<arpa/inet.h> //inet_addr
#include<unistd.h>	//write
	
int main(int argc , char *argv[])
{
	int MAX_MESSAGE_SIZE = 10;	// Because of max size of ints (2^31)
	int main_socket;
	int port = 2323;
	int client_sock;
	int addr_length; 		
	int read_size;
	
	struct sockaddr_in server , client;

	char client_message[MAX_MESSAGE_SIZE];
	int client_number;

	// If there are some argument, use it as port
	if (argc > 1){
		port=atoi(argv[1]);
	}
	printf("Listening port %i\n", port);

	// Create socket
	main_socket = socket(AF_INET , SOCK_STREAM , 0);
	if (main_socket == -1){
		fprintf(stderr, "Error creating socket");	 
		return 1;
	}
	 
	// Server configuration
	server.sin_family = AF_INET;		
	server.sin_addr.s_addr = INADDR_ANY;		// Accept connections from every IP
	server.sin_port = htons( port );		// The htons() function makes sure that numbers are stored in memory in network byte order (Big endian)
	
	// Bind socket and server
	if( bind(main_socket,(struct sockaddr *)&server , sizeof(server)) < 0){
		fprintf(stderr, "Error binding");	  
		return 1;
	}
	 
	// Listen
	listen(main_socket, 10);
	
	// Accept and incoming connection
	addr_length = sizeof(struct sockaddr_in);
	client_sock = accept(main_socket, (struct sockaddr *)&client, (socklen_t*)&addr_length);
	if (client_sock < 0){
		fprintf(stderr, "Error while accepting connection");	 
		return 1;
	}
	 
	// Read message from client
	read_size = recv(client_sock , client_message , MAX_MESSAGE_SIZE , 0);
	if(read_size > 0){
		client_number=atoi(client_message);		// This value will be 0 if the user send non-digits characters 
	}else if(read_size == 0){
		fprintf(stderr, "Error, client sent no data");
		return 1;	 		 
	}else{	// read_size has negative value
		fprintf(stderr, "Error reading message from client");
		return 1;	 
	}


	// Reply to client with double of his number
	char double_char[MAX_MESSAGE_SIZE*2];
	snprintf(double_char, MAX_MESSAGE_SIZE*2,"%d",client_number*2);	// Converting from int to char
	write(client_sock , double_char , strlen(double_char));

	// Close the connection 
	if (close(client_sock) < 0){
		fprintf(stderr, "Error closing connection");	  
		return 1;
	}
	return 0;
}
