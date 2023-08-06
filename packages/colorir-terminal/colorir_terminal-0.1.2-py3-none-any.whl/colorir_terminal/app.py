# color-terminal para colorir algumas palavras no seu terminal quando executar seu codigo.
import colorterminal

def color(cor , texto):
    cor = cor.upper()   # Transformar a string toda em Maiusculo

    if cor == 'RED':
        return colorterminal.ColorText.RED + texto
    elif cor == 'BLACK':
        return colorterminal.ColorText.BLACK + texto
    elif cor == 'GREEN':
        return colorterminal.ColorText.GREEN + texto
    elif cor == 'YELLOW':
        return colorterminal.ColorText.YELLOW + texto
    elif cor == 'PURPLE':
        return colorterminal.ColorText.PURPLE + texto
    elif cor == 'BEREZOVY':
        return colorterminal.ColorText.BEREZOVY + texto
    elif cor == 'WHITE':
        return colorterminal.ColorText.WHITE + texto
    else:
        return colorterminal.ColorText.RED + "{ Cor Indefinida }"


def efeitos(tipo, texto):
    tipo.upper()
    if tipo == 'RESET':
        return colorterminal.EffectsText.RESET + texto
    if tipo == 'FATTY':
        return colorterminal.EffectsText.FATTY + texto
    if tipo == 'FADED':
        return colorterminal.EffectsText.FADED + texto
    if tipo == 'ITALICS':
        return colorterminal.EffectsText.ITALICS + texto
    if tipo == 'EMPHATIC':
        return colorterminal.EffectsText.EMPHATIC + texto
    if tipo == 'RARE_BLINKING':
        return colorterminal.EffectsText.RARE_BLINKING + texto
    if tipo == 'FREQUENT_BLINKING':
        return colorterminal.EffectsText.FREQUENT_BLINKING + texto
    if tipo == 'CHANGING_BACKGROUND_COLOR':
        return colorterminal.EffectsText.CHANGING_BACKGROUND_COLOR + texto
    else:
        return colorterminal.ColorText.RED + "{ Efeito Indefinido }"


def background(tipo, texto):
    tipo.upper()

    if tipo == 'BLACK':
        return colorterminal.ColorBackground.BLACK + texto
    elif tipo == 'RED':
        return colorterminal.ColorBackground.RED + texto
    elif tipo == 'GREEN':
        return colorterminal.ColorBackground.GREEN + texto
    elif tipo == 'YELLOW':
        return colorterminal.ColorBackground.YELLOW + texto
    elif tipo == 'BLUE':
        return colorterminal.ColorBackground.BLUE + texto
    elif tipo == 'PURPLE':
        return colorterminal.ColorBackground.PURPLE + texto
    elif tipo == 'BEREZOVY':
        return colorterminal.ColorBackground.BEREZOVY + texto
    elif tipo == 'WHITE':
        return colorterminal.ColorBackground.WHITE + texto
    else:
        return colorterminal.ColorText.RED + "{ Background Indefinido }"