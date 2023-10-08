#let title = "Atividade 1: Guided Local Search"
#let author = "Henrique Coutinho Layber"
#set document(title: title, author: author)

#set par(leading: 0.55em, first-line-indent: 1.8em, justify: true)
#set text(font: "New Computer Modern")
#show raw: set text(font: "New Computer Modern Mono")
#show par: set block(spacing: 0.55em)
#show heading: set block(above: 1.4em, below: 1em)

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

Guided Local Search (GLS) is a metaheuristic method that has been successfully applied to solve combinatorial optimization problems#cite("voudouris1999TSP"). It is a high-level strategy that applies an efficient penalty-based approach to interact with the local improvement procedure. This interaction creates a process capable of escaping from local optima, which improves the efficiency and robustness of the underlying local search algorithms#cite("handbook2018"). GLS builds up penalties during a search and uses penalties to help local search algorithms escape from local minima and plateaus. When the given local search algorithm settles in a local optimum, GLS modifies the objective function using a specific scheme. It is presented an overview of history and state of the art of GLS, definition and description, as well as a conclusion.

= Resumo

O _Guided Local Search_ (GLS) é um método metaheurístico que tem sido aplicado com sucesso para resolver problemas de otimização combinatória#cite("voudouris1999TSP"). É uma estratégia de alto nível que aplica uma abordagem eficiente baseada em penalidades para interagir com o procedimento de melhoria local. Essa interação cria um processo capaz de escapar de ótimos locais, o que melhora a eficiência e a robustez dos algoritmos de busca local subjacentes#cite("handbook2018"). O GLS acumula penalidades durante uma busca e usa essas penalidades para ajudar os algoritmos de busca local a escapar de mínimos locais e planaltos. Quando o algoritmo de busca local dado se estabiliza em um ótimo local, o GLS modifica a função objetivo usando um esquema específico. Em seguida, a busca local operará usando uma função objetivo aumentada, projetada para tirar a busca do ótimo local. O artigo visa fornecer uma visão geral do algoritmo GLS, incluindo sua definição e descrição, exemplos de aplicação em problemas combinatórios, bem como suas vantagens e eficiência em relação a outros algoritmos de busca local. É apresentado uma visão geral da história e estado da arte do GLS, definição e descrição, além de uma conclusão.

= Introdução
// Explicar em linhas gerais o que será apresentado, características, principais aplicações
O GLS é uma meta-heurística que se baseia em _Local Search_ (LS) e permite escapar de ótimos locais. O objetivo do GLS é encontrar soluções melhores do que as encontradas pelo LS. É uma técnica híbrida que combina a busca local com a busca global, em que é utilizada uma função de penalização para penalizar certos aspectos da solução atual que são considerados desfavoráveis. A busca local é realizada usando uma função objetivo que é piorada por essas penalidades (soma ou subtração, à depender se é um problema de maximização ou minimização), incentivando assim a busca por soluções melhores. Um exemplo de aplicação do GLS na otimização de rotas de veículos é o trabalho de Gonçalves et al.#cite("gonçalves2021"), que propõe indicadores de desempenho para o problema de roteirização de veículos com janelas de tempo. A abordagem proposta visa o desenvolvimento de um algoritmo baseado na metaheurística _GRASP_ conjugada com a técnica de intensificação de resultados _Path Relink_. Os resultados alcançados demonstram que o algoritmo proposto alcançou os resultados encontrados na literatura para 46,5% das instâncias executadas, indicando resultados promissores para um trabalho em desenvolvimento. Outro exemplo é o trabalho de Morais et al.#cite("morais2018"), que propõe uma abordagem para lidar com a geração de rotas multi-objetivo, considerando múltiplas métricas e estimativas de congestionamento de tráfego. Os experimentos incluem veículos que pretendem executar rotas com múltiplas paradas em redes rodoviárias de grande porte. Os dados do _OpenStreetMap_#footnote[https://www.openstreetmap.org/] foram usados para criar a rede rodoviária que contém todas as informações necessárias. Quatro cenários foram simulados com diferentes níveis de congestionamento de tráfego. Depois disso, os resultados obtidos foram comparados com as melhores soluções computadas pelo Algoritmo de Dijkstra. A abordagem proposta obteve bom desempenho computacional e demonstrou eficiência, oferecendo bons trade-offs, destacando os melhores resultados para cenários com maiores níveis de congestionamento de tráfego.

= Histórico
// Falar sobre as principais referências sobre a meta-heurística desde sua origem.

Em 1991, a empresa BRACIL #footnote[https://www.bracil.net/], mais especificamente sua divisão _Contraint Programming and Satisfaction Laboratory_ iniciou desenvolvimento de um novo algoritmo chamado GENET#cite("GENET") para solução de problemas binários, e ele foi expandido em 1992 para problemas não binários#cite("GENET_nb"). Eventualmente, Chris Voudouris em sua tese de pós doutorado generalizou o GENET para o que hoje conhecemos como _Guided Local Search_ (GLS)#cite("voudouris1997").

Tung Leng-Lau em 1999 extendeu o GLS como parte de um algoritmo genético, o _Guided Genetic Algorithm_ (GGA)#cite("leng1999"). Em 2002, Patrick Mills em sua tese de pós doutorado trabalhou na caracterização e extensão do algoritmo#cite("mills2002"), no algoritmo _Extended Guided Local Search_ (EGLS) que se inspira na função de aspiração do _Tabu Search_ para obter novos resultados e escapar de algumas dificuldades do GLS.

= Estado da Arte

Por volta da mesma época, o GLS já estava sendo aplicado em problemas famosos como o Problema do Caixeiro Viajante (TSP)#cite("voudouris1999TSP"), e mais recentemente é usado com sucesso como parte de meta-heurísticas híbridas: o GLS é utilizado em conjunto com outras técnicas, como redes neurais#cite("glsvrp2019"), algoritmos genéticos#cite("zachariadis2009"), e conhecimentos de domínio#cite("arnold2019knowledge"), para melhorar a eficiência e a eficácia da busca, com um sucesso mais impressionante no Problema de Roteamento de Veículos, nada um tomando sua forma especial: _Knowledge-Guided Local Search_#cite("arnold2019knowledge"), _Guided Fast Local Search_#cite("handbook2010"), _Extended Guided Local Search_#cite("mills2002")

= Definição e descrição
// Pseudocódigo e explicação do funcionamento da meta-heurística, com exemplos
// Detalhes do funcionamento da meta-heusrística

O GLS explora infomações relacionadas ao problema e a busca, para _guiar_ uma _Local Search_ (LS) em um espaço de busca. This se torna possível aumentando a função objetivo original para incluir termos de penalidade. A LS é afetada pelos termos de penalidade e confina a sua atenção em regiões promisoras do espaço de busca. Dessa forma, itera-se sobre o LS e a cada vez que o LS fica preso em uma ótima local, as penalidades são atualizadas e a LS é chamada novamente sobre a função aumentada usando as penalidades novas.

Modificações de penalidade "normalizam" as soluções geradas pelo LS, de acordo com informação anterior ou informação adquirida durante a busca. A ideia é usar informação anterior para ajudar-nos a resolver um problema aproximado. Informação anterior traduz-se para restrições que definem nosso problema, então reduzimos o número de soluções candidatas a serem considerados. O GLS também aproveita de informação aprendida durante a busca para impor restrições adicionais, que são usadas para evitar que o LS retorne a soluções já visitadas. O GLS então não altera o funcionamento do LS além da modificações da função objetivo. Então, para descrevermos o GLS de caso geral, o LS é considerado uma caixa preta, da seguinte forma:

#set par(first-line-indent: 0pt)
$ s_2 <- "procedure" "LocalSearch"(s_1, g) $
/ $s_1$: Solução inicial
/ $s_2$: Solução final
/ $g$: Função objetivo a ser maximizada/minimizada
#set par(first-line-indent: 1.8em)

== Propriedades da solução

Temos então o conceito de _propriedades da solução_, onde uma propriedade pode ser qualquer propriedade não-trivial da solução que satisfaz as restrições, ou seja, nem todas as soluções têm uma determinada propriedade. Propriedades de solução são específicos do problema em questão. Restrições em problemas são introduzidos ou reforçados com base na informação sobre o problema e o caminho do LS, então o custo das propriedades são representações de seus impactos diretos ou indiretos de suas propriedades correspondentes no custo da solução. 

Uma propriedade $f_i$ é representado por uma função indicadora $I_i$ da seguinte forma:


#set par(first-line-indent: 0pt)
$ I_i(s) = cases(
  1", se" s "tem a propriedade" i,
  0", caso contrário"
), s in S $
/ $S$: espaço de busca
/ $s$: solução
/ $i$: índice da propriedade
/ $I_i$: função indicadora da propriedade $f_i$
#set par(first-line-indent: 1.8em)

== Função aumentada de custo

Com isso, temos tudo que precisamos para definir a função aumentada de custo:

#set par(first-line-indent: 0pt)
$ h(s) = g(s) + lambda sum_{i=1}^M p_i I_i(s) $
/ $g$: Função objetivo original
/ $M$: Número de propriedades definidas sobre soluções
/ $p_i$: Penalidades correspondentes da propriedade $f_i$
/ $s$: Solução
/ $I_i$: Função indicadora da propriedade $f_i$
/ $lambda$: _Parâmetro de regularização_
/ $h$: Função aumentada de custo
#set par(first-line-indent: 1.8em)

O parâmetro de regularização $lambda$ representa a importância relativa das penalidades no que diz respeito ao custo da solução e é de grande significância pois provê uma medida de controlar a influência da informação no processo de busca.

GLS iterativamente usa a LS simplesmente modifica o vetor de penalidades $p$ dado por $p = (p_1, dots, p_M)$ cada vez que o LS fica preso em uma ótima local. Inicialmente, todos os parâmetros de penalidade se iniciam em $0$ (ou seja não há propriedades restringidas) e uma chamada é feita ao LS para encontrar uma ótima local da função de custo aumentada. Depois da primeira ótima local e toda ótima subsequente, o algoritmo toma a ação de modificar a função aumentada de custo e re-aplica o LS, iniciando da solução encontrada anteriormente. A ação de modificação é simplesmente incrementar o parâmetro das penalidades correspondentes à propriedades presentes na solução em $1$. O histórico anterior é gradualmente inserido na função aumentada de custo selecionando quais parâmetros de penalidade incrementar.


== Pseudocódigo

= Exemplo // de aplicação em problema de Otimização Combinatória
// Não precisa necessariamente ser o timetabling, pode ser outro problema

= Conclusão

#bibliography("works.yml", title: "Referências")
