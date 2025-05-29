# Site Map

```mermaid
graph LR;
    X[Login]-->A
    A[Main]-->B[Players];
        B-->F[Register Player];
        B-->G[Delete Player];
    A[Main]-->C[Boardgames];
        C-->H[Register Game];
        C-->I[Delete Game];
    A[Main]-->D[Season];
        D-->J[Register Season];
        D-->K[Delete Season];
    A[Main]-->E[Matches];
        E-->L[Register Match];
        E-->M[Delete Match];
```

```mermaid
graph LR;
    F[Profile];
```