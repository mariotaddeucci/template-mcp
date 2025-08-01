# GitHub Copilot Task Execution Prompt

## 🎯 **Objetivo Geral**
Implementar a primeira tarefa pendente do projeto MCP Secure Server: **Setup e Configuração Inicial**, especificamente a inicialização do projeto com uv e configuração do `pyproject.toml`.

## 📋 **Tarefa Específica a Executar**
**Inicializar projeto com uv**: Configurar `pyproject.toml` com todas as dependências necessárias para o desenvolvimento do servidor MCP seguro.

## 🔍 **Contexto do Projeto**
- **Projeto**: Servidor MCP (Model Context Protocol) seguro com FastMCP
- **Framework Stack**: FastMCP + Pydantic + JWT + pytest
- **Gerenciador de Pacotes**: uv (conforme instruções do projeto)
- **Foco**: Segurança, autenticação, autorização granular

## 📦 **Dependências Requeridas**

### Core Dependencies
```
fastmcp>=0.1.0              # Framework base para servidor MCP
pydantic>=2.0.0             # Validação de dados e schemas
python-jose[cryptography]   # JWT e autenticação
python-multipart            # Suporte a multipart forms
uvicorn[standard]           # ASGI server
```

### Security & Auth
```
passlib[bcrypt]             # Hashing de senhas
python-dotenv               # Gerenciamento de variáveis de ambiente
cryptography                # Operações criptográficas
```

### Logging & Monitoring
```
loguru                      # Logging estruturado e auditoria
prometheus-client           # Métricas e monitoramento
```

### Development Dependencies
```
pytest>=7.0.0               # Framework de testes
pytest-asyncio             # Testes assíncronos
pytest-cov                 # Cobertura de testes
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
│   ├── auth/
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
description = "Servidor MCP seguro com FastMCP e controle de acesso granular"
authors = [
    {name = "Your Name", email = "your.email@domain.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
keywords = ["mcp", "fastmcp", "security", "auth", "server"]
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
    # Core dependencies aqui
]

[project.optional-dependencies]
dev = [
    # Development dependencies aqui
]
test = [
    # Test dependencies aqui
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 🔄 **Próximos Passos (NÃO EXECUTAR AGORA)**
Após completar esta tarefa, a próxima será:
- **Instalar dependências base**: `uv add` das dependências principais
- **Configurar estrutura de diretórios**: Criar estrutura completa
- **Setup de ambiente**: Configurar variáveis de ambiente

## 💡 **Dicas de Implementação**
1. **Comece simples**: Configure primeiro as dependências core
2. **Valide incrementalmente**: Teste a instalação a cada grupo de dependências
3. **Use versões específicas**: Para dependências críticas de segurança
4. **Documente mudanças**: Comente escolhas importantes no pyproject.toml

---

**🤖 Copilot Instructions**: Execute apenas a tarefa especificada acima. Não prossiga para outras tarefas até que esta esteja 100% completa e validada. Use `uv` conforme as instruções do projeto.
