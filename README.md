# Power-Dev: Prova de Conceito de Janela "Incaturável"

Este projeto é uma exploração de engenharia de software de baixo nível com o objetivo de criar um sistema onde um aplicativo pode se tornar "invisível" para softwares de captura de tela no Linux (X11).

## Objetivo Final

Criar um sistema de Prova de Conceito (PoC) composto por dois programas:
1.  **Um Compositor Modificado:** Uma versão customizada de um compositor X11 que contém a lógica para "ocultar" janelas específicas.
2.  **Um Aplicativo Alvo:** Um programa (em Python) que pode se "marcar" para ser ocultado pelo nosso compositor.

O sistema deve permitir que o Aplicativo Alvo seja visível para o usuário no monitor, mas invisível para qualquer software de captura de tela (como Flameshot ou OBS).

---

## Redefinição do Plano: Migração para o Picom

A exploração inicial com o compositor `xcompmgr` revelou limitações fundamentais que impediram a correta detecção e manipulação da janela alvo em um ambiente de desktop moderno (XFCE). O `xcompmgr` não conseguia obter os metadados necessários da janela (`WM_CLASS` ou propriedades customizadas) de forma confiável.

Por isso, o projeto foi redefinido para utilizar o **picom**, um compositor moderno, ativamente mantido e muito mais poderoso, que oferece os mecanismos necessários (como uma interface DBus) para alcançar nosso objetivo de forma mais robusta e elegante.

---

## Novas Fases do Projeto (Baseado no Picom)

### Fase 1: Controle do Ambiente (Versão Picom)

*   **Objetivo:** Provar que podemos compilar e executar nossa própria versão do `picom`.
*   **Atividades:**
    1.  Modificar o `shell.nix` para incluir o `picom` e suas dependências de compilação (`meson`, `ninja`, `dbus`, etc.).
    2.  Obter o código-fonte do `picom` e copiá-lo para um diretório local (`src/picom-modified`).
    3.  Compilar o `picom` original, sem modificações, e executá-lo (após desativar o compositor do XFCE) para confirmar que nosso ambiente de desenvolvimento está correto.
*   **Status:** A Fazer.

---

### Fase 2: O "Sinal Secreto" (Estratégia Validada)

*   **Objetivo:** Fazer nossa versão do `picom` identificar a janela secreta.
*   **M��todo:** Manteremos a estratégia de usar a `WM_CLASS` da janela, que se provou ser um método de identificação robusto.
*   **Atividades:**
    1.  **No Aplicativo Alvo (`src/jeitinhoBR.py`):** Garantir que o aplicativo defina sua `WM_CLASS` para um valor único e conhecido (ex: `"jeitinhoBR.py"`).
    2.  **No Compositor (C/C++ - `picom`):** Estudar o código-fonte do `picom` para encontrar a função principal que gerencia e processa as janelas. Adicionaremos uma função que lê a `WM_CLASS` de cada janela e a "marca" com uma flag interna customizada se ela corresponder ao nosso sinal secreto.
*   **Critério de Sucesso:** Adicionando logs ao `picom`, podemos confirmar que ele identifica e marca corretamente a janela do `jeitinhoBR.py` quando ela é criada.

---

### Fase 3: A Lógica da Ocultação (Modo Picom)

*   **Objetivo:** Modificar o `picom` para que ele ignore o desenho da janela marcada quando o modo "invisível" estiver ativo.
*   **Método:** Usaremos as flags internas da estrutura de janelas do `picom` para controlar a renderização.
*   **Atividades:**
    1.  **Análise de Código:** Identificar a estrutura de dados que representa uma janela no `picom` e encontrar uma flag apropriada (como `paint_excluded` ou similar) ou adicionar a nossa própria (`powerdev_secret_window`).
    2.  **Implementação da Condição:** No loop de renderização principal do `picom`, adicionaremos uma condição: `if (g_modo_invisivel && janela_tem_flag_secreta) { /* pular renderização */ }`.
*   **Critério de Sucesso:** Com o `g_modo_invisivel` ativado manualmente no código, a janela do `jeitinhoBR.py` deve se tornar invisível para o usuário.

---

### Fase 4: O "Gatilho" via DBus

*   **Objetivo:** Criar um mecanismo para ligar e desligar a "invisibilidade" sob demanda, de forma limpa e programática.
*   **Método:** Expondremos uma nova função na interface DBus do `picom`.
*   **Atividades:**
    1.  **No Compositor (C/C++):**
        *   Adicionaremos um novo método à interface DBus do `picom`, como `dev.power.ToggleInvisibility`.
        *   Este método irá inverter o valor da variável booleana global `g_modo_invisivel`.
        *   Após inverter a variável, ele forçará um redesenho de todas as janelas para que a mudança tenha efeito imediato.
    2.  **No Aplicativo Alvo (Python):**
        *   Adicionaremos a biblioteca `pydbus` ao nosso ambiente `shell.nix`.
        *   O script `jeitinhoBR.py` terá uma função que se conecta ao DBus e chama o método `dev.power.ToggleInvisibility` do nosso `picom` modificado.
*   **Critério de Sucesso:** Podemos executar o `picom` e o `jeitinhoBR.py`. Ao chamar a função de gatilho no Python, a janela do overlay desaparece e reaparece na tela.

---

### Fase 5: Teste Final e Validação

*   **Objetivo:** Validar que a solução completa atinge o objetivo original de forma automática.
*   **Método:** A lógica final será um pouco diferente do plano original. O objetivo é que a janela seja *sempre* visível para o usuário, mas *nunca* para a captura de tela. Isso exigirá uma detecção mais inteligente no `picom`, mas como PoC, o gatilho manual ainda é válido.
*   **Atividades de Teste (com Gatilho Manual):**
    1.  Executar nosso `picom` final (com o compositor do XFCE desativado).
    2.  Executar nosso `jeitinhoBR.py`. A janela está visível.
    3.  Iniciar o Flameshot ou OBS.
    4.  Ativar o modo invisibilidade via gatilho (ex: uma tecla no app Python que chama a função DBus).
    5.  Capturar a tela com o Flameshot.
    6.  Desativar o modo invisibilidade. A janela continua visível para o usuário durante todo o processo, exceto por um piscar momentâneo.
*   **Critério de Sucesso:** A imagem capturada pelo Flameshot **não contém** a janela do nosso aplicativo.