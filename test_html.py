"""
Testes automatizados para validar o index.html
Estes testes simulam o que um pipeline de CI/CD faria
antes de permitir o deploy do codigo.
"""
import re
import sys
 
 
def ler_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()
 
 
def test_tags_fechadas(html):
    """Verifica se todas as tags <p> abertas estao fechadas."""
    abertas = len(re.findall(r"<p[ >]", html, re.IGNORECASE))
    fechadas = len(re.findall(r"</p>", html, re.IGNORECASE))
    assert abertas == fechadas, (
        f"ERRO: {abertas} tag(s) <p> aberta(s), mas so {fechadas} fechada(s). "
        f"Falta fechar {abertas - fechadas} tag(s)."
    )
 
 
def test_links_tem_url(html):
    """Verifica se nenhum link <a href=""> esta com URL vazia."""
    links_vazios = re.findall(r'<a\s[^>]*href\s*=\s*""\s*[^>]*>', html, re.IGNORECASE)
    assert len(links_vazios) == 0, (
        f"ERRO: {len(links_vazios)} link(s) com href vazio encontrado(s). "
        f"Todo link precisa apontar para uma URL valida."
    )
 
 
def test_imagens_tem_src_valido(html):
    """Verifica se as imagens referenciam arquivos existentes (nao vazios)."""
    imgs = re.findall(r'<img\s[^>]*src\s*=\s*"([^"]*)"', html, re.IGNORECASE)
    for src in imgs:
        assert src.strip() != "", "ERRO: Tag <img> com src vazio."
        assert not src.endswith("-que-nao-existe.png"), (
            f"ERRO: Imagem '{src}' parece ser um arquivo inexistente."
        )
 
 
def test_titulo_presente(html):
    """Verifica se a pagina tem um <title> definido."""
    titulo = re.search(r"<title>(.+?)</title>", html, re.IGNORECASE)
    assert titulo is not None, "ERRO: A pagina nao possui tag <title>."
    assert titulo.group(1).strip() != "", "ERRO: O <title> esta vazio."
 
 
# ──────────────────────────────────────────────
# Execucao dos testes
# ──────────────────────────────────────────────
if __name__ == "__main__":
    arquivo = "index.html"
    html = ler_arquivo(arquivo)
 
    testes = [
        ("Tags <p> fechadas corretamente", test_tags_fechadas),
        ("Links possuem URL valida", test_links_tem_url),
        ("Imagens com src valido", test_imagens_tem_src_valido),
        ("Titulo da pagina presente", test_titulo_presente),
    ]
 
    falhas = 0
    print("=" * 55)
    print("  EXECUTANDO TESTES DE QUALIDADE DO HTML")
    print("=" * 55)
 
    for nome, funcao in testes:
        try:
            funcao(html)
            print(f"  PASSOU  -> {nome}")
        except AssertionError as e:
            print(f"  FALHOU  -> {nome}")
            print(f"           {e}")
            falhas += 1
 
    print("=" * 55)
 
    if falhas > 0:
        print(f"\n  RESULTADO: {falhas} teste(s) falharam!")
        print("  O deploy NAO deve ser feito.\n")
        sys.exit(1)
    else:
        print("\n  RESULTADO: Todos os testes passaram!")
        print("  O deploy pode prosseguir.\n")
        sys.exit(0)
