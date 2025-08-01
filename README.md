# Template MCP

Servidor MCP seguro com FastMCP e Eunomia Authorization - controle de acesso granular com políticas JSON dinâmicas.

## ✅ Status do Setup Inicial

- [x] Projeto inicializado com uv
- [x] Dependências instaladas (fastmcp, eunomia-ai, eunomia-sdk, pydantic, pytest, pytest-asyncio)
- [x] Servidor Eunomia rodando via Docker
- [x] Estrutura de diretórios criada (src/, tests/, docs/, configs/, examples/)
- [x] Configuração de ambiente implementada
- [x] Build system configurado
- [x] Testes básicos funcionando

## 🚀 Quick Start

```bash
# 1. Instalar dependências
uv sync --all-extras

# 2. Iniciar servidor Eunomia
docker run -d -p 8000:8000 ttommitt/eunomia-server:latest

# 3. Executar aplicação básica
uv run python -m template_mcp.main

# 4. Executar testes
uv run pytest
```

## 📁 Estrutura do Projeto

```
template-mcp/
├── src/template_mcp/     # Código fonte principal
├── tests/                # Testes unitários e de integração
├── docs/                 # Documentação
├── configs/              # Arquivos de configuração
├── examples/             # Exemplos e scripts de demonstração
├── .env.*               # Arquivos de ambiente
└── pyproject.toml       # Configuração do projeto
```

## 🛠 Próximos Passos

Ver [Task.md](Task.md) para a lista completa de tarefas pendentes.
