# Control Finanças


Cnteúdos
=================
<!--ts-->
   * [Sobre](#Sobre)
   * [Ínicio](#Ínicio)
      * [Pré Requisitos](#pre-requisitos)
      * [Instalação](#instalacao)
   * [Autor](#autor)
<!--te-->

# Sobre
    Este projeto consiste obter um controle das finanças, cadastrando Receitas e Despesas
    filtrando e exportando arquivo csv por data.


# Ínicio

* Essas instruções serão necessárias para configuração e execução do projeto em sua máquina local para desenvolvimento e testes. Antes de tudo, visualize o arquivo abaixo sobre como você realizará a configuração do projeto para execução oficial.

# Pré Requisitos
* ![Badge](https://img.shields.io/badge/Python-3.11.2-brightgreen)
* ![Badge](https://img.shields.io/badge/Django-4.2-brightgreen)




# Instalação

* É necessário ter em sua máquina o Python 3.11 ou superior que é disponibilizado no site oficial do Python (https://www.python.org/downloads/). Antes de finalizar confira em suas Variações de Ambiente do Windows se o Python encontra-se configurado em sua "path". Posteriormente, faz se necessário criar e configurar sua própria maquina virtual de desenvolvimento para que as ferramentas de projeto não se instalem em suas respectivas máquinas permanentemente.

Criar a virtual environment:

    python -m venv (nomedaEnvironment)

 Ativar a environment criada

    (nomeDaEnvironment)\Scripts\activate

 Instalar o requirements.txt:

    pip install -r requirements.txt

 Atualizar as migrações do banco de dados:

    py manage.py makemigrations

 Construir o banco de dados da aplicação:

    py manage.py migrate

# Autor

* Daniel de Oliveira - _Desenvolvedor Backend_ - @danieldl0 <br>
