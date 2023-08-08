# Hullermeier Index for fuzzy partitions

**Projeto desenvolvido como Trabalho de Conclusão do Curso de Anderson de Alencar Barros**

Este projeto é a implementação do índice de Hullermeier usando pontos flutuantes de precisão arbitrária, conhecido como bigfloats, sendo útil para projetos que requerem alta precisão onde um ponto de fluante de precisão dupla poder ocasionar erros de divisão por zero ou não ser preciso o suficiente. Como o índice varia entre 0 e 1, também pode ser convertidos para precisão dupla com o operador do Python.

O projeto foi implementado segundo o artigo,

```bash
HULLERMEIER, E. et al. Comparing fuzzy partitions: A generalization of the rand index and
related measures. IEEE Transactions on Fuzzy Systems, IEEE, v. 20, n. 3, p. 546–556, 2011.
```

Para explorar o projeto comece fazendo um clone do projeto,

```bash
git clone https://github.com/AndersonAlencarBarros/hullermeier
```

Os requisitos para executar esse projeto são,

- Poetry
- Python 3.10

Para instalar use o comando,

```bash
pip install hullermeier
```

## Exemplo

```python
from hullermeier import hullermeier
import numpy as np


U = np.array([[1.0, 0, 0], [0, 1.0, 1.0]])
V = np.array([[1.0, 1, 0], [0, 0, 1]])

indice_de_hullermeier = hullermeier(U, V)

print(indice_de_hullermeier)
```