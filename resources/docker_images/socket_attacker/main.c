#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>

#define LISTEN_PORT 8123
static const char reply[] = "HTTP/1.1 200 OK\r\n" \
			    "Content-type: text/html\r\n" \
			    "Connection: close\r\n" \
			    "\r\n" \
			    "<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">" \
			    "<html>" \
			    "<head><title>It works!</title></head>" \
			    "<body><h1>It works!</h1><p>This is only a test.</p></body>" \
			    "</html>\n";

#define BUFLEN 2048
static char recvbuf[BUFLEN];

int main(int argc __attribute__((unused)),
	 char *argv[] __attribute__((unused)))
{
    while(1) {
        int rc = 0;
        int srv, client;
        ssize_t n;
        struct sockaddr_in srv_addr;

        srv = socket(AF_INET, SOCK_STREAM, 0);
        if (srv < 0) {
            fprintf(stderr, "Failed to create socket: %d\n", errno);
            return rc;
        }

        srv_addr.sin_family = AF_INET;
        srv_addr.sin_addr.s_addr = INADDR_ANY;
        srv_addr.sin_port = htons(LISTEN_PORT);

        rc = bind(srv, (struct sockaddr *) &srv_addr, sizeof(srv_addr));
        if (rc < 0) {
            fprintf(stderr, "Failed to bind socket: %d\n", errno);
            return rc;
        }

        /* Accept one simultaneous connection */
        rc = listen(srv, 1);
        if (rc < 0) {
            fprintf(stderr, "Failed to listen on socket: %d\n", errno);
            return rc;
        }

        close(srv);
        printf("HERE\n");
	}
	return 0;
}