````markdown
# GitHub Copilot Task Execution Prompt

## 🎯 **Objetivo Geral**
Implementar a primeira tarefa pendente do projeto MCP Secure Server: **Setup e Configuração Inicial**, especificamente a inicialização do projeto com uv e configuração do `pyproject.toml`.

## 📋 **Tarefa Específica a Executar**
**Inicializar projeto com uv**: `uv init mcp-secure-server` e configurar `pyproject.toml` com todas as dependências necessárias para o desenvolvimento do servidor MCP seguro com Eunomia Authorization.

## 🔍 **Contexto do Projeto**
- **Projeto**: Servidor MCP (Model Context Protocol) seguro com FastMCP e Eunomia Authorization
- **Framework Stack**: FastMCP + Eunomia Authorization + Pydantic + pytest
- **Gerenciador de Pacotes**: uv (conforme instruções do projeto)
- **Foco**: Controle de acesso granular através do Eunomia - o sistema oficial de autorização do FastMCP

## 📦 **Dependências Requeridas**

### Core Dependencies
```
fastmcp>=0.1.0              # Framework base para servidor MCP
eunomia-mcp                 # Sistema oficial de autorização do FastMCP
pydantic>=2.0.0             # Validação de dados e schemas
python-dotenv               # Gerenciamento de variáveis de ambiente
```

### Testing & Quality
```
pytest>=7.0.0               # Framework de testes
pytest-asyncio             # Testes assíncronos para FastMCP
pytest-cov                 # Cobertura de testes
```

### Logging & Monitoring
```
loguru                      # Logging estruturado para auditoria
structlog                   # Logging estruturado alternativo (conforme Task.md)
```

### Development Dependencies
```
black                      # Formatação de código
isort                      # Organização de imports
flake8                     # Linting
mypy                       # Type checking
pre-commit                 # Hooks de commit
```

## 📁 **Estrutura de Diretórios a Criar**
```
src/
├── mcp_secure_server/
│   ├── __init__.py
│   ├── core/
│   ├── models/
│   ├── tools/
│   └── config/
tests/
├── unit/
├── integration/
└── security/
docs/
├── api/
└── guides/
configs/
├── development.env
├── production.env
└── test.env
examples/
└── client_examples/
```

## 🎯 **Tarefas Específicas a Executar**

### 1. Configurar pyproject.toml
- [ ] Atualizar `[project]` com metadados corretos
- [ ] Adicionar todas as dependências listadas acima
- [ ] Configurar `[project.optional-dependencies]` para dev/test
- [ ] Definir `[build-system]` usando hatchling
- [ ] Configurar `[tool.pytest.ini_options]`
- [ ] Configurar `[tool.black]`, `[tool.isort]`, `[tool.mypy]`

### 2. Verificar Instalação
- [ ] Executar `uv sync` para instalar dependências
- [ ] Verificar se todas as dependências foram instaladas corretamente
- [ ] Testar import das principais bibliotecas

## 📝 **Critérios de Sucesso**
- ✅ `pyproject.toml` configurado com todas as dependências
- ✅ Estrutura de diretórios criada conforme especificação
- ✅ `uv sync` executa sem erros
- ✅ Imports das principais bibliotecas funcionam
- ✅ Ferramentas de desenvolvimento configuradas

## 🚨 **Restrições e Cuidados**
- **USE APENAS UV**: Não usar pip, poetry ou outros gerenciadores
- **Uma tarefa por vez**: Foque apenas na configuração inicial
- **Valide cada passo**: Confirme que cada comando foi executado com sucesso
- **Mantenha compatibilidade**: Use versões estáveis das dependências

## 📋 **Exemplo de pyproject.toml Base**
```toml
[project]
name = "mcp-secure-server"
version = "0.1.0"
description = "Servidor MCP seguro com FastMCP e Eunomia Authorization - controle de acesso granular com políticas JSON dinâmicas"
authors = [
    {name = "Your Name", email = "your.email@domain.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
keywords = ["mcp", "fastmcp", "eunomia", "authorization", "security", "server"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "fastmcp>=0.1.0",
    "eunomia-mcp",
    "pydantic>=2.0.0",
    "python-dotenv",
    "loguru",
]

[project.optional-dependencies]
dev = [
    "black",
    "isort",
    "flake8",
    "mypy",
    "pre-commit",
]
test = [
    "pytest>=7.0.0",
    "pytest-asyncio",
    "pytest-cov",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 🔄 **Próximos Passos (NÃO EXECUTAR AGORA)**
Após completar esta tarefa, a próxima será:
- **Instalar dependências base**: `uv add fastmcp eunomia-mcp pydantic pytest pytest-asyncio`
- **Setup servidor Eunomia**: Rodar servidor Eunomia via Docker: `docker run -d -p 8000:8000 ttommitt/eunomia-server:latest`
- **Configurar estrutura de diretórios**: Criar `src/`, `tests/`, `docs/`, `configs/` e `examples/`
- **Setup de ambiente**: Configurar variáveis de ambiente para desenvolvimento, teste e produção

## 💡 **Dicas de Implementação**
1. **Comece simples**: Configure primeiro as dependências core (fastmcp, eunomia-mcp, pydantic)
2. **Valide incrementalmente**: Teste a instalação a cada grupo de dependências
3. **Foque no Eunomia**: Este é o sistema oficial de autorização do FastMCP
4. **Documente mudanças**: Comente escolhas importantes no pyproject.toml

---

**🤖 Copilot Instructions**: Execute apenas a tarefa especificada acima. Não prossiga para outras tarefas até que esta esteja 100% completa e validada. Use `uv` conforme as instruções do projeto e foque na integração com Eunomia Authorization.
