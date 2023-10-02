#import "@preview/polylux:0.3.1": *
#import themes.clean: *

#set text(font: "New Computer Modern")

// #set footnote(
//     numbering: it => []
// )

#show: clean-theme.with(
    logo: image("../assets/lagostim.png", fit: "contain", width: 6em, alt: "Lagostim"),
    footer: "Guided Local Search (GLS)",
    short-title: "Henrique Coutinho Layber",
)

#show link: underline

#let focus-slide = it => [
    #themes.clean.focus-slide[
        #align(center)[
            #it
        ]
    ]
] 

#title-slide(
    title: "Guided Local Search (GLS)",
    subtitle: "Tópicos Especiais em Otimização I",
    authors: "Henrique Coutinho Layber",
    date: "2023/2"
)

#slide(title: "O que é Guided Local Search (GLS)?")[
    O GLS é uma simples variação do Local Search, então para entendermos o GLS, precisamos entender o Local Search.
]

#new-section-slide("Local Search")

#slide(title: "Local Search")[
    O Local Search é uma classe de algoritmos de 
    #alternatives-match((
        "1, 2": [busca local],
        "3-": highlight[busca local]
    )) que tentam encontrar uma solução ótima para um problema de otimização combinatória.
    #only("2-")[\O que isso significa? 
        #align(center)[
            #alternatives-match((
                "2": [#image("../assets/🤔❔.png", height: 5.1cm)],
                "3-": [#image("../assets/🧐.png", height: 5.1cm)],
            ))
        ]
    ]
]


#slide[
    #align(center)[
        #image("../assets/xadrez1passo.png", height: 65%) #footnote(numbering: it => [])[Fonte: OptaPlanner team, https://docs.optaplanner.org/6.0.0.CR5/optaplanner-docs/html/localSearch.html, data de acesso 2023-09-30]
    ]
]

#slide[
    #align(center)[
        #image("../assets/xadrez3passos.png", height: 65%) #footnote(numbering: it => [])[Fonte: OptaPlanner team, https://docs.optaplanner.org/6.0.0.CR5/optaplanner-docs/html/localSearch.html, data de acesso 2023-09-30]
    ]
]

#slide(title: [Local Search $dot$ Vizinhança])[
    Uma relação de vizinhança é uma relação geralmente simétrica entre os elementos do conjunto de soluções. É comum que essa relação seja definida em fator de uma nova função de #highlight[distância].
]

#slide[
    #align(center)[
        #image("../assets/neighborhood definition.png", height: 65%) #footnote(numbering: it => [])[Fonte: K. Sylejmani et al, 2013 https://www.researchgate.net/figure/Sample-neighborhood-representation-in-local-search-techniques_fig2_305775960, data de acesso 2023-09-28]
    ]
]

#slide(title: "Passo-a-passo (Linguagem natural)")[
    + Escolha uma solução inicial; #pause \ #uncover("4-")[`loop {`]
    + Defina vizinhos da solução atual e suas distâncias; #pause
    + Solução atual $<-$ melhor dos vizinhos; #pause \ #uncover("4-")[`}`]
    #pause
    ... Até que o critério de parada seja atingido.
]

#slide[
    #align(center)[
        #image("../assets/neighborhood traversal.png", height: 70%) #footnote(numbering: it => [])[Fonte: S. Liu et al, 2019 https://www.mdpi.com/1996-1073/12/11/2189, data de acesso 2023-09-28]
    ]
]

#slide[
    #align(center)[
        #image("../assets/hill_climbing.png",
        alt: "Gráfica de uma função com descrição dos pontos de interesse da busca local",
        height: 7.75cm,
        )]
    #footnote(numbering: it => [])[Fonte: https://wikidocs.net/189098, data de acesso: 2023-09-28]
]

#new-section-slide[Guided Local Search]


#let guided_local_search_introduction = [
    O GLS é uma variação do Local Search que utiliza uma função de penalização para guiar a busca local. \
    Ao atravessar a vizinhança, o GLS penaliza soluções que estão longe de uma solução guia, e ao encontrar uma ótima local, o GLS atualiza a solução guia, e então torna a operar em uma função objetivo aumentada, desenhada para elevar o escopo da busca além da ótima local.
]

#slide(title: "Guided Local Search")[
    #guided_local_search_introduction
]

#slide[
    #align(center)[
        #image("../assets/🛑.png")
    ]
]


#new-section-slide[Histórico]

#slide(title: "História do Guided Local Search")[
    Mais um de uma séria de metaheurísticas emergentes nos anos 90#footnote[https://acrogenesis.com/or-tools/documentation/user_manual/manual/metaheuristics/GLS.html], aplicado com sucesso no Problema do Caixeiro Viajante (TSP) (Voudouris and Tsang, 1995). Recentemente, um caso de sucesso é o Knowledge-Guided Local Search, que se mostrou que eficientemente resolve o Problema de Roteamento de Veículos (VRP) (Arnold and Sörensen, 2019).
]

#slide(title: [Retomando...])[#guided_local_search_introduction]


// TODO Conclusão da história

#new-section-slide[Função aumentada de custo]

#slide[
    Para isso é necessário:
    // - Uma função de custo $c_i$ para cada _feature_ $f_i$;
    - Cada _feature_ $f_i$ é associada a um valor penalidade $p_i$: #pause
        - Inicia como $0$ e grava o número de occorências da _feature_ nas ótimas locais; #pause
    - Função indicadora $I_i(s) = 1$ se a solução $s$ contém a _feature_ $f_i$, $0$ caso contrário;
]

#slide(title: "Função de penalidade")[
    $ sum_(1<=i<=m) I_i(s) p_i $ #pause

    / $I_i$: Função indicadora #pause
    / $p_i$: Penalidade da _feature_ $f_i$
]

#slide[
    $ g(s) = f(s) + lambda a sum_(1<=i<=m) I_i(s) p_i $
    / $I_i$: Função indicadora
    / $p_i$: Penalidade da _feature_ $f_i$ #pause
    / $f(s)$: Função objetiva original (específico do problema) #pause
    / $lambda$: Parâmetro de intensidade da busca por soluções #pause
    / $a$: Coeficiente para equilibrar a penalidade em relação à função objetiva (específico do problema) #pause
    / $g(s)$: Função de objetivo aumentada
]

// TODO exemplo com aplicação

#slide[
    - Maior $lambda$ aumenta a intensidade da busca fora de ótimas locais;
    - $lambda$ muito grande pode levar a busca a ficar semelhante à uma busca aleatória;
    - $lambda$ muito pequeno pode levar a busca a ficar semelhante à uma busca local;
]
