#Formal Language Simulator


1. **Autômato Finito**

  Representando autômato finitos determinístcos e não-determinísticos esta classe é constituída de um conjunto de estados, um conjunto de símbolos que é o alfabeto, um estado inicial, um conjunto de estados finais, um hashmap(“dict”) com as transições entre os estados. Ao construir um objeto, inicialmente precisamos apenas dos estados, alfabeto, estado inicial e estados finais. Podemos adicionar novos estados com o objeto já construído, e também devemos adicionar as transições após a construção. Os estados também são representados por uma classe que é intrinsecamente relacionada com a implementação do autômato.

  O reconhecimento de uma sentença por um autômato é realizado de forma recursiva. Començando do estado inicial, verifica-se se existe alguma transição que pode ser tomada, isto é por epsilon ou pelo primeiro símbolo da sentença, no segundo caso o primeiro símbolo é retirado, o resto da sentença é passado para o próximo estado. A cada estado é verificado se a sentença já não é vazia, e se for, se o estado atual é aceitador.

  A determinização e remoção das epsilon-transições é feita de maneira similar à manual. Começamos pelo “multi-estado” do epsilon-fecho do estado inicial e criamos os “multi-estados” alcançáveis por suas transições, e os “multi-estados” alcançáveis pelos anteriores… Quando todos estes e suas transições estão criadas, criamos um estado para cada “multi-estado” e o hashmap de suas transições, agora com os novos estados. A partir disso já podemos substituir nosso antigo autômato por sua determinização, não esquecendo de substituir também o conjunto de estados finais, e o estado inicial por seus referentes.

  Temos métodos de remoção de estados inalcançáveis e mortos, implementados como visto em sala. São utilizados para a minimização do autômato, onde o determinizamos, removemos os inalcançáveis, removemos os mortos e removemos os estados equivalentes. Para realizar esta última operação, foi necessária a implementação da procura por classes de equivalência onde procuramos conjuntos de estados equivalentes entre si, de modo que possamos torná-los um só na minimização.

  Para o complemento de um autômato criamos um novo autômato como uma cópia do atual, determinizamos esse novo autômato, e adicionamos um estado morto, que leva a ele mesmo por todas as transições, em qualquer transição não definida. Trocamos o conjunto de estados finais do novo automato pelo seu complemento, isto é o conjunto de todos os estados do autômato exceto os estados que estavam definidos como finais. Retornamos então este novo autômato.

  A intersecção entre autômatos foi realizada de forma simples exceto pela implementação da união entre dois autômatos. A intersecção dos autômatos A e B é dada pelo complemento da união entre o complemento de A e o complemento de B. 

2. **Gramática Regular**

  Constituímos a classe de um conjunto de produções, um conjunto de símbolos terminais, um conjunto de símbolos não-terminais, e um símbolo inicial, que necessariamente pertence ao conjunto dos símbolos não-terminais. Inicializamos um objeto com seus símbolos, e adicionamos cada produção separadamente, checando se seus símbolos são coerentes. As produções também são descritas por uma classe, onde cada objeto é inicializado com o lado esquerdo e direito de uma produção.

  Um método estático para construir um nova gramática a partir de um texto foi necessário. O texto é dividido em linhas e de cada linha retiramos os símbolos “->” sabendo que o texto a direita deles é referente ao lado direito de cada uma das produções da mesma linha. Dividindo o resto do texto da linha pelo separador “|” temos os lados direitos das produções, então podemos construir cada uma e adicionar na nova gramática.

  Outra construção importante é a passagem de uma gramática para autômato finito não determinístico. Criamos um conjunto de estados com um estado referente ao símbolo não-terminal inicial, e um estado final referente às produções que levam a símbolos terminais. Percorremos as produções e adicionamos estados para cada lado esquerdo ainda não visto. Considerando final também todos os estados referentes a não-terminais que possuem produções que levam à epsilon. Com todos os estados criados, criamos também o autômato, mas ainda precisamos criar as transições. Percorrendo todas as produções: cada produção que leva a um símbolo terminal, adicionamos uma transição do estado respectivo ao lado esquerdo desta produção, pelo símbolo terminal, até o estado final mencionado inicialmente; cada produção que leva a um símbolo terminal seguido de não terminal, adicionamos uma transição do estado respectivo ao não-terminal do lado esquerdo desta produção, pelo símbolo terminal, ao estado respectivo ao não-terminal do lado direito. Então, com todas a transições adicionadas, podemos retornar o autômato.

3. **Expressão Regular**

  Com o objeto criado partindo apenas do texto respectivo à expressão, este é constituído também de um conjunto com os símbolos “terminais” encontrados no texto. O texto também passa por um pré-processamento, que o formata para facilitar o trabalho dos outros métodos, símbolos de concatenação são adicionados e parenteses desnecessários são retirados.

  Temos um método que é utilizado durante outros processamentos, que retorna o símbolo menos significativo do “nível mais exterior” da expressão, e sua posição. Isto é, o símbolo da operação que deve ser feita antes das outras considerando o estado atual da expressão.

  Necessitamos transformar essa expressão em um autômato finito utilizando o método de De Simone, portanto precisamos construir a árvore de De Simone. Criamos diversas classes para cada nodo referente a uma operação, e suas implementações de percorrimento da árvore. Ou seja, os retornos de seus percorrimentos “indo para cima”, “indo para baixo” na árvore, e sua costura. E na classe da ER construímos a árvore, utilizando estes nodos, e método acima mencionado que retorna a operação que devemos fazer na expressão.

  Com a árvore de De Simone montada podemos começar seu percorrimento para construir o autômato referente à expressão. Esta construção foi feita de maneira muito similar à maneira que realizamos manualmente em sala. Inicialmente construímos uma tabela com um estado inicial e sua composição é referente ao percorrimento da árvore partindo da raiz. Percorremos todos os estados na tabela (inicialmente apenas um, mas adicionamos novos estados durante este percorrimento), e verificamos os nodos em sua composição, se o nodo é lambda este estado é final, se o nodo é referente a um símbolo por onde ainda não há transição, criamos um novo estado e adicionamos os nodos alcançáveis por este à composição do novo estado, se o nodo é referente a um símbolo por onde já temos uma transição, unimos à composição do estado na transição os nodos alcançáveis pela costura deste nodo. Acabamos de verificar os nodos, então precisamos ter certeza que estes novos estados já não estão na tabela, checando as composições deles e dos estados na tabela substituímos os estados duplicados por aqueles que já estão na tabela, e adicionamos os não duplicados nela. Com a tabela completa construímos o autômato e o retornamos.

4. **Interface Gráfica**

  Feita utilizando o framework Qt, introduzimos os seguintes elementos à utilização:

  1. *Edição de Expressão Regular*

    Uma caixa de texto onde uma expressão regular é digitada. Pode ser transformada em autômato finito enviando este para o Slot A ou B e a lista de autômatos envolvidos. Ou utilizar esta para fazer uma busca por palavras que se encaixam em um texto.

  2. *Busca de palavras em texto*

    Com a janela de busca aberta, após entrar com uma expressão regular, o texto pode ser colocado na nova caixa de texto e os elementos que se encaixarem na expressão aparecerão destacados.

  3. *Edição de Gramática Regular*

    Uma caixa de texto onde uma gramática pode ser digitada. Pode ser transformada em autômato finito enviando este para o Slot A ou B e a lista de autômatos envolvidos. Podemos também compará-la com a expressão regular, tal que uma nova janela se abrirá com o resultado da equivalência entre a ER e GR.

  4. *Slots A e B para autômatos finitos*

    Tabelas onde os autômatos realizados são mostrados. Podem ser determinizados, minimizados, ou feito seus complementos, todos os autômatos resultantes dessas operações também são adicionados à lista de autômatos envolvidos. Podemos também realizar a intersecção entre os dois autômatos atualmente nos slots, o resultado e colocado no Slot A, mas também na lista de autômatos.

  5. *Lista de Autômatos envolvidos*

    Mostra todos os autômatos resultantes das operações realizadas, como um histórico, qualquer autômato na lista pode ser selecionado e colocado novamente em algum dos Slots.
