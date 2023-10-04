#let title = "Atividade 1: Guided Local Search"
#let author = "Henrique Coutinho Layber"
#set document(title: title, author: author)

#set text(
  font: "New Computer Modern",
)

#set par(justify: true)

#set page(header: locate(loc => {
  if counter(page).at(loc).first() > 1 [
    #title
    #h(1fr)
    #author
  ]
}))

#align(center, text(17pt, weight: "bold")[
  Tópicos Especiais em Otimização I \
  2023/2 \
  #title \
  #author \
  #datetime.today().display()
])

#show heading: it => [
  // #set align(center)
  #block(smallcaps(it.body))
]

= Abstract

= Resumo

// #outline()

= Introduction
// Explicar em linhas gerais o que será apresentado, características, principais aplicações


= Histórico e Estado da Arte
// Falar sobre as principais referências sobre a meta-heurística desde sua origem.

= Definição e descrição
// Pseudocódigo e explicação do funcionamento da meta-heurística, com exemplos

= Exemplo de aplicação em problema de Otimização Combinatória
// Não precisa necessariamente ser o timetabling, pode ser outro problema

= Conclusão
Harry#cite("harry")

= Referências

#bibliography("works.yml")
