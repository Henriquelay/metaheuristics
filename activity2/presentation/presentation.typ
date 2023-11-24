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

    #image("../activity1/assets/lagostim.png", fit: "contain", width: 6em, alt: "Lagostim")
]

#slide[
    = Roteiro da apresentação

    + Detalhes de implementação
    + Experimentos (todo)
      + Calibração de parâmetros (todo)
      + Comparação com outras metaheurísticas (todo)
]


#centered-slide[
  #image("assets/screengrab0.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab1.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab2.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab3.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab4.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab5.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab6.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab7.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab8.png", fit: "contain", height: 15cm, width: 30cm)
]
#centered-slide[
  #image("assets/screengrab9.png", fit: "contain", height: 15cm, width: 30cm)
]

#focus-slide[
    Perguntas?
]
