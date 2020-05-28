unsigned long long int se_jiffies=0;
unsigned long long int jiffy_diff=0;
unsigned int last_jiffies=0;

int main() {
    while (1) {
        if (last_jiffies) {
            jiffy_diff = se_jiffies - last_jiffies;
            if (jiffy_diff >= 128) { /* 128 jiffies = 128 * 8 =  1024ms */
                printf("Timer stuck for more than 1024ms\n se_jiff: %llu, last_jiff: %u\n", se_jiffies, last_jiffies);
            } else if (jiffy_diff >= 42) { /* 42 jiffies = 42 * 8 =  336ms */
                printf("Timer stuck for more than 336ms\n");
            }
        }
        last_jiffies = se_jiffies++;
    }
}
