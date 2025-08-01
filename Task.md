# Checklist: Servidor MCP Seguro com FastMCP e Eunomia Authorization

## Plano

**Resumo do plano**: Desenvolver um servidor MCP (Model Context Protocol) robusto e seguro utilizando FastMCP como framework base, implementando controle de acesso granular através do **Eunomia Authorization** - o sistema oficial de autorização do FastMCP, com políticas JSON dinâmicas, logging de auditoria e testes abrangentes.

## Definição de Completo

- [ ] **Servidor MCP funcional**: Servidor rodando com FastMCP, respondendo a tools básicas e gerenciando recursos adequadamente
- [ ] **Sistema Eunomia implementado**: Servidor Eunomia rodando e middleware integrado ao FastMCP
- [ ] **Políticas de autorização configuradas**: Políticas JSON definidas e validadas para controle granular de acesso
- [ ] **Cobertura de testes ≥ 80%**: Testes unitários, integração e segurança cobrindo cenários críticos
- [ ] **Documentação completa**: README, API docs e guias de deployment com exemplos práticos

## Todo List

### Setup e Configuração Inicial
- [ ] **Inicializar projeto com uv**: `uv init mcp-secure-server` e configurar pyproject.toml com dependências
- [ ] **Instalar dependências base**: `uv add fastmcp eunomia-mcp pydantic pytest pytest-asyncio`
- [ ] **Setup servidor Eunomia**: Rodar servidor Eunomia via Docker: `docker run -d -p 8000:8000 ttommitt/eunomia-server:latest`
- [ ] **Configurar estrutura de diretórios**: Criar `src/`, `tests/`, `docs/`, `configs/` e `examples/`
- [ ] **Setup de ambiente**: Configurar variáveis de ambiente para desenvolvimento, teste e produção

### Desenvolvimento do Core MCP
- [ ] **Implementar servidor FastMCP básico**: Criar servidor com tool "hello" simples funcionando
- [ ] **Integrar middleware Eunomia**: Adicionar `EunomiaMcpMiddleware()` ao servidor FastMCP em uma linha
- [ ] **Definir modelos Pydantic**: Schemas para dados de negócio com validações robustas
- [ ] **Criar sistema de configuração**: Config manager usando Pydantic Settings para diferentes ambientes
- [ ] **Implementar logging estruturado**: Setup com loguru/structlog para auditoria e debugging

### Sistema de Autorização com Eunomia
- [ ] **Configurar políticas de acesso**: Usar `eunomia-mcp init` para criar arquivo de políticas JSON
- [ ] **Definir roles e permissões**: Criar políticas para diferentes níveis (admin, user, guest) no arquivo JSON
- [ ] **Validar políticas**: Executar `eunomia-mcp validate mcp_policies.json` para verificar configuração
- [ ] **Deploy das políticas**: Usar `eunomia-mcp push mcp_policies.json` para aplicar no servidor Eunomia
- [ ] **Configurar identificação de agentes**: Setup de headers `X-Agent-ID`, `X-User-ID`, `User-Agent` ou `Authorization`

### Tools e Resources Seguros
- [ ] **Desenvolver tools com diferentes níveis**: Tools que demonstrem acesso read, write e admin
- [ ] **Implementar sanitização de inputs**: Validação rigorosa de parâmetros de entrada em todas as tools
- [ ] **Criar resources protegidos**: Recursos que são filtrados pelo middleware baseado nas políticas
- [ ] **Testar filtragem automática**: Verificar que `tools/list`, `resources/list` e `prompts/list` filtram corretamente
- [ ] **Testar bloqueio de execução**: Confirmar que `tools/call`, `resources/read` e `prompts/get` são bloqueados quando não autorizados

### Testes e Qualidade
- [ ] **Testes unitários do core**: Cobertura das funções principais e middleware Eunomia
- [ ] **Testes de integração MCP**: Simulação de cliente MCP real conectando ao servidor com diferentes identidades
- [ ] **Testes de políticas**: Verificar que políticas são aplicadas corretamente em cenários diversos
- [ ] **Testes de segurança**: Tentativas de bypass de autorização e edge cases de segurança
- [ ] **Setup de CI/CD**: GitHub Actions com testes automatizados, linting e security scan

### Documentação e Deploy
- [ ] **Documentar API e usage**: README detalhado com exemplos de uso e configuração do Eunomia
- [ ] **Criar guia de políticas**: Documentação sobre como criar e gerenciar políticas JSON no Eunomia
- [ ] **Setup de deploy**: Docker Compose com FastMCP server + Eunomia server + configurações de segurança
- [ ] **Exemplo de client**: Script demonstrando conexão com diferentes identidades de agente
- [ ] **Guia de troubleshooting**: Documentação para debugging de problemas de autorização

### Monitoramento e Manutenção
- [ ] **Implementar health checks**: Endpoints para verificar status do servidor FastMCP e Eunomia
- [ ] **Configurar alertas**: Monitoramento de falhas de autorização e violations de políticas
- [ ] **Logs de auditoria**: Sistema completo de auditoria fornecido automaticamente pelo Eunomia
- [ ] **Backup de políticas**: Procedimentos para versionamento e backup dos arquivos de política JSON

---

## Notas Técnicas

**Framework Stack**: FastMCP + Eunomia Authorization + Pydantic + pytest
**Autorização**: Eunomia middleware oficial com políticas JSON dinâmicas e auditoria automática
**Deploy**: Docker Compose (FastMCP + Eunomia) + environment variables + secrets management
**Monitoramento**: Structured logging + health checks + audit logs do Eunomia

## Recursos do Eunomia

**Filtragem Automática**: O middleware filtra automaticamente resultados de listing (`tools/list`, `resources/list`, `prompts/list`) baseado nas políticas
**Firewall de Execução**: Bloqueia operações de execução (`tools/call`, `resources/read`, `prompts/get`) não autorizadas
**Identificação de Agentes**: Suporte automático para headers `X-Agent-ID`, `X-User-ID`, `User-Agent`, `Authorization`
**Auditoria Completa**: Log automático de todas as tentativas de acesso e violações de política
