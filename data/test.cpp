#include <stdio.h>

int map[100][100];
bool visited[100][100];
int Qx[1000];
int Qy[1000];

int findIsland(int m, int n)
{
    int count = 0;
    int st, en;
    st = en = 0;

    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (!visited[i][j])
            {
                visited[i][j] = true;
                if (map[i][j])
                {
                    Qx[en] = i;
                    Qy[en] = j;
                    en++;
                    count++;

                    while (st < en)
                    {
                        int ii = Qx[st];
                        int jj = Qy[st];
                        st++;

                        if (ii > 0 && !visited[ii-1][jj])
                        {
                            visited[ii-1][jj] = true;
                            if (map[ii-1][jj])
                            {
                                Qx[en] = ii - 1;
                                Qy[en] = jj;
                                en++;
                            }
                        }
                        if (jj > 0 && !visited[ii][jj-1])
                        {
                            visited[ii][jj-1] = true;
                            if (map[ii][jj-1])
                            {
                                Qx[en] = ii;
                                Qy[en] = jj - 1;
                                en++;
                            }
                        }
                        if (ii < m - 1 && !visited[ii+1][jj])
                        {
                            visited[ii+1][jj] = true;
                            if (map[ii+1][jj])
                            {
                                Qx[en] = ii + 1;
                                Qy[en] = jj;
                                en++;
                            }
                        }
                        if (jj < n - 1 && !visited[ii][jj+1])
                        {
                            visited[ii][jj+1] = true;
                            if (map[ii][jj+1])
                            {
                                Qx[en] = ii;
                                Qy[en] = jj +1;
                                en++;
                            }
                        }
                    }
                }
            }
        }
    }
    return count;
}

int main()
{
    FILE *fp = fopen("data.txt", "r");

    char ch;
    int m, n;
    m = n = 0;
    int j = 0;
    while (fscanf(fp, "%c", &ch) != EOF)
    {
        if (ch == '\n')
        {
            m++;
            n = j;
            j = 0;
            continue;
        }
        map[m][j++] = (ch == '1')?1:0;
    }

    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            visited[i][j] = false;

    int cnt = findIsland(m,n);
    printf("%d\n",cnt);

    return 0;
}
