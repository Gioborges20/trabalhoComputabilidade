from fasthtml.common import FastHTML, serve
app = FastHTML()

def gerar_titulo(titulo, subtitulo):
    return f"""
    <html>
        <head>
            <title>{titulo}</title>
        </head>
        <body>
            <h1>{titulo}</h1>
            <h2>{subtitulo}</h2>
        </body>
    </html>
    """