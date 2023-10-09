#import "@preview/lovelace:0.1.0": * // For pseudocode
#show: setup-lovelace.with(line-number-supplement: "Linha")
#let pseudocode = pseudocode.with(indentation-guide-stroke: .5pt)

#let title = "Atividade 1: Guided Local Search"
#let author = "Henrique Coutinho Layber"
#set document(title: title, author: author)

#set par(leading: 0.55em, justify: true)
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

#set math.equation(numbering: "(1)", supplement: "Equação")

= Abstract

Guided Local Search (GLS) is a metaheuristic method that has been successfully applied to solve combinatorial optimization problems#cite("voudouris1999TSP"). It is a high-level strategy that applies an efficient penalty-based approach to interact with the local improvement procedure. This interaction creates a process capable of escaping from local optima and shoulders, which improves the efficiency and robustness of the underlying local search algorithms#cite("handbook2018"). GLS builds up penalties during a search and uses penalties to help local search algorithms escape from local minima and plateaus. When the given local search algorithm settles in a local optimum, GLS modifies the objective function using a specific scheme. It is presented an overview of history and state of the art of GLS, definition and description, as well as a conclusion, everything based on the work of Voudouris#cite("voudouris1997").

= Resumo

O _Guided Local Search_ (GLS) é um método meta-heurístico que tem sido aplicado com sucesso para resolver problemas de otimização combinatória#cite("voudouris1999TSP"). É uma estratégia de alto nível que aplica uma abordagem eficiente baseada em penalidades para interagir com o procedimento de melhoria local. Essa interação cria um processo capaz de escapar de ótimos locais, o que melhora a eficiência e a robustez dos algoritmos de busca local subjacentes#cite("handbook2018"). O GLS acumula penalidades durante uma busca e usa essas penalidades para ajudar os algoritmos de busca local a escapar de ótimos locais e planaltos. Quando o algoritmo de busca local dado se estabiliza em um ótimo local, o GLS modifica a função objetivo usando um esquema específico. O artigo visa fornecer uma visão geral do algoritmo GLS, incluindo sua definição e descrição, exemplos de aplicação em problemas combinatórios, bem como suas vantagens e eficiência em relação a outros algoritmos de busca local. É apresentado uma visão geral da história e estado da arte do GLS, definição e descrição, além de uma conclusão, tudo com base no trabalho de Voudouris#cite("voudouris1997").

= Introdução
// Explicar em linhas gerais o que será apresentado, características, principais aplicações
O GLS é uma meta-heurística que se baseia em _Local Search_ (LS) e permite escapar de ótimos locais. O objetivo do GLS é encontrar soluções melhores do que as encontradas pelo LS. É uma técnica híbrida que combina a busca local com a busca global, em que é utilizada uma função de penalização para penalizar certos aspectos da solução atual considerados desfavoráveis. A busca local é realizada utilizando uma função objetivo alternativa, piorada usando essas penalidades (acrescentada ou subtraída, a depender se é um problema de maximização ou minimização), incentivando assim a busca por soluções melhores. Um exemplo de aplicação do GLS na otimização de rotas de veículos é o trabalho de Gonçalves et al.#cite("gonçalves2021"), que propõe indicadores de desempenho para o problema de roteirização de veículos com janelas de tempo. A abordagem proposta visa o desenvolvimento de um algoritmo baseado em _GRASP_ conjugada com a técnica de intensificação de resultados _Path Relink_. Os resultados alcançados demonstram que o algoritmo proposto alcançou os resultados encontrados na literatura para 46,5% das instâncias executadas, indicando resultados promissores para um trabalho em desenvolvimento. Outro exemplo é o trabalho de Morais et al.#cite("morais2018") propõe uma abordagem para lidar com a geração de rotas multi-objetivo, considerando múltiplas métricas e estimativas de congestionamento de tráfego. Os experimentos incluem veículos que pretendem executar rotas com múltiplas paradas e os dados do _OpenStreetMap_#footnote[https://www.openstreetmap.org/] foram usados para criar a rede rodoviária que contém todas as informações necessárias. Quatro cenários foram simulados com diferentes níveis de congestionamento de tráfego. Depois disso, os resultados obtidos foram comparados com as melhores soluções computadas pelo Algoritmo de Dijkstra. A abordagem proposta obteve bom desempenho computacional e demonstrou eficiência, oferecendo boas trocas, destacando os melhores resultados para cenários com maiores níveis de congestionamento de tráfego.

= Histórico
// Falar sobre as principais referências sobre a meta-heurística desde sua origem.

Em 1991, a empresa BRACIL #footnote[https://www.bracil.net/], mais especificamente sua divisão _Contraint Programming and Satisfaction Laboratory_ iniciou desenvolvimento de um novo algoritmo chamado GENET#cite("GENET") para solução de problemas binários, e ele foi expandido em 1992 para problemas não binários#cite("GENET_nb"). Eventualmente, Chris Voudouris em sua tese de pós doutorado generalizou o GENET para o que hoje conhecemos como _Guided Local Search_ (GLS)#cite("voudouris1997").

Tung Leng-Lau em 1999 extendeu o GLS como parte de um algoritmo genético, o _Guided Genetic Algorithm_ (GGA)#cite("leng1999"). Em 2002, Patrick Mills em sua tese de pós doutorado trabalhou na caracterização e extensão do algoritmo#cite("mills2002"), no algoritmo _Extended Guided Local Search_ (EGLS) que se inspira na função de aspiração do _Tabu Search_ para obter novos resultados e escapar de algumas dificuldades do GLS.

= Estado da Arte

Por volta da mesma época, o GLS já estava sendo aplicado em problemas famosos como o Problema do Caixeiro Viajante (TSP)#cite("voudouris1999TSP"), e é usado mais recentemente com sucesso como parte de meta-heurísticas híbridas: o GLS é utilizado em conjunto com outras técnicas, como redes neurais#cite("glsvrp2019"), algoritmos genéticos#cite("zachariadis2009"), e conhecimentos de domínio#cite("arnold2019knowledge"), para melhorar a eficiência e a eficácia da busca, com um sucesso mais impressionante no Problema de Roteamento de Veículos, nada um tomando sua forma especial: _Knowledge-Guided Local Search_#cite("arnold2019knowledge"), _Guided Fast Local Search_#cite("handbook2010"), _Extended Guided Local Search_#cite("mills2002")

= Definição e descrição
// Pseudocódigo e explicação do funcionamento da meta-heurística, com exemplos
// Detalhes do funcionamento da meta-heusrística

O GLS explora informações relacionadas ao problema e a busca, para _guiar_ uma _Local Search_ (LS) em um espaço de busca. Isso se torna possível aumentando a função objetivo original para incluir termos de penalidade. A LS é afetada pelos termos de penalidade e confina a sua atenção em regiões promissoras do espaço de busca. Dessa forma, itera-se sobre o LS e a cada vez que o LS fica preso em uma ótima local, as penalidades são atualizadas e a LS é chamada novamente sobre a função aumentada usando as penalidades novas.

Modificações de penalidade normalizam as soluções geradas pelo LS, de acordo com informação anterior ou informação adquirida durante a busca. A ideia é usar informação anterior para ajudar-nos a resolver um problema aproximado. Informação anterior traduz-se para restrições que definem nosso problema, então reduzimos o número de soluções candidatas a serem considerados. O GLS também aproveita de informação aprendida durante a busca para impor restrições adicionais, para evitar que o LS retorne a soluções já visitadas. O GLS não altera o funcionamento do LS além das modificações da função objetivo. Então, para descrevermos o GLS de caso geral, o LS é considerado uma caixa preta, da seguinte forma:

#block(breakable: false)[
  $ s_2 <- "LocalSearch"(s_1, g) $
  / $g$: Função objetivo a ser maximizada/minimizada
]

== Propriedades da solução

Temos então o conceito de _propriedades da solução_, onde uma propriedade pode ser qualquer propriedade não-trivial da solução que satisfaz as restrições, ou seja, nem todas as soluções têm uma determinada propriedade. Propriedades de solução são específicos do problema em questão. Restrições em problemas são introduzidos ou reforçados com base na informação sobre o problema e o caminho do LS, então o custo das propriedades são representações de seus impactos diretos ou indiretos de suas propriedades correspondentes no custo da solução. Uma propriedade $i$ é representado por uma função indicadora $I_i$ da seguinte forma:

#block(breakable: false)[
  $ I_i(s) = cases(
    1", se" s "tem a propriedade" i,
    0", caso contrário"
  ), s in S $
  / $S$: espaço de busca
  / $s$: solução
  / $i$: índice da propriedade
  / $I_i$: função indicadora da propriedade $i$
]

== Função aumentada de custo

Com isso, temos tudo que precisamos para definir a função aumentada de custo:

$ h(s) = g(s) + lambda sum_{i=1}^M p_i I_i(s) $ <augmented>
/ $g$: Função objetivo original
/ $M$: Número de propriedades definidas sobre soluções
/ $p_i$: Penalidades correspondentes da propriedade $i$
/ $s$: Solução
/ $I_i$: Função indicadora da propriedade $i$
/ $lambda$: _Parâmetro de regularização_
/ $h$: Função aumentada de custo

O parâmetro de regularização $lambda$ representa a importância relativa das penalidades no que diz respeito ao custo da solução e é de grande significância, pois provê uma medida de controlar a influência da informação no processo de busca. GLS iterativamente usa a LS simplesmente modifica o vetor de penalidades $p$ dado por $p = (p_1, dots, p_M)$ cada vez que o LS fica preso em uma ótima local. \
Inicialmente, todos os parâmetros de penalidade se iniciam em $0$ (ou seja, não há propriedades restringidas) e uma chamada é feita ao LS para encontrar uma ótima local da função aumentada de custo. \
Depois da primeira ótima local e toda ótima subsequente, o algoritmo toma a ação de modificar a função aumentada de custo e re-aplica o LS, iniciando da solução encontrada anteriormente. A ação de modificação é simplesmente incrementar o parâmetro das penalidades correspondentes às propriedades presentes na solução em $1$. O histórico anterior é inserido na função aumentada de custo selecionando quais parâmetros de penalidade incrementar.

#let cost_set = math.bold("c")

As fontes de informações são os custos das propriedades e a própria ótima local. Assuma que cada propriedade $i$ definida sobre o conjunto de soluções $S$ é atribuído um custo $c_i$. Esse custo pode ser constante ou variável. Para simplificar a nossa análise, considere os custos constantes e dado pelo _vetor de custos_ #cost_set:

$ #cost_set = (c_1, dots, c_M)", " c_i in NN $

Uma solução ótima particular $s*$ exibe um número de propriedades. Indicadores $I_i$ das propriedades $i$ exibidas tomam o valor de $1$. Ou seja: para uma propriedade $i$ exibida por $s*$, $I_i(s*) = 1$.

== Modificações de penalidade

Em uma ótima local, os parâmetros de penalidade $p_i$ correspondentes às propriedades exibidas são incrementados em $1$ para todas as propriedades $i$ que maximizam a função utilitária:

$ "util"(s_*, i) = I_i(s_*) (c_i)/(1+p_i) $ <util>

Incrementar a penalidade $p_i$ é considerada uma _ação_ com valor de utilidade dado pela @util. Em uma ótima local apenas as ações com utilidade _máxima_ são selecionadas e então efetuadas, empregando o valor atual da penalidade como divisor para $p_i$ para que não seja totalmente enviesado para a penalização das propriedades de alto custo. Assim, se a propriedade foi penalizada múltiplas vezes, então o termo $c_i/(1+p)$ na @util diminui para essa propriedade, diversificando escolhas e dando oportunidades para que outras propriedades também sejam penalizadas, e que propriedades sejam penalizadas com frequência proporcional a seu custo.

== Parâmetro de regularização

Este parâmetro $lambda$ determina o grau em que as restrições irão afetar a LS. Um movimento altera a solução, adicionando novas propriedades e removendo propriedades existentes. No caso geral, a diferença $Delta h$ no valor da função aumentada é dada por:

$ Delta h = Delta g + lambda sum_(i=1)^M Delta I_i p_i $ <deltah>

@deltah mostra que se $lambda$ for grande, então os movimentos irão somente remove as propriedades da solução e as penalidades irão dominar o trajeto do LS. Isso introduz risco, pois as informações podem estar erradas. Por outro lado, se $lambda$ for pequeno, então os movimentos irão somente adicionar propriedades à solução e as informações de penalidade não terão efeito. Então, o parâmetro de regularização $lambda$ controla o grau em que as penalidades afetam o LS. O GLS é tolerante quanto a $lambda$, operando bem com uma variada gama de valores#cite("voudouris1997").

#block(breakable: false)[
== Pseudocódigo

  #algorithm(
    caption: [Guided Local Search],
    supplement: none,
    pseudocode(
      no-number,
      [*input:* $S$, $g$, $lambda$, $[I_1, dots, I_M]$, $[c_1, dots, c_M]$, M],
      no-number,
      [*output:* Uma solução razoavelmente boa para $g$],
      
      $k <- 0$,
      $s_0 <- "Solução aleatória ou heuristicamente gerada em" S$,

      [*for* $i <- 1$ até $M$ *do*], ind,
        [$p_i <- 0$ #comment[Inicia todas as penalidades em $0$]], ded,

      [*while* _CritérioDeParada_ *do*], ind,
        [$h <- g + lambda * sum I_i * p_i $ #comment[@augmented]],
        $s_(k+1) <- "LocalSearch"(s_k, h)$,

        [*for* $i <- 1$ até $M$ *do*], ind,
          [$"util"_i <- I_i(s_(s+1)) * c_i\/(1+p_i)$ #comment[@util]], ded,

        
        [*for each* $i$ que $"util"_i$ é máximo *do*], ind,
          $p_i <- p_i + 1$, ded,

        $k <- k+1$, ded,
      
      $s_* <- "Melhor solução em respeito à função de custo " g$,
      [*return*  $s_*$],
    )
  )
]
#block(breakable: false)[
  / $S$: Espaço de busca
  / $g$: Função objetivo original
  / $h$: Função aumentada de custo
  / $lambda$: Parâmetro de regularização
  / $M$: Número de propriedades definidas sobre soluções
  / $I_i$: Função indicadora da propriedade $i$
  / $c_i$: Custo da propriedade $i$
  / $p_i$: Penalidades correspondentes da propriedade $i$
]
= Exemplo // de aplicação em problema de Otimização Combinatória
// Não precisa necessariamente ser o timetabling, pode ser outro problema

== TSP

Examinaremos o problema do TSP simétrico. Ele é definido da por $N$ cidades e uma matriz simétrica de distâncias $D = [d_(i j)]$ que contém a a distância entre duas cidades $i$ e $j$. O objetivo é encontrar um _tour_ que visita cada cidade exatamente uma vez e retorna à cidade inicial, minimizando a distância total percorrida. Então o tour é uma permutação cíclica $pi$ de $N$ cidades se interpretamos $pi(i)$ sendo a cidade visitada após a cidade $i$, o custo do tour é dado por:

$ g(pi) = sum_(i=1)^N d_(i pi(i)) $ <TSP>

== Aplicação

Para aplicar o GLS ao TSP, precisamos definir as propriedades da solução. Um conjunto de propriedades facilmente definidos são os conjuntos de arestas não direcionados $EE = e_(i j) = (i = 1, dots N, j=i+1dots N, i != j)$. Como o problema é definido em torno de uma matriz de distâncias $D$, é útil definir nossas penalidades da mesma maneira $P = [p_(i j)]$. Então é preciso combinar a função objetivo do problema (@TSP) com as penalidades para formar a função aumentada de custo (@augmented), então usemos uma matrix auxiliar de distância que inclui as penalidades:

#block[
  $ D' = D + lambda P = [d_(i j) + lambda p_(i j)] $
  / $d_(i j)$: Distância entre as cidades $i$ e $j$
  / $D$: Matriz de distâncias original
  / $P$: Matriz de penalidades
  / $p_(i j)$: Penalidade da aresta $(i, j)$
  / $D'$: Matriz de distâncias auxiliar
  / $lambda$: Parâmetro de regularização
]

E o LS precisa usar $D'$ ao invés de $D$ na avaliação de movimentos. O GLS modifica $P$ e através disso também modifica $D'$, sempre que o LS atinge um ótimo local

Considerando um LS simples (2-Opt), uma solução vizinha é obtida através da solução atual removendo duas arestas, invertendo a ordem das arestas resultantes e reconectando o tour. Em termos práticos, isso significa inverter a ordem de cidades em uma seção contígua do vetor de distâncias. Se $e_1$ e $e_2$ são removidos e $e_3$ e $e_4$ são adicionados, cada um com distâncias $d_1$, $d_2$, $d_3$ e $d_4$, então a mudança do custo do movimento é dado por:

$ d_3 + d_4 - d_1 - d_2 $ <delta>

Como usamos as distâncias com penalidades, elas precisam necessariamente ser:

$ (d_3 + d_4 - d_1 - d_2) + lambda (p_3 + p_4 - p_1 - p_2) $

E quando o LS encontra esses ótimos locais, as arestas a serem penalizados são selecionados de acordo com a a função de utilidade (@util):

$ "util"("tour", e_(i j)) = I_e_(i j) ("tour") d_(i j)/(1 = p_(i j)) $

Onde

$ I_e_(i j) ("tour") = cases(
  1", se " e_(i j) in "tour",
  0", se " e_(i j) in.not "tour"
) $

O único parâmetro do GLS que precisa de refinamento é o $lambda$. Para muitos problemas, observa-se que bons valores para $lambda$ podem ser encontrados dividindo o valor da função objetivo de uma mínima local com o número de propriedades presentes nela. Nesses problemas, $lambda$ é dinâmicamente computado após a primeira mínima local. O usuário provê um parâmetro para $alpha$, que é relativamente independente da instância. Uma fórmula recomendada para $lambda$ é:

$ lambda = (alpha g(x_*)) / M $
/ $M$: Número de propriedades presentes em $x_*$

E para o TSP, valores de $alpha$ entre $1/8$ e $1/2$ são considerados bons para soluções de alta qualidade#cite("handbook2010").

= Conclusão

O GLS é algoritmo extremamente geral, versátil e útil. Se provou razoavelmente eficaz comparado à meta-heurísticas especializadas como o de Lin-Kernighan (LK) para o TSP. Inclusive em geral ele é mais rápido que o LK, se definido alguma quantia de tempo limite pequena. Também é muito fácil utilizá-lo com outras meta-heurísticas, pois não modifica o funcionamento interno do LS, apenas suas variáveis de entrada, como o _Fast Local Search_ (FLS), resultando no _Guided Fast Local Search_ (GFLS).

Podemos concluir com segurança que o GLS é uma meta-heurística muito poderosa, dada também sua facilidade de refinamento (apenas um parâmetro). 

// Conclua o texto


#bibliography("works.yml", title: "Referências")
