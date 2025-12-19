# RELATÓRIO PROJETO FINAL IP

# 🎮🏴‍☠️ Nome do jogo: Zarpar!
Um jogo desenvolvido em Pygame que une aventura e desafio, colocando o jogador no papel de um pirata em busca de escapar de uma ilha perigosa. Ao longo da jornada, é preciso explorar o cenário, coletar itens essenciais e desviar de obstáculos, testando reflexos, estratégia e tomada de decisão para alcançar o objetivo final.

---

# 👥 Integrantes:
- Beatriz Freitas Souza Pedrosa (bfsp)
- Beatriz Pandolfi Maroja (bpm)
- João Antônio Lins Carvalho de Aguiar  (jalca)
- João Luis de Siqueira Ribeiro (jlsr) 
- Luísa Bispo Lócio (lbl5)
- Marina Cabral Nogueira Lima (mcnl2)

---

# 📂 Estrutura do Projeto

Abaixo está a árvore de diretórios necessária para o funcionamento correto do jogo:

```text
Projeto-IP/
├── main.py     # Arquivo principal que inicia o jogo
├── classes/    # Pasta contendo a lógica modular e as classes do jogo
│   ├── config.py   # Variáveis globais 
│   ├── assets.py   # Carregamento de Imagens/Sons
│   ├── entidades.py    # Definição das classes (Jogador, Inimigo, Itens)
│   └── fase.py     # Lógica da fase, colisões e renderização
└── assets/     # Pasta de recursos externos
    ├── images/     # Arquivos de imagem 
    │   ├── pirata.png          
    │   ├── pirata_andando.png  
    │   ├── pirata_pulando.png  
    │   ├── carangueijo.png     
    │   ├── moeda.png           
    │   ├── diamante.png        
    │   ├── rum.png             
    │   ├── chave.png          
    │   ├── navio.png           
    │   ├── coqueiro.png        
    │   ├── background.png      
    │   ├── nuvens.png          
    │   ├── areia.png           
    │   ├── estrela.png
    │   └── Prints/     # Prints do jogo (README)
    │       ├── Print_inicio.jfif
    │       ├── Print_plataforma.jfif
    │       ├── Print_morte.jfif
    │       └── Print_final.jfif
    └── sons/    # Arquivos de áudio 
        ├── pulo.wav            
        ├── moeda.wav           
        ├── diamante.wav        
        ├── rum.wav             
        ├── inimigo.wav         
        ├── vitoria.wav         
        ├── gameover.wav        
        └── musica_fundo.ogg        
```

---

# 📸 Capturas de tela
![Imagem da tela inicial](assets/images/Prints/Print_inicio.jfif)

*Figura 1 – Tela inicial* 

![Imagem do personagem em cima da plataforma](assets/images/Prints/Print_plataforma.jfif)

*Figura 2 – Personagem na plataforma*

![Imagem da morte para o carangueijo](assets/images/Prints/Print_morte.jfif)

*Figura 3 – Morte para o caranguejo*  

![Imagem do fim dojogo](assets/images/Prints/Print_final.jfif)

*Figura 4 – Tela final do jogo*

---

# 🛠 Ferramentas, bibliotecas e frameworks
- **Pygame**: é o principal framework utilizado para a construção do jogo, atuando como o motor responsável pela execução e controle da aplicação. Gerencia o game loop, renderiza gráficos/textos, processa entradas (teclado) e controla o áudio via classes Sprite e Surface.
- **Bibliotecas os e sys**: utilizadas para garantir que o jogo encontre as pastas de sons e imagens em qualquer computador e feche o processo corretamente ao sair (manipulação de arquivos).
- **Arquitetura Modular (POO)**: o código foi separado em classes (Jogador, Fase, Assets). Isso torna o projeto organizado, fácil de corrigir e pronto para receber novas fases.
- **Versionamento**: uso de **Git e GitHub** para controle de versão e organização das etapas de desenvolvimento.
- **ChatGPT**: Dado o tempo apertado, contar com o ChatGPT como consultor foi de grande ajuda. A ferramenta contribuiu para economizar horas de debug, auxiliando na identificação de erros simples que poderiam passar despercebidos. Além disso, ele foi muito útil para gerar imagens do nosso jogo.

---

# 💡 Conceitos utilizados
Durante o processo de aprendizado de Python aplicado ao jogo, conseguimos estudar uma série de conceitos fundamentais da programação, como:
- **Estruturas de dados**: uso de listas e grupos de sprites para armazenar e gerenciar múltiplas entidades do jogo, como plataformas, inimigos e itens coletáveis.
- **Estruturas de controle**: utilização de laços de repetição (while e for) para manter o jogo em execução e percorrer os elementos do cenário, além de condicionais (if) para implementar física, colisões e regras de vitória e derrota.
- **Modularização**: divisão do código em múltiplos arquivos e classes, facilitando a leitura, manutenção e reutilização do código.

---

# 📋 Divisão de trabalho

- **Beatriz Freitas Souza Pedrosa:**  Desenvolvimento do código e adição dos aquivos de som
- **Beatriz Pandolfi Maroja:**  Separação do código em classes e desenvolvimento do README
- **João Antônio Lins Carvalho De Aguiar:**  Seleção das pngs do jogo e criação dos slides
- **João Luis de Siqueira Ribeiro:**  Desenvolvimento do código e seleção dos sons do jogo
- **Luísa Bispo Lócio:**  Separação do código em classes e finalização do README
- **Marina Cabral Nogueira Lima:** Desenvolvimento do código, criação dos slides e seleção das pngs do jogo

---

# ❌ Principais erros
O maior erro da equipe, de maneira geral, foi a demora para escolher de forma definitiva o estilo do jogo e, consequentemente, o atraso para entender e começar o código. Passamos uma quantidade significativa de tempo discutindo ideias diferentes e essa indecisão acabou consumindo um tempo precioso que poderia ter sido melhor utilizado no desenvolvimento efetivo do jogo.


---

# 💣Maior desafio
O maior desafio que enfrentamos foi a organização e distribuição do tempo, especialmente na última semana de aula, quando precisávamos entregar uma prova e três trabalhos em pouquíssimo tempo. A carga de atividades era intensa e estava espalhada ao longo da semana, o que dificultava a coordenação e a reunião da equipe para discutir as diversas partes do projeto. Esse cenário exigiu de nós uma gestão mais eficaz do tempo e das responsabilidades, para conseguirmos dar conta de todas as demandas e garantir a qualidade das entregas. 

---

# ✍🏼Lições aprendidas
Acho  que de maneira geral, a equipe se desenvolveu em três principais aspectos:

1. Aplicabilidade dos conceitos aprendidos: 
Vimos o conhecimento que adquirimos durante o semestre se materializar na prática e conseguimos aplicar o que aprendemos nas listas de exercícios diretamente na criação do jogo. À medida que implementávamos as diferentes partes do jogo, ficou claro como os conceitos se conectam e se complementam, aprimorando o processo de desenvolvimento. Essa experiência consolidou nosso aprendizado, transformando a teoria em algo tangível e completamente funcional.


2. Gestão de tempo: 
A gestão de tempo inicialmente era um grande desafio, especialmente na reta final do período, toda nossa equipe estava com uma sobrecarga de demandas. Durante essa fase, aprendemos a ser mais diretos e eficientes, priorizando as tarefas mais urgentes e dividindo o trabalho de forma mais estratégica. Tivemos que adaptar nossa rotina, focando nas atividades essenciais e evitando a procrastinação. A experiência nos ensinou a importância de organizar o tempo de maneira mais disciplinada, estabelecendo prazos realistas e distribuindo as responsabilidades de forma equilibrada, o que nos permitiu cumprir todas as tarefas de forma eficaz, mesmo sob pressão.


3. Utilização do Git e GitHub:
Aprender a utilizar Git e GitHub foi uma experiência muito positiva e enriquecedora. Essas ferramentas mostraram como é possível organizar melhor os projetos, acompanhar mudanças no código e trabalhar de forma mais colaborativa. Além disso, o uso de versionamento traz mais segurança, facilita correções de erros e evita a perda de trabalho. Esse aprendizado será extremamente útil em ações futuras, tanto em projetos acadêmicos quanto profissionais, já que Git e GitHub são amplamente utilizados no mercado de tecnologia e estimulam boas práticas de desenvolvimento.
