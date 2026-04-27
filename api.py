from fastapi import FastAPI
from pydantic import BaseModel

try:
    from kira.app import KiraApp
except Exception as e:
    KiraApp = None
    erro_importacao = str(e)


app = FastAPI(
    title="KIRA API",
    description="Knowledge Intelligence & Research Assistant",
    version="1.0.0"
)


class PesquisaRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "status": "online",
        "assistente": "KIRA",
        "mensagem": "KIRA API está funcionando."
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "servico": "KIRA API"
    }


@app.post("/pesquisar")
def pesquisar(data: PesquisaRequest):
    pergunta = data.query.strip()

    if not pergunta:
        return {
            "status": "erro",
            "mensagem": "A pergunta não pode estar vazia."
        }

    try:
        if KiraApp is None:
            return {
                "status": "erro",
                "mensagem": "Erro ao importar KiraApp.",
                "detalhe": erro_importacao
            }

        kira = KiraApp()

        if hasattr(kira, "processar"):
            resposta = kira.processar(pergunta)

        elif hasattr(kira, "responder"):
            resposta = kira.responder(pergunta)

        elif hasattr(kira, "pesquisar"):
            resposta = kira.pesquisar(pergunta)

        else:
            resposta = (
                "KIRA recebeu sua pergunta, mas ainda não encontrei "
                "um método processar(), responder() ou pesquisar() dentro da classe KiraApp."
            )

        return {
            "status": "ok",
            "pergunta": pergunta,
            "resposta": resposta
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": "Erro interno ao processar a pergunta.",
            "detalhe": str(e)
        }