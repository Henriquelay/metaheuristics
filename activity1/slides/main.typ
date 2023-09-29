#import "@preview/polylux:0.3.1": *
#import themes.clean: *

#set text(font: "New Computer Modern")

#set footnote(
    numbering: it => []
)

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
    #only("2-")[\ O que isso significa? 
    #align(center)[#image("../assets/🤔❔.png", height: 35%)]]
]

#slide(title: [Local Search $dot$ Vizinhança])[
    Uma relação de vizinhança é uma relação geralmente simétrica entre os elementos do conjunto de soluções. É comum que essa relação seja definida em fator de uma nova função de #highlight[distância].
]

#slide[
    #align(center)[
        #image("../assets/neighborhood definition.png", height: 65%) #footnote[Fonte: K. Sylejmani et al, 2013 https://www.researchgate.net/figure/Sample-neighborhood-representation-in-local-search-techniques_fig2_305775960, data de acesso 2023-09-28]
    ]
]

#slide(title: "Passo-a-passo")[
    + Escolha uma solução inicial; #pause \ #uncover("4-")[`loop {`]
    + Defina vizinhos da solução atual e suas distâncias; #pause
    + Solução atual $<-$ melhor dos vizinhos; #pause \ #uncover("4-")[`}`]
    #pause
    ... Até que o critério de parada seja atingido.
]
#slide[
    #align(center)[
        #image("../assets/neighborhood traversal.png", height: 70%) #footnote[Fonte: S. Liu et al, 2019 https://www.mdpi.com/1996-1073/12/11/2189, data de acesso 2023-09-28]
    ]
]

#slide[
    #align(center)[
        #image("../assets/hill_climbing.png",
        alt: "Function graph describing local search's points of interest",
        height: 7.75cm,
        )]
    #footnote[Fonte: https://wikidocs.net/189098, data de acesso: 2023-09-28]
]

#new-section-slide[Guided Local Search]


#let guided_local_search_introduction = [
    O GLS é uma variação do Local Search que utiliza uma função de penalização para guiar a busca local. \
    Ao atravessar a vizinhança, o GLS penaliza soluções que estão longe de uma solução guia, e ao encontrar uma ótima local, o GLS atualiza a solução guia, e então torna a operar em uma função objetivo aumentada, desenhada para elevar o escopo da busca além da ótima local.
]

#slide(title: "Guided Local Search")[
    #guided_local_search_introduction
]

// GLS history
// Talk about GENET and such
// http://www.bracil.net/CSP/gls.html

#slide(title: [Retomando...])[#guided_local_search_introduction]

#slide[
    Para isso é necessário:
    - Uma função de custo $c_i$ para cada _feature_ $f_i$;
    - Cada _feature_ $f_i$ é associada a um valor penalidade $p_i$:
        - Inicia como $0$ e grava o número de occorências da _feature_ nas ótimas locais;
    - Função indicadora $I_i(s) = 1$ se a solução $s$ contém a _feature_ $f_i$, $0$ caso contrário;
]

#slide[
    $ g(s) = f(s) + lambda a sum_(1<=i<=m) I_i(s) p_i $
    / $g(s)$: Função de custo aumentada
    / $f(s)$: Função objetiva original
    / $I_i$: Função indicadora
    / $p_i$: Penalidade da _feature_ $f_i$
    / $lambda$: Parâmetro de intensidade da busca por soluções
    / $a$: Coeficiente para equilibrar a penalidade em relação à função objetiva
]
