#import "@preview/tablex:0.0.6": tablex, cellx, colspanx
#import "@preview/lovelace:0.1.0": * // For pseudocode
#show: setup-lovelace.with(line-number-supplement: "Linha")
#let pseudocode = pseudocode.with(indentation-guide-stroke: .5pt)

#let title = "Atividade 2: Guided Local Search"
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

#set math.equation(numbering: "(1)", supplement: "equação")

= Abstract

Guided Local Search (GLS) is a metaheuristic method that has been successfully applied to solve combinatorial optimization problems@voudouris1999TSP. It is a high-level strategy that applies an efficient penalty-based approach to interact with the local improvement procedure. This interaction creates a process capable of escaping from local optima and shoulders, which improves the efficiency and robustness of the underlying local search algorithms@handbook2018. GLS builds up penalties during a search and uses penalties to help local search algorithms escape from local minima and plateaus. When the given local search algorithm settles in a local optimum, GLS modifies the objective function using a specific scheme. It is presented details of an implementation made for solving the University Course Timetabling Problem, including solution representation, neighborhood and neighbor generation, technical details, parameter calibration and exhibit of results obtained by calibrating said parameters.

= Resumo

O _Guided Local Search_ (GLS) é um método meta-heurístico que tem sido aplicado com sucesso para resolver problemas de otimização combinatória@voudouris1999TSP. É uma estratégia de alto nível que aplica uma abordagem eficiente baseada em penalidades para interagir com o procedimento de melhoria local. Essa interação cria um processo capaz de escapar de ótimos locais, o que melhora a eficiência e a robustez dos algoritmos de busca local subjacentes@handbook2018. O GLS acumula penalidades durante uma busca e usa essas penalidades para ajudar os algoritmos de busca local a escapar de ótimos locais e planaltos. Quando o algoritmo de busca local dado se estabiliza em um ótimo local, o GLS modifica a função objetivo usando um esquema específico. O artigo visa fornecer uma visão geral do algoritmo GLS, incluindo sua definição e descrição, exemplos de aplicação em problemas combinatórios, bem como suas vantagens e eficiência em relação a outros algoritmos de busca local. É apresentado detalhes de implementação feita para resolver o Problema de Alocação de Horários de Universidades, incluindo representação de solução, vizinhança e geração de vizinhos, detalhes técnicos, calibração de parâmetros e exibição de resultados obtidos pela calibração dos referidos parâmetros.

= Introdução
// Explicar em linhas gerais o que será apresentado, características, principais aplicações

O _Guided Local Search_ (GLS) funciona por vias da implementação de contadores de penalidades, um para cada _feature_, onde a cada execução do Local Search (LS), as _features_ encontradas nessa ótima local que respeitam uma função utilidade recebem um incremento. O contador começa em zero e nunca é reiniciado até o término do programa. Isso evita que o LS tenda a ir sempre para as soluções que minimizem as mesmas _features_, em especial aqueles em sua imediata vizinhança, variando assim o espaço de soluções explorado.

== Descrição do método meta-heurístico

O GLS é definido de maneira formal de acordo com a @augmented abaixo:

#block(breakable: false)[
  $ h(s) = g(s) + lambda sum_{i=1}^M p_i I_i(s) $ <augmented>
  / $g$: Função objetivo original
  / $M$: Número de propriedades definidas sobre soluções
  / $p_i$: Penalidades correspondentes da propriedade $i$
  / $s$: Solução
  / $I_i$: Função indicadora da propriedade $i$
  / $lambda$: _Parâmetro de regularização_
  / $h$: Função aumentada de custo
]

$I_i(s)$ sendo definido pela @selector-function abaixo:

#block(breakable: false)[
  $ I_i(s) = cases(
    1", se" s "tem a propriedade" i,
    0", caso contrário"
  ), s in S $ <selector-function>
  / $S$: espaço de busca
  / $s$: solução
  / $i$: índice da propriedade
  / $I_i$: função indicadora da propriedade $i$
]

Ou seja, é sempre um acréscimo (para o caso de problemas de minimização) ao resultado da função original. $I_(i\(s\))$ pode ser informalmente descrito como uma função *seletora*, ou seja, ela retorna 1 se a solução $s$ tem a propriedade $i$, e 0 caso contrário. $p_i$ é o valor da penalidade para a propriedade atual $i$, ou seja, $p_i I_(i\(s\))$ em @augmented é igual ao contador atual de penalidades da _feature_ $i$, se presente na solução $s$.

É importante ressaltar que somente as penalidades que maximizam o valor de @util são incrementadas, ou seja, para uma iteração de LS, somente as _features_ que maximizam @util em relação às outras _feature_ dessa mesma solução encotrada nessa iteração são incrementadas.
$ "util"(s_*, i) = I_i(s_*) (c_i)/(1+p_i) $ <util>

Note o divisor $1+p_i$. Com $p_i$ na posição de divisor, fazemos com que o GLS evite penalizar sempre as mesmas _features_, que mesmo em um determinado período sejam caras, podem se provarem competitivas em iterações posteriores.

= Implementação
// Explicar como foi implementado, detalhes técnicos

O código é aberto pode ser acessado no GitHub, disponível em https://github.com/Henriquelay/metaheuristics e no SourceHut, disponível em https://git.sr.ht/~damnorangecat/metaheuristics.

== Representação de solução
// Explicar como foi representado o problema, como foi feita a codificação das soluções e a manipulação de grafo e tabela-horário

A identificação dos nós é fundamental para definir a representação da solução. Havia o desejo também fazer alguma representação (razoavelmente) fidedigna de todo o espaço de soluções, ou seja, mesmo que uma _feature_ ocorrente torne uma solução inviável, foi querida possível sua representação.

Foi identificado o limite físico do problema, que consiste em que cada *horário* (espaço de tempo em que se aloca um aula) devem estar disponíveis todas as salas para serem possíveis de representar soluções nelas. Logo, foi definido que o uma cor de nossos nós seriam uma tripla composta de sala, dia e período, `room-day-period`. Os outros nós seriam os cursos que devem estar disponíveis sua representação nessas triplas.

A representação da solução foi feita da forma de uma matriz de ajacências, onde as linhas da matriz são as triplas, e as colunas são os cursos. O valor armazenado é um número inteiro, representando a quantidade de aulas do determinado curso naquela tripla.

Exemplo:

Segundo a @example-triplet:

#figure(supplement: [tabela], caption: [Exemplo de uma solução])[
  #table(
    columns: 5,
    align: center + horizon,

    [], [*$"C1"$*], [*$"C2"$*], [*$"C3"$*], [*$"C4"$*],
    [*$"S1-D1-P1"$*], [$1$], [$0$], [$1$], [$0$],
    [*$"S1-D1-P2"$*], [$0$], [$2$], [$0$], [$0$],
    [*$"S1-D2-P1"$*], [$0$], [$0$], [$0$], [$1$],
    [*$"S1-D2-P2"$*], [$0$], [$1$], [$0$], [$0$],
    [*$"S2-D1-P1"$*], [$0$], [$1$], [$0$], [$0$],
    [*$"S2-D1-P2"$*], [$0$], [$2$], [$1$], [$0$],
    [*$"S2-D2-P1"$*], [$2$], [$0$], [$1$], [$0$],
    [*$"S2-D2-P2"$*], [$0$], [$0$], [$0$], [$0$],
  )
] <example-triplet>

Temos um problema com 2 dias, 2 períodos em cada dia, 2 salas _S1_ e _S2_, e 4 cursos _C1_, _C2_, _C3_ e _C4_. A solução apresentada é a seguinte:
- Uma unidade de aula do curso _C1_ e uma de _C3_ na sala _S1_ no dia 1 e período 1;
- Duas unidades de aula do curso _C2_ na sala _S1_ no dia 1 e período 2;
- Uma unidade de aula do curso _C4_ na sala _S1_ no dia 2 e período 1;
- Uma unidade de aula do curso _C2_ na sala _S1_ no dia 2 e período 2;
- Uma unidade de aula do curso _C2_ na sala _S2_ no dia 1 e período 2;
- Duas unidades de aula do curso _C1_ na sala _S2_ no dia 2 e período 1;
- Uma unidade de aula do curso _C3_ na sala _S2_ no dia 2 e período 2;

Podemos ver claramente que a solução é inviável segundo as regras determinadas em @kampke2020.

== Solução Inicial
// Explicar como foi feita a geração da solução inicial, quais foram as estratégias utilizadas

Para gerar uma solução inicial, como os algoritmos de busca local não definem, foi implementado uma função de geração de valor inicial pseudo-aleatória, que evita somente as soluções inviáveis mais óbvias, como por exemplo _H1_@kampke2020#footnote[_H1-Aulas: Todas as aulas de uma disciplina devem ser alocadas, e em períodos
diferentes. Uma violação ocorre se uma aula não é alocada, ou se duas aulas da
mesma disciplina são alocadas no mesmo período._]. Isso gera soluções relativamente bem ruins, onde é um desafio sequer achar soluções viáveis dentro do tempo estabelecido.

== Vizinhança e geração de vizinhos
// Explicar como foi feita a geração de vizinhos, quais foram as estratégias utilizadas

A vizinhança de uma solução foi definida como sendo qualquer solução que seja possível chegar a ela através de um único movimento. O movimento de escolha foi o _Lecture Move_, que é um bom movimento de geração de vizinhos@müller2009@kampke2020.

Cada solução tem muitos e muitos vizinhos, a depender pelo tamanho do problema. Então uma técnica foi implementada de limitar a busca aos primeiros `n` aleatórios vizinhos, então escolher o melhor deles, ou seja, uma versão limitada do _steepest descent_. Isso não é muito impactante ao comparar os resultados, pois o LS também é afetado pelo mesmo parâmetro@mills2002.

== Detalhes técnicos
// Versão da linguagem, compilador, configurações da máquina, tempo resultado no benchmark

A linguagem escolhida de implementação foi Python, e foi usada a versão `3.12.0a2`. Como ferramenta de gerência de dependências, foi usado o Poetry versão `1.7.1`.

O código foi escrito de uma forma a não usar de paralelismo algum, há somente um thread e um processo. Múltiplos processos foram usados para acelerar a geração de resultados, mas em instâncias separadas de execução (começando em valores iniciais diferentes).

A configuração da máquina usada para os testes foi um AMD Ryzen 7600X com 326GB de RAM DDR5, no sistema operacional Arch Linux. O resultado do `benchmark_my_linux_machine` responde que devo rodar o algoritmo por $72$ segundos.

Por questões de limitação de tempo, a função de utilidade não foi implementada, e todos os parâmetros encontrados ao final do LS sofrem penalidade.

= Calibração de parâmetros
// Explicar como foi feita a calibração dos parâmetros, quais foram os parâmetros calibrados, e o que resulta desses parâmetros

O parâmetros $lambda$ foi calibrado a partir de $0.5$, valor que os autores originais encontaram bom para o TSP@voudouris1999TSP. Daí, implementa-se uma técnica de busca binária, analisando o incremento e o decremento do valor, e observando os resultados médios entre 5 execuções obtidos. O valor final encontrado foi $lambda = 0.8$.

= Resultados
// Apresentar os resultados obtidos, comparar com os resultados conhecidos

A seguir seguem os resultados obtidos ao executar o algoritmo por $72$ segundos em cada iteração:

#figure(supplement: [tabela], caption: [Resultados obtidos])[
  #tablex(
    columns: 6,
    align: center + horizon,

    [], [*Ótimo*], colspanx(2)[*$f_("GLS")$*], colspanx(2)[*Gaps*],
    [*Instância*], [*$f_("ótimo")$*], [*$"Min"_(5)$*], [*$"Média"_(5)$*], [*$"gap"_"Min"$*], [*$"gap"_"Média"$*],
    [comp01], [5], [1291], [1389.8], [257.2], [276.96],
    [comp02], [24], [6165], [6641.2], [6165], [6641.2],
    [comp03], [64], [4576], [4972.0], [4576], [4972.0],
    [comp04], [35], [4538], [4823.6], [4538], [4823.6],
    [comp05], [284], [4747], [5623.2], [5393], [5623.2],
    [comp08], [37], [4399], [4700.6], [4399], [4700.6],
    [comp09], [96], [4471], [4642.0], [4471], [4642.0],
    [comp10], [4], [4187], [5146.0], [4187], [5146.0],
    [comp11], [0], [1373], [1436.8], [inf], [inf],
    [comp12], [294], [2342], [2629.8], [2342], [2629.8],
    [comp13], [59], [5558], [6277.6], [5558], [6277.6],
    [comp14], [51], [2817], [3087.6], [2817], [3087.6],
    [comp15], [62], [5062], [5279.4], [5062], [5279.4],
    [comp16], [18], [4660], [5181.6], [4660], [5181.6],
    [comp17], [56], [4756], [5266.6], [4756], [5266.6],
    [comp18], [61], [1054], [1154.2], [1054], [1154.2],
    [comp19], [57], [2901], [4108.8], [2901], [4108.8],
    [comp20], [4], [6143], [7367.6], [6143], [7367.6],
    [comp21], [74], [4288], [5004.6], [4288], [5004.6]
  )
] <results>

= Conclusão
// Apresentar as conclusões obtidas, o que foi aprendido, o que pode ser melhorado

O GLS é um algoritmo que se promete eficiente para o problema de alocação de horários de universidades. A implementação do algoritmo foi relativamente simples e facilmente generalizável para implementação de outras heurísticas para comparações, e a calibração dos parâmetros foi feita de maneira simples e direta.

Meus resultados não foram bons, e não consegui encontrar o motivo. Acredito que seja por conta da função de utilidade não ter sido implementada, e por conta disso, o algoritmo não consegue escapar de ótimos locais. Acredito que com a implementação da função de utilidade, o algoritmo se torne mais eficiente e consiga escapar de ótimos locais, e assim, melhorar os resultados obtidos.

Outro fator impactante é a geração de valores iniciais. Acredito que a geração de valores iniciais aleatórios não seja a melhor estratégia, e que uma estratégia de geração de valores iniciais mais inteligente possa melhorar drasticamente os resultados obtidos.

#bibliography("works.yml", title: "Referências")
