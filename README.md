# Compilado CLI

![Python - Version](https://img.shields.io/badge/python-3.10-green) [![License - MIT](https://img.shields.io/badge/license-PSF--2.0-9400d3.svg)](https://spdx.org/licenses/PSF-2.0.html)

Automatização de tarefas através de linha de comando para a geração de assets para episódios do **Compilado**, a newsletter e podcast do canal **[Código Fonte TV](https://youtube.com/codigofontetv)**.

## Objetivo

`compilado-cli` gera thumbnails a partir de modelos pré-prontos disponíveis em arquivos PSD. As informações a serem preenchidas são automaticamente coletadas a partir do feed RSS do podcast:

## Recursos

- Gerador automático de thumbnail para o Youtube e Podcast a partir da data do último lançamento do podcast, usando o Adobe Photoshop.
- Gerador do conteúdo da newsletter a partir de um documento no Dropbox Paper _(EM DESENVOLVIMENTO)_
- Agendamento da newsletter _(EM DESENVOLVIMENTO)_

## Como usar

### Thumbnails

Geração automática a partir da data de publicação do último episódio do podcast

```shell
$ compilado thumbnail -a
...
```

`-a` ou `--auto` faz com que as informações sejam buscadas automaticamente a partir do feed RSS do podcast

Com informações personalizadas

```shell
$ compilado thumbnail -e "#027" -p "18/09 à 24/09"
...
```

`-e` ou `--episode` é o número do episódio

`-p` ou `--period` é o período a qual compreende o conteúdo do episódio

## Instalação

```shell
$ pip install -r requirements.txt
...
```

## Tecnologias utilizadas

Foi utilizado _Python_ como linguagem de programação e algumas bibliotecas para leitura de _feed rss_ do podcast, manipulação do _Adobe Photoshop_ entre outras.

## Autores

- **Gabriel Froes** - _Initial work_ - [Twitter](https://www.twitter.com/gabrielfroes)
- **Vanessa Weber** - _Initial work_ - [Twitter](https://www.twitter.com/nessaweberfroes)

## Youtube Channel

![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UCFuIUoyHB12qpYa8Jpxoxow?style=social)

## Licença

Esse projeto está sob a licença [GNU General Public License](https://opensource.org/licenses/GPL-3.0).
