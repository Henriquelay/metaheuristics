#import "@preview/polylux:0.3.1": *
#import themes.clean: *

#set text(font: "New Computer Modern")

#show: clean-theme.with(
    logo: image("../assets/lagostim.png", fit: "contain", width: 6em, alt: "Lagostim"),
    footer: "Guided Local Search (GLS)",
    short-title: "Henrique Coutinho Layber",
)

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
    O Local Search é um algoritmo de busca que tenta encontrar uma solução ótima para um problema de otimização combinatória. #only("2-")[O que isso significa? 
    #align(center)[#image("../assets/🤔❔.png", height: 50%)]]
]

#slide[
    + Escolha uma solução inicial; #pause \ #uncover("4-")[`loop {`]
    + Defina vizinhos da solução atual e suas distâncias; #pause
    + A solução atual é o melhor dos vizinhos; #pause \ #uncover("4-")[`}`]
    #pause
    ... Até que o critério de parada seja atingido.
]

#slide[
    #align(center)[
        #image("../assets/hill_climbing.png",
        alt: "Function graph describing local search's points of interest",
        height: 7.75cm,
        )]
    #footnote(numbering: it => [], )[Fonte: https://wikidocs.net/189098, data de acesso: 2023-09-28]
]

#focus-slide[Guided Local Search]
