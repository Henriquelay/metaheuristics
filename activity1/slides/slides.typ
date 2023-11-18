#import "@preview/polylux:0.3.1": *
#import themes.simple: *

#set text(font: "New Computer Modern")

// #set footnote(
//     numbering: it => []
// )

#show: simple-theme.with(
    footer: "Guided Local Search (GLS)",
)

#show link: underline

#let focus-slide = it => [
    #themes.clean.focus-slide[
        #align(center)[
            #it
        ]
    ]
] 

#title-slide[
    = Guided Local Search (GLS)
    == Tópicos Especiais em Otimização I
    2023/2

    Henrique Coutinho Layber
    \ \ \

    #image("../assets/lagostim.png", fit: "contain", width: 6em, alt: "Lagostim")
]

#slide[
    = Roteiro da apresentação

    + O que é Guided Local Search (GLS)?
    + Resumo do Local Search
    + Guided Local Search
        + História
        + Objetivo
        + Função objetivo aumentada
        + Pseudocódigo
]

#slide[
    == O que é Guided Local Search (GLS)?

    O GLS é uma simples variação do Local Search, então para entendermos o GLS, precisamos entender o Local Search.
]

#centered-slide[
    = Local Search
]

#slide[
    O Local Search é uma classe de algoritmos de 
    #alternatives-match((
        "1, 2": [busca local],
        "3-": highlight[busca local]
    )) que tentam encontrar uma solução ótima para um problema de otimização combinatória.
    #only("2-")[\O que isso significa? 
        #align(center)[
            #alternatives-match((
                "2": [#image("../assets/🤔❔.png", height: 9cm)],
                "3-": [#image("../assets/🧐.png", height: 9cm)],
            ))
        ]
    ]
]


#slide[
    #align(center)[
        #image("../assets/xadrez1passo.png", 
        alt: "Diagrama de um tabuleiro de xadrez demonstrando as posições vizinhas à atual, todas à um movimento de distância",
        height: 9cm) #footnote(numbering: it => [ ])[Fonte: OptaPlanner team, https://docs.optaplanner.org/6.0.0.CR5/optaplanner-docs/html/localSearch.html, data de acesso 2023-09-30]
    ]
]

#slide[
    #align(center)[
        #image("../assets/xadrez3passos.png",
        alt: "Diagrama de um tabuleiro de xadrez demonstrando três níveis de iterações de vizinhanças, cada uma à um movimento de distância",)
    ]
]

#slide[
    == Vizinhança

    Uma relação de vizinhança é uma relação geralmente simétrica entre os elementos do conjunto de soluções. É comum que essa relação seja definida em fator de uma nova função de *distância*.
]

#slide[
    #align(center)[
        #image("../assets/neighborhood definition.png", 
        alt: "Gráfico do espaço de busca demonstrando uma vizinhando como um conjunto definido pela distância",
        height: 9cm) #footnote(numbering: it => [ ])[Fonte: K. Sylejmani et al, 2013 https://www.researchgate.net/figure/Sample-neighborhood-representation-in-local-search-techniques_fig2_305775960, data de acesso 2023-09-28]
    ]
]

#slide[
    == Passo-a-passo (Linguagem natural)

    + Escolha uma solução inicial; #pause \ #uncover("4-")[`loop {`]
    + Defina vizinhos da solução atual e suas distâncias; #pause
    + Solução atual $<-$ melhor dos vizinhos; #pause \ #uncover("4-")[`}`]
    #pause
    ... Até que o critério de parada seja atingido.
]

#slide[
    #align(center)[
        #image("../assets/neighborhood traversal.png",
        alt: "Gráfico de conjunto de vizinhanças demonstrando a evolução das vizinhanças escolhidas pelo algoritmos Local Search em cada iteração",
        height: 9cm) #footnote(numbering: it => [ ])[Fonte: S. Liu et al, 2019 https://www.mdpi.com/1996-1073/12/11/2189, data de acesso 2023-09-28]
    ]
]

#slide[
    #align(center)[
        #image("../assets/hill_climbing.png",
        alt: "Gráfico de uma função com marcação e descrição dos pontos de interesse da busca local",
        height: 9cm,
        )]
    #footnote(numbering: it => [ ])[Fonte: https://wikidocs.net/189098, data de acesso: 2023-09-28]
]

#centered-slide[
    = Guided Local Search
]

#let guided_local_search_introduction = [
    O GLS é uma variação do Local Search que utiliza uma função de penalização para guiar a busca local. \
    Ao atravessar a vizinhança, o GLS penaliza que estão em uma ótima local já visitada, e atualiza a solução guia, e então torna a operar em uma função objetivo aumentada (ao invés da função objetivo original), desenhada para elevar dinâmicamente o escopo da busca além da ótima local.
]

#slide[
    #guided_local_search_introduction
]

#slide[
    #align(center)[
        #image("../assets/🛑.png")
    ]
]


#centered-slide[== História do Guided Local Search]

#slide[
    Mais um de uma série de metaheurísticas emergentes nos anos 90#footnote[https://acrogenesis.com/or-tools/documentation/user_manual/manual/metaheuristics/GLS.html], surgiu a partir do _GENET_, aplicado com sucesso no Problema do Caixeiro Viajante (TSP) (Voudouris & Tsang, 1999).
    #grid(
        columns: 3,
        image("../assets/ChrisVoudouris.jpg", height: 5cm, alt: "Chris Voudouris"),
        align(center + horizon)[&],
        image("../assets/EdwardCloseUp.jpg", height: 5cm, alt: "Edward Tsang")
    )

    Patrick Mills em 2002 extendeu o GLS e incluiu os parâmetros _randomness_ e _aspiration_, resultando no EGLS (Extended GLS). O EGLS é menos sensível ao parâmetro principal ($lambda$)
    #image("../assets/PatrickMills.jpg", height: 5cm, alt: "Patrick Mills")

    \

    Um caso de sucesso mais recente é o Knowledge-Guided Local Search, que se mostrou que eficientemente resolve o Problema de Roteamento de Veículos (VRP) (Arnold & Sörensen, 2017).
    #grid(
        columns: 3,
        image("../assets/FlorianArnold.jpg", height: 5cm, alt: "Florian Arnold"),
        align(center + horizon)[&],
        image("../assets/KennethSörensen.jpg", height: 5cm, alt: "Kenneth Sörensen")
    )

    \

    Existe uma página oficial#footnote[https://www.bracil.net/CSP/gls.html] e ela é maravilhosa!

    O GLS pode ser visto como uma especialização do Tabu Search, pois ambos criam a "função objetivo aumentada" a fim de evitar mínimos locais.

    Embora o comportamento dos Local Searches sejam muito similares aos algoritmos de Gradiente Descendente, eles não são a mesma coisa: o Gradiente Descendente depende do *gradiente* da função objetivo, enquanto o Local Search é uma explícita *exploração* do espaço de busca.
]

#slide[
    == Retomando...

    #guided_local_search_introduction
]

#centered-slide[== Função objetivo aumentada]

#slide[
    Para isso é necessário:
    - Cada _feature_ $f_i$ é associada a um valor penalidade $p_i$:
        - Inicia como $0$ e grava o número de occorências da _feature_ nas ótimas locais;
    - Função indicadora $I_i(s) = 1$ se a solução $s$ contém a _feature_ $f_i$, $0$ caso contrário;
    - Uma função de custo $c_i$ para cada _feature_ $f_i$ (padrão do Local Search);
]

#centered-slide[
    == Função de penalidade

    $ sum_(1<=i<=m) I_i(s) p_i $ 

    / $I_i$: Função indicadora 
    / $p_i$: Penalidade da _feature_ $f_i$
]

#slide[
    == Função objetivo aumentada

    $ g(s) = f(s) + lambda a sum_(1<=i<=m) I_i(s) p_i $
    / $I_i$: Função indicadora
    / $p_i$: Penalidade da _feature_ $f_i$ 
    / $f(s)$: Função objetiva original (específico do problema) 
    / $lambda$: Parâmetro de intensidade da busca por soluções 
    / $a$: Coeficiente para equilibrar a penalidade em relação à função objetiva (específico do problema) 
    / $g(s)$: Função de objetivo aumentada
]

#centered-slide[
    #alternatives[
        #image("../assets/função utilidade 1.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 2.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 3.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 4.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 5.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 6.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 7.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 8.png", fit: "contain", height: 11.5cm)
    ][
        #image("../assets/função utilidade 9.png", fit: "contain", height: 10.25cm)#footnote(numbering: it => [])[Fonte: https://www.youtube.com/watch?v=HVIrmDjJP68, data de acesso: 2023-10-03]
    ]
]

#slide[
    - Maior $lambda$ aumenta a intensidade da busca fora de ótimas locais;
    - $lambda$ muito grande pode levar a busca a ficar semelhante à uma busca aleatória;
    - $lambda$ muito pequeno pode levar a busca a ficar semelhante à uma busca local;
]

#slide[
    === Pseudocódigo
    ```python
    def GLS():
        current_s = initial_solution()
        best_s = current_s
        while not stop_condition():
            # Busca usando a função aumentada
            current_s = local_search(g, current_s)
            # Avalia a solução atual usando a função original
            if f(current_s) < f(best_s):
                best_s = current_s
            # Sempre atualiza a penalidade na função aumentada
            g = update_penalty(g, best_s)
        return best_s
    ```
]

// TODO exemplo com aplicação
#slide[
    = Referências


    #set text(size: 16pt)
    
    + Site oficial GLS: https://www.bracil.net/CSP/gls.html
    + C. Voudouris, E. Tsang, Guided Local Search and Its Application to the Traveling Salesman Problem, 1999
    + P. Mills, Extensions To Guided Local Search, 2002
    + A. Alsheddy, C. Voudouris, E. P. K. Tsang, A. Alhindi, Handbook of Heuristics, 2018
    + F. Arnold, K. Sörensen, Knowledge-Guided Local Search for the Vehicle Routing Problem, 2017
]

#focus-slide[
    Perguntas?
]
