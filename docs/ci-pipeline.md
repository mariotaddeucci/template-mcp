# GitHub Actions CI Pipeline

Este projeto utiliza GitHub Actions para automatizar a execução de todos os comandos de verificação através de `uv run task`. A pipeline está configurada para rodar verificações em paralelo para melhor performance.

## Workflows Configurados

### 1. `ci.yml` - Pipeline Principal
**Trigger:** Push e Pull Request para `main` e `develop`

Executa as seguintes verificações em paralelo:

#### Job: `code-quality`
- **Estratégia Matrix**: Executa `format-check` e `lint` em paralelo
- **Comandos**: 
  - `uv run task format-check` - Verifica formatação do código
  - `uv run task lint` - Executa linting com Ruff

#### Job: `security`
- **Comando**: `uv run task security` - Análise de segurança com Semgrep
- **Configuração especial**: Desabilita métricas do Semgrep para CI

#### Job: `tests`
- **Comando**: `uv run task test-cov` - Executa testes com cobertura
- **Upload**: Envia relatórios de cobertura para Codecov (opcional)

#### Job: `verify`
- **Dependências**: Aguarda todos os jobs anteriores
- **Função**: Verifica status final e falha se algum job anterior falhou

### 2. `pr-checks.yml` - Verificações Rápidas para PR
**Trigger:** Eventos de Pull Request

- **Foco**: Feedback rápido (timeout de 10 minutos)
- **Verificações**: `format-check`, `lint`, `test` (básico)
- **Informações**: Mostra estatísticas do PR (arquivos alterados, linhas, etc.)

### 3. `comprehensive.yml` - Suite Completa de Testes
**Trigger:** Manual (`workflow_dispatch`) e agendado (segunda-feira 6h UTC)

#### Jobs incluídos:
- **comprehensive-checks**: `uv run task pre-commit`
- **security-comprehensive**: `uv run task security-full`
- **test-coverage**: Testes com relatório detalhado
- **matrix-testing**: Testa em Python 3.12 e 3.13

### 4. `dependencies.yml` - Gerenciamento de Dependências
**Trigger:** Agendado (segunda-feira 8h UTC) e manual

- **Validação**: Verifica se `uv.lock` está atualizado
- **Auditoria**: Checa vulnerabilidades de segurança
- **Sincronização**: Valida ambiente sincronizado

## Configuração do Ambiente

Todos os workflows seguem o mesmo padrão:

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    version: "latest"

- name: Set up Python
  run: uv python install 3.12

- name: Install dependencies
  run: uv sync --all-extras
```

## Tasks Executados

Os seguintes comandos do `taskipy` são executados na CI:

| Task | Comando | Descrição |
|------|---------|-----------|
| `format-check` | `ruff format --check src tests` | Verifica formatação |
| `lint` | `ruff check src tests` | Análise estática |
| `security` | `semgrep --config=auto src/` | Varredura de segurança |
| `security-full` | `semgrep --config=p/security-audit --config=p/secrets --config=p/python src/` | Varredura completa |
| `test` | `pytest` | Testes básicos |
| `test-cov` | `pytest --cov=src --cov-report=html --cov-report=term-missing` | Testes com cobertura |
| `pre-commit` | Combinação de lint + format + security + test | Verificação completa |

## Paralelização

A pipeline é otimizada para execução paralela:

- **Code Quality**: `format-check` e `lint` executam simultaneamente via matrix strategy
- **Jobs independentes**: `security` e `tests` executam em paralelo
- **Matrix testing**: Testa múltiplas versões do Python simultaneamente

## Configurações Especiais

### Semgrep
- Métricas desabilitadas: `SEMGREP_SEND_METRICS: "off"`
- Configuração robusta para ambientes CI

### Codecov (Opcional)
- Upload automático de relatórios de cobertura
- Requer `CODECOV_TOKEN` configurado nos secrets do repositório

### Timeouts
- **PR Checks**: 10 minutos (feedback rápido)
- **Comprehensive**: 15 minutos (verificação completa)

## Como Executar Localmente

Para executar as mesmas verificações localmente:

```bash
# Verificação completa (equivalente ao pre-commit)
uv run task pre-commit

# Verificações individuais
uv run task format-check
uv run task lint
uv run task security
uv run task test-cov
```

## Troubleshooting

### Falha na Verificação de Formato
```bash
# Corrigir formatação automaticamente
uv run task format
```

### Falha no Linting
```bash
# Ver detalhes dos problemas
uv run task lint
```

### Falha nos Testes
```bash
# Executar testes com output detalhado
uv run task test -v
```

### Problemas de Dependências
```bash
# Resincronizar ambiente
uv sync --all-extras
```