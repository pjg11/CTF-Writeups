#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int generatePin() {
    
    srand(1893497025);
    return rand();
}

int main()
{
    printf("%d\n", generatePin());
    return 0;
}