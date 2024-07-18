# Apresentação

Código-fonte utilizado na Versão *alpha* do Projeto de Extração de [*n-grams*](https://pt.wikipedia.org/wiki/N-grama) e Isolamento de Orações de textos, inicialmente voltado para processamento de comunicações científicas do [Encontro Nacional de Pesquisa em Ciência da Informação (ENANCIB)](https://ancib.org/diretrizes-gerais/).

O conteúdo deste projeto é de livre distribuição, desde que seja referenciado e utilizada a Licença [Creative Commons 4.0 BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

Este projeto foi inspirado no software _White_, desenvolvido em Linguagem de Programação [Delphi](https://www.embarcadero.com/products/delphi) pelo Professor Dr. [Ricardo César Gonçalves Sant'Ana](http://lattes.cnpq.br/1022660730972320), utilizado nos artigos _Informação e Tecnologia no ENANCIB: Percurso do GT 08 no período de 2008 - 2015_ e _Informação e Tecnologia: Percurso Temático do GT 08_, liderados pela Professora Dra. [Plácida Leopoldina Ventura Amorim da Costa Santos](http://lattes.cnpq.br/7408791408049766). 

# Como citar
RODRIGUES, F. A.; FARINELLI, F.; ARAKAKI, A. C. S.; ARAKAKI, F. A. Projeto de Extração de n-grams e Isolamento de Orações de textos. GitHub (repositório). São Francisco, 2024. Disponível em: https://github.com/rodriguesprobr/ngram_oracao_extrator.

# Colaboradores do Projeto
- Prof. Dr. [Fernando de Assis Rodrigues](https://rodrigues.pro.br) (Universidade Federal do Pará - UFPA)
- Profa. Dra. [Fernanda Farinelli](http://lattes.cnpq.br/1907817850408525) (Universidade de Brasília - UnB)
- Profa. Dra. [Ana Carolina Simionato Arakaki](http://lattes.cnpq.br/9896600626524397) (Instituto Brasileiro de Informação em Ciência e Tecnologia - IBICT)
- Prof. Dr. [Felipe Augusto Arakaki](https://www.pesquisar.unb.br/professor/felipe-augusto-arakaki) (Universidade de Brasília - UnB)

# Preparação dos Textos
Para a execução deste algoritmo, os textos já devem estar no [formato texto](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_403) (TXT), utilizado codificação [UTF-8](https://pt.wikipedia.org/wiki/UTF-8) nos arquivos. Existem vários conversores de outros formatos para o formato texto, inclusive _on-line_.

Os textos devem ser separados em diretórios/pastas por ano de publicação (*e.g.* 2014, 2015, 2016, etc.). Este projeto já inclui estes dados, mas podem ser modificados, excluídos ou subistituídos a depender das análises desejadas.

Se for de interesse, sugerimos que antes do processamento sejam removidos informações como autores, e-mails e referências biblográficas, bem como cabeçalhos e rodapés.

# Dependências do Projeto
Foi utilizado o [Python](https://www.python.org) na versão 3.10.
Além disso, são requeridas as seguintes bibliotecas:
- [pt-core-news-lg](https://spacy.io/models/pt), versão 3.7.x
- [SQLAlchemy](https://www.sqlalchemy.org/), versão 2.x
- [spacy](https://spacy.io/), na versão 3.7.x (não utilizar o spacy na versão 4.x, pois não há o núcleo em língua portuguesa)
- [spacy-ngram](https://pypi.org/project/spacy-ngram/), na versão 0.0.3
- [tqdm](https://github.com/tqdm/tqdm), na versão 4.66.x

O algoritmo faz o uso do [SQLite3](https://sqlite.org/) como [Sistema de Gerenciamento de Banco de Dados](https://pt.wikipedia.org/wiki/Sistema_de_gerenciamento_de_banco_de_dados). Todavia, o código-fonte já possui uma instância para facilitar a sua execução. O _SQLAlchemy_ possui o dialeto para integração automática dos dados com o algoritmo.

Foi utilizado uma adaptação do código-fonte de pré-processamento de textos para o _spacy_, desenvolvido por [Omri Mendels, da Cientista de Dados da Microsoft](https://gist.github.com/omri374/ec1c243a5a94a657dae40078d47977b6). Parte do seu código pode ser encontrado no diretório _util_, arquivo _preprocessamento.py_.

## Como instalar

Após a instalação do [Python](https://www.python.org/downloads/), recomendamos que se utilize um instalador de bibliotecas/pacotes, como o Pip. Você pode ver um tutorial do Pip em português do Brail no endereço eletrônico https://packaging.python.org/pt-br/latest/tutorials/installing-packages/.

Com o Pip, você poderá instalar o [SQLAlchemy](https://www.sqlalchemy.org/), [spacy](https://spacy.io/) e o [tqdm](https://github.com/tqdm/tqdm).
Já o [pt-core-news-lg](https://spacy.io/models/pt) e o [spacy-ngram](https://pypi.org/project/spacy-ngram/) devem ser instalados pelos comandos _python -m spacy download pt-core-news-lg_ e _python -m spacy download spacy-ngram_. Importante: Até o momento, o _pt-core-news-lg_ só existe na versão 3.7.x do _spacy_, não sendo possíveol a utilização da versão 4. Verifique se esta versão foi instalada corretamente.

Dúvidas podem ser verificadas entrando em contato com um dos colaboradores do projeto e _bugs_ podem ser incluídos nos _issues_ aqui no GitHub. Sinta-se à vontade para nos contatar ;).

# Como utilizar
Após a instalação do _Python_ e das bibliotecas, deve-se executar o _script_ _\_\_init\_\_.py_.

O _script_ _\_\_init\_\_.py_ pode demorar algumas horas para terminar a execução. Ele utiliza programação em _threads_ para processar múltiplos textos ao mesmo tempo. No arquivo _config.json_ você poderá aumentar ou diminuir quantos textos são processados em paralelo, alterando o valor do atributo _threads_quantidade_.

## Parametrização do config.json

Parte do algoritmo pode ser personalizado no arquivo _config.json_.

- Se na execução os dados serão excluídos, deve ser deixar o atributo _excluir_dados_ para _true_. Caso contrário, deve-se configurar o parâmetro para _false_.
- O local em que o algoritmo fará a varredura procurando as comunicações científicas a serem processadas está referenciado no atributo _local_comunicacoes_cientificas_. O padrão está configurado para pasta dados, subpasta comunicacoes_cientificas. O projeto já está populado com as comunicações científicas do ENANCIB, que podem ser substituídas.
- O local em que o algoritmo exportará a frequência e a ocorrência de ngramas por ano são configuradas, respecitivamente, nos atributos _local_analise_ngram_frequencia_por_ano_ e _local_analise_ngram_ocorrencia_por_ano_. Por padrão, o local em que serão salvos os arquivos em formato [Comma-Separated Values (CSV)](https://pt.wikipedia.org/wiki/Comma-separated_values) é na pasta dados.

# _TODO List_
- [ ] Separar Comunicações Científicas (_e.g._ poster, resumo, etc.).
- [x] Verificar a ocorrência de n-gramas sem relação com nenhuma Comunicação Científica.
- [x] Remover hyperlinks no preprocessamento.
- [x] Refatoração de parte do algoritmo.
- [x] Orientação a Objetos.
- [x] Análise tanto da Frequência como da Ocorrência de palavras por ano.
- [x] Melhorias no processamento paralelo para evitar _OutOfMemoryError_.