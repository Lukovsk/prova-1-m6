# prova-2-m6

## Enunciado
Desenvolva um código em Python capaz de utilizar o openCV para a leitura de um vídeo (frame a frame) e, para cada frame, o seu código deve identificar e marcar na imagem os retângulos correspondentes a cada uma das faces encontradas. Ao final do código, um novo vídeo deve ser salvo com a(s) face(s) identificada(s).

## Implementação

Na pasta ```src/```, existe o arquivo ```main.py``` e um vídeo em formato mp4. Ao rodar o arquivo ```main.py```, ele abre o vídeo em questão e identifica rostos utilizando o haar Cascade, sobrepondo retângulos vermelhos nos rostos identificados.
Por questões, provavelmente, da eficácia do modelo ou de parametrização, ele identifica coisas que não são rostos às vezes.