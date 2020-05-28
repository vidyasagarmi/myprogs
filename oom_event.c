#include <sys/eventfd.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#define handle_error(msg) \
    do { perror(msg); exit(EXIT_FAILURE); } while (0)

#define MEM_FILE "/sys/fs/cgroup/memory/my.slice/memory.usage_in_bytes"
#define EVENT_FILE "/sys/fs/cgroup/memory/my.slice/cgroup.event_control"

int main()
{
    char cmd[2048];
    int efd, fd;
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <num>...\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    efd = eventfd(0, 0);
    if (efd == -1)
        handle_error("eventfd");
    fd = fopen(MEM_FILE, "r");
    if (fd == -1)
        handle_error("fopen fd");
    snprintf(cmd, 2048, "echo \"%d %d %lu\" > %s", efd,fd,EVENT_FILE);
    printf("%s\n", cmd);
    fclose(efd);
    fclose(fd);
}
