import asyncio
import flet as ft
# import flet_audio as fta


def main(page: ft.Page):

    # ============================================================
    # CONFIGURAÇÕES DA PÁGINA
    # ============================================================

    page.title = "Pong - Etapa 8"

    # Fundo preto
    page.bgcolor = ft.Colors.BLACK

    # Remove o espaçamento da página
    page.padding = 0

    # Pasta onde ficam imagens, sons e outros arquivos
    page.assets_dir = "assets"

    

    # =====================================================
    # SONS DO JOGO
    # =====================================================

    # Som da bola batendo na raquete
    som_raquete = fta.Audio(
        src="raquete.wav"
    )

    # Som da bola batendo na parede
    som_parede = fta.Audio(
        src="parede.wav"
    )

    # Som quando um jogador marca ponto
    som_ponto = fta.Audio(
        src="ponto.wav"
    )

    # Registra os serviços de áudio na página
    #page.services.extend([
    #    som_raquete,
    #    som_parede,
    #])  


    # =====================================================
    # TESTE DO ÁUDIO
    # =====================================================

    async def testar_audio():

        # Reproduz o som da raquete
        #await som_raquete.play()

    # Executa o teste
    page.run_task(testar_audio) 


    # ============================================================
    # TAMANHO DO CAMPO
    # ============================================================

    largura = 800
    altura = 450


    # ============================================================
    # PLACAR
    # ============================================================

    pontos_1 = 0
    pontos_2 = 0

    placar_1 = ft.Text(
        "0",
        size=40,
        color=ft.Colors.WHITE
    )

    placar_2 = ft.Text(
        "0",
        size=40,
        color=ft.Colors.WHITE
    )


    # ============================================================
    # LINHA CENTRAL
    # ============================================================

    linha_central = ft.Column(
        spacing=10,
        controls=[
            ft.Container(
                width=4,
                height=20,
                bgcolor=ft.Colors.WHITE
            )
            for _ in range(20)
        ]
    )


    # ============================================================
    # CONFIGURAÇÕES DAS RAQUETES
    # ============================================================

    largura_raquete = 15
    altura_raquete = 90


    # ============================================================
    # RAQUETE 1
    # ============================================================

    raquete_1 = ft.Container(
        width=largura_raquete,
        height=altura_raquete,
        bgcolor=ft.Colors.WHITE,
        border_radius=5,

        # Posição inicial
        left=30,
        top=altura / 2 - altura_raquete / 2
    )


    # ============================================================
    # RAQUETE 2
    # ============================================================

    raquete_2 = ft.Container(
        width=largura_raquete,
        height=altura_raquete,
        bgcolor=ft.Colors.WHITE,
        border_radius=5,

        # Posição inicial
        left=largura - 45,
        top=altura / 2 - altura_raquete / 2
    )


    # ============================================================
    # FUNÇÃO PARA MOVER A RAQUETE 1
    # ============================================================

    def mover_raquete_1(e: ft.DragUpdateEvent):

        # Obtém o deslocamento vertical do dedo/mouse
        raquete_1.top += e.local_delta.y


        # Impede ultrapassar o topo
        if raquete_1.top < 0:
            raquete_1.top = 0


        # Impede ultrapassar o fundo
        if raquete_1.top > altura - altura_raquete:
            raquete_1.top = altura - altura_raquete


        # Atualiza a raquete
        raquete_1.update()


    # ============================================================
    # FUNÇÃO PARA MOVER A RAQUETE 2
    # ============================================================

    def mover_raquete_2(e: ft.DragUpdateEvent):

        # Obtém o deslocamento vertical
        raquete_2.top += e.local_delta.y


        # Impede ultrapassar o topo
        if raquete_2.top < 0:
            raquete_2.top = 0


        # Impede ultrapassar o fundo
        if raquete_2.top > altura - altura_raquete:
            raquete_2.top = altura - altura_raquete


        # Atualiza a raquete
        raquete_2.update()


    # ============================================================
    # ÁREA DE TOQUE DO JOGADOR 1
    # ============================================================

    area_toque_1 = ft.GestureDetector(

        # Detecta o movimento do dedo/mouse
        on_pan_update=mover_raquete_1,

        # Intervalo entre os eventos
        drag_interval=5,

        # Área transparente
        content=ft.Container(
            width=largura / 2,
            height=altura,
            bgcolor=ft.Colors.TRANSPARENT
        ),

        # Posição
        left=0,
        top=0
    )


    # ============================================================
    # ÁREA DE TOQUE DO JOGADOR 2
    # ============================================================

    area_toque_2 = ft.GestureDetector(

        # Detecta o movimento do dedo/mouse
        on_pan_update=mover_raquete_2,

        # Intervalo entre os eventos
        drag_interval=5,

        # Área transparente
        content=ft.Container(
            width=largura / 2,
            height=altura,
            bgcolor=ft.Colors.TRANSPARENT
        ),

        # Começa na metade direita
        left=largura / 2,
        top=0
    )


    # ============================================================
    # BOLA
    # ============================================================

    bola = ft.Container(
        width=20,
        height=20,

        # Cor da bola
        bgcolor=ft.Colors.WHITE,

        # Deixa a bola redonda
        border_radius=10,

        # Posição inicial
        left=largura / 2 - 10,
        top=altura / 2 - 10
    )


    # ============================================================
    # VELOCIDADE DA BOLA
    # ============================================================

    # Velocidade horizontal
    velocidade_x = 5

    # Velocidade vertical
    velocidade_y = 3

    #Velocidade vertical máxima
    velocidade_max_y = 5



    def reiniciar_bola(direcao):

        # Coloca a bola novamente no centro do campo
        bola.left = largura / 2 - bola.width / 2
        bola.top = altura / 2 - bola.height / 2

        # Mantém a velocidade vertical
        # e define para qual lado a bola irá
        velocidade_x = 5 * direcao

        return velocidade_x


    # ============================================================
    # MOVIMENTO DA BOLA
    # ============================================================

    async def mover_bola():

        # Informamos que estas variáveis pertencem
        # à função main() e serão alteradas aqui
        nonlocal velocidade_x, velocidade_y
        nonlocal pontos_1, pontos_2

        while True:

            # =================================================
            # MOVIMENTO DA BOLA
            # =================================================

            bola.left += velocidade_x
            bola.top += velocidade_y


            # =================================================
            # COLISÃO COM O TOPO
            # =================================================

            if bola.top <= 0:

                bola.top = 0

                velocidade_y = -velocidade_y

                # Toca o som da bola batendo na parede
                #await som_parede.play()


            # =================================================
            # COLISÃO COM O FUNDO
            # =================================================

            if bola.top >= altura - bola.height:

                bola.top = altura - bola.height

                velocidade_y = -velocidade_y

                # Toca o som da bola batendo na parede
                #await som_parede.play()


            # =================================================
            # COLISÃO COM A RAQUETE 1
            # =================================================

            if (
                velocidade_x < 0
                and bola.left <= raquete_1.left + raquete_1.width
                and bola.left + bola.width >= raquete_1.left
                and bola.top + bola.height >= raquete_1.top
                and bola.top <= raquete_1.top + raquete_1.height
            ):

                # Coloca a bola do lado direito da raquete
                bola.left = raquete_1.left + raquete_1.width

                # Calcula o centro da bola
                centro_bola = bola.top + bola.height / 2

                # Calcula o centro da raquete
                centro_raquete = raquete_1.top + raquete_1.height / 2

                # Calcula a distância entre o centro da bola
                # e o centro da raquete
                diferenca = centro_bola - centro_raquete

                # Transforma essa diferença em velocidade vertical
                velocidade_y = diferenca / 9

                # Limita a velocidade vertical
                if velocidade_y > velocidade_max_y:
                    velocidade_y = velocidade_max_y

                if velocidade_y < -velocidade_max_y:
                    velocidade_y = -velocidade_max_y

                # Inverte a direção horizontal
                velocidade_x = -velocidade_x

                # Toca o som da raquete
                #await som_raquete.play()


            # =================================================
            # COLISÃO COM A RAQUETE 2
            # =================================================

            if (
                velocidade_x > 0
                and bola.left + bola.width >= raquete_2.left
                and bola.left <= raquete_2.left + raquete_2.width
                and bola.top + bola.height >= raquete_2.top
                and bola.top <= raquete_2.top + raquete_2.height
            ):

                # Coloca a bola do lado esquerdo da raquete
                bola.left = raquete_2.left - bola.width

                # Calcula o centro da bola
                centro_bola = bola.top + bola.height / 2

                # Calcula o centro da raquete
                centro_raquete = raquete_2.top + raquete_2.height / 2

                # Calcula a diferença entre os centros
                diferenca = centro_bola - centro_raquete

                # Define a velocidade vertical
                velocidade_y = diferenca / 9

                # Limita a velocidade vertical
                if velocidade_y > velocidade_max_y:
                    velocidade_y = velocidade_max_y

                if velocidade_y < -velocidade_max_y:
                    velocidade_y = -velocidade_max_y

                # Inverte a direção horizontal
                velocidade_x = -velocidade_x

                # Toca o som da raquete
                #await som_raquete.play()


            # =================================================
            # JOGADOR 2 MARCA PONTO
            # =================================================

            if bola.left < 0:

                # Acrescenta um ponto ao jogador 2
                pontos_2 += 1

                # Atualiza o texto do placar
                placar_2.value = str(pontos_2)

                # Toca o som do ponto
                #await som_ponto.play()

                # Reinicia a bola no centro
                bola.left = largura / 2 - bola.width / 2
                bola.top = altura / 2 - bola.height / 2

                # Faz a bola seguir para a direita
                velocidade_x = 5


            # =================================================
            # JOGADOR 1 MARCA PONTO
            # =================================================

            if bola.left > largura:

                # Acrescenta um ponto ao jogador 1
                pontos_1 += 1

                # Atualiza o texto do placar
                placar_1.value = str(pontos_1)

                # Toca o som do ponto
                #await som_ponto.play()

                # Reinicia a bola no centro
                bola.left = largura / 2 - bola.width / 2
                bola.top = altura / 2 - bola.height / 2

                # Faz a bola seguir para a esquerda
                velocidade_x = -5


            # =================================================
            # ATUALIZA A BOLA
            # =================================================

            bola.update()

            # Atualiza os placares
            placar_1.update()
            placar_2.update()


            # =================================================
            # AGUARDA 16 MILISSEGUNDOS
            # =================================================

            await asyncio.sleep(0.016)


    # ============================================================
    # CAMPO DO JOGO
    # ============================================================

    campo = ft.Stack(

        width=largura,
        height=altura,

        controls=[

            # ----------------------------------------------------
            # PLACAR 1
            # ----------------------------------------------------

            ft.Container(
                content=placar_1,
                left=largura / 2 - 80,
                top=20
            ),


            # ----------------------------------------------------
            # PLACAR 2
            # ----------------------------------------------------

            ft.Container(
                content=placar_2,
                left=largura / 2 + 50,
                top=20
            ),


            # ----------------------------------------------------
            # LINHA CENTRAL
            # ----------------------------------------------------

            ft.Container(
                content=linha_central,
                left=largura / 2 - 2,
                top=0
            ),


            # ----------------------------------------------------
            # RAQUETE 1
            # ----------------------------------------------------

            raquete_1,


            # ----------------------------------------------------
            # RAQUETE 2
            # ----------------------------------------------------

            raquete_2,


            # ----------------------------------------------------
            # BOLA
            # ----------------------------------------------------

            bola,


            # ----------------------------------------------------
            # ÁREA DE TOQUE 1
            # ----------------------------------------------------

            area_toque_1,


            # ----------------------------------------------------
            # ÁREA DE TOQUE 2
            # ----------------------------------------------------

            area_toque_2
        ]
    )


    # ============================================================
    # BORDA DO CAMPO
    # ============================================================

    campo_com_borda = ft.Container(

        width=largura,
        height=altura,

        bgcolor=ft.Colors.BLACK,

        border=ft.Border.all(
            width=3,
            color=ft.Colors.WHITE
        ),

        content=campo
    )


    # ============================================================
    # ADICIONA O JOGO À PÁGINA
    # ============================================================

    page.add(

        ft.Row(
            controls=[campo_com_borda],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


    # ============================================================
    # INICIA A ANIMAÇÃO DA BOLA
    # ============================================================

    page.run_task(mover_bola)


# ================================================================
# INICIA O PROGRAMA
# ================================================================

ft.run(main)