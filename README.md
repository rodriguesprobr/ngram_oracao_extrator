# Apresentação

Código-fonte utilizado na Versão *alpha* do Projeto de Extração de [*n-grams*](https://pt.wikipedia.org/wiki/N-grama) e Isolamento de Orações de textos do [Encontro Nacional de Pesquisa em Ciência da Informação (ENANCIB)](https://ancib.org/diretrizes-gerais/).

O conteúdo deste projeto é de livre distribuição, desde que seja referenciado e utilizada a Licença [Creative Commons 4.0 BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

Este projeto foi inspirado no software _White_, desenvolvido em Linguagem de Programação [Delphi](https://www.embarcadero.com/products/delphi) pelo Professor Dr. [Ricardo César Gonçalves Sant'Ana](http://lattes.cnpq.br/1022660730972320), utilizado nos artigos _Informação e Tecnologia no ENANCIB: Percurso do GT 08 no período de 2008 - 2015_ e _Informação e Tecnologia: Percurso Temático do GT 08_, liderados pela Professora Dra. [Plácida Leopoldina Ventura Amorim da Costa Santos](http://lattes.cnpq.br/7408791408049766). 

# Colaboradores do Projeto

- Profa. Dra. [Ana Carolina Simionato Arakaki](http://lattes.cnpq.br/9896600626524397) (Instituto Brasileiro de Informação em Ciência e Tecnologia - IBICT)
- Prof. Dr. [Felipe Augusto Arakaki](https://www.pesquisar.unb.br/professor/felipe-augusto-arakaki) (Universidade de Brasília - UnB)
- Profa. Dra. [Fernanda Farinelli](http://lattes.cnpq.br/1907817850408525) (Universidade de Brasília - UnB)
- Prof. Dr. [Fernando de Assis Rodrigues](https://rodrigues.pro.br) (Universidade Federal do Pará)

# Preparação dos Textos

Para a execução deste algoritmo, os textos já devem estar no [formato texto](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_403) (TXT), utilizado codificação [UTF-8](https://pt.wikipedia.org/wiki/UTF-8) nos arquivos. Existem vários conversores de outros formatos para o formato texto, inclusive _on-line_.

Os textos devem ser separados em diretórios/pastas por ano de publicação (*e.g.* 2014, 2015, 2016, etc.). Este projeto já inclui estes dados, mas podem ser modificados, excluídos ou subistituídos a depender das análises desejadas.

Se for de interesse, sugerimos que antes do processamento sejam removidos informações como autores, e-mails e referências biblográficas, bem como cabeçalhos e rodapés.

# Dependências do Projeto
Foi utilizado o Python na versão 3.10.
Além disso, são requeridas as seguintes bibliotecas:
- [pt-core-news-lg](https://spacy.io/models/pt), versão 3.7.x (deve ser instalado pelo comando python -m spacy download pt-core-news-lg)
- [SQLAlchemy](https://www.sqlalchemy.org/), versão 2.x
- [spacy](https://spacy.io/), na versão 3.7.x (não utilizar o spacy na versão 4.x, pois não há o núcleo em língua portuguesa)
- [spacy-ngram](https://pypi.org/project/spacy-ngram/), na versão 0.0.3 (deve ser instalado pelo comando python -m spacy download spacy-ngram)
- [tqdm](https://github.com/tqdm/tqdm), na versão 4.66.x

O algoritmo faz o uso do [SQLite3](https://sqlite.org/) como [Sistema de Gerenciamento de Banco de Dados](https://pt.wikipedia.org/wiki/Sistema_de_gerenciamento_de_banco_de_dados). Todavia, o código-fonte já possui uma instância para facilitar a sua execução. O _SQLAlchemy_ possui o dialeto para integração automática dos dados com o algoritmo.

Foi utilizado uma adaptação do código-fonte de pré-processamento de textos para o _spacy_, desenvolvido por [Omri Mendels, da Cientista de Dados da Microsoft](https://gist.github.com/omri374/ec1c243a5a94a657dae40078d47977b6). Parte do seu código pode ser encontrado no diretório _util_, arquivo _preprocessamento.py_.

# Como utilizar
Após a instalação do _Python_ e das bibliotecas, deve-se executar na seguinte ordem: 1) _processar.py_ e 2) _analisar.py_.

O _script_ _processar.py_ pode demorar algumas horas para terminar a execução. Ele utiliza programação em _threads_ para processar múltiplos textos ao mesmo tempo. No arquivo _config.json_ você poderá aumentar ou diminuir quantos textos são processados em paralelo, alterando o valor do atributo _threads_quantidade_.

No _config.json_ também pode ser alterado se os dados serão excluídos na execução (atributo _excluir_dados_) e o local em que o algoritmo fará a varredura procurando os textos a serem processados (atributo _comunicacoes_cientificas_dir_).

# _TODO List_
- [ ] Refatoração de parte do algoritmo
- [ ] Orientação a Objetos
- [x] Melhorias no processamento paralelo para evitar _OutOfMemoryError_. (Commit 
b384192)