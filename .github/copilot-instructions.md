Utilize o uv como gerenciador de pacotes para instalar o Copilot CLI. O uv é uma ferramenta que facilita a instalação e o gerenciamento de pacotes no ambiente de desenvolvimento.
Todas asconfigurações de ferramentas devem ser feitas no arquivo `pyproject.toml` do projeto, que é o padrão para projetos Python modernos. Certifique-se de que todas as dependências necessárias estejam listadas corretamente nesse arquivo.
Utilize o ruff para linter e formatação de código, garantindo que o código esteja sempre limpo e seguindo as melhores práticas de estilo.
Utilize o pytest para testes unitários e de integração, garantindo que o código esteja sempre testado e funcionando corretamente.
Utilize o taskpi para gerenciar as tarefas do projeto, garantindo que todas as tarefas sejam rastreáveis e organizadas.
Execute sempre com o uv run para garantir que todas as dependências estejam instaladas e o ambiente esteja configurado corretamente antes de executar qualquer comando. ex uv run task `nome do alias no pyproject.toml`.
Antes de iniciar as tarefcas do ./Task.md, verifique se não há PRs já aprovados ou issues abertas relacionadas às tarefas que você pretende realizar. Isso ajuda a evitar duplicação de esforços e garante que você esteja trabalhando na versão mais atualizada do projeto. Se o PR estiver aprovado, faça um squash merge para manter o histórico de commits limpo e organizado na main branch (utilize o mcp do github para isso). Após tudo, atualize seu branch local com as últimas alterações da main branch para garantir que você esteja trabalhando com a versão mais recente do código.
Ao seguir as instruções do ./Task.md, ao executar uma task, apenas execute uma task por vez e antes de finalizar a task, certifique-se de que todos os passos foram concluídos com sucesso.
Esse projeto utiliza o github e se tornará publico, portanto, é importante seguir as melhores práticas de segurança e documentação.
utilize o MCP do github para abrir issues e pull requests, garantindo que todas as alterações sejam rastreáveis e revisadas adequadamente.
Nunca realizar alterações diretamente no branch principal (main/master). Sempre crie um branch separado para cada feature ou correção, e faça pull requests para revisão antes de mesclar as alterações.
Siga as convenções de commit:
- Use mensagens de commit claras e descritivas.
- Use o formato `feat(nova-funcionalidade):`, `fix(correção):`, `docs(documentação):`, `style(estilo):`, `refactor(refatoração):`, `test(teste):`, `chore(tarefas):` para categorizar os commits.
- Mantenha os commits pequenos e focados em uma única tarefa ou correção.

Nas branchs realize quantos commits forem necessários para concluir a tarefa, mas evite commits desnecessários ou vazios. Cada commit deve representar uma mudança significativa e funcional no código.
- Após concluir uma tarefa, faça um pull request para o branch principal, solicitando revisão e aprovação antes de mesclar as alterações.
Os pull requests devem ser claros e descritivos, explicando as alterações feitas e o motivo delas.
O commmit sempre deve ser feito em inglês, e as mensagens devem ser claras e descritivas, seguindo o padrão de commit do projeto.
A codebase e docstrings devem ser escritas em inglês, garantindo que sejam compreensíveis para uma audiência global.
Garanta documentação multilíngue, se necessário, mas o código e as mensagens de commit devem ser sempre em inglês.
O projeto é brasileiro então os PRs e issues podem ser abertos em português, mas o código e as mensagens de commit devem ser sempre em inglês.

## Fluxo de Desenvolvimento Completo

Quando solicitado a implementar mudanças ou melhorias no projeto, siga este fluxo estruturado:

### 1. Análise Inicial do Repositório
- **Verificar estado atual**: Use o MCP do GitHub para verificar PRs pendentes, issues abertas e notificações relacionadas ao projeto
- **Analisar mudanças**: Examine as modificações locais não commitadas usando ferramentas de diff
- **Verificar branch atual**: Confirme que está na branch principal (main) e atualizada
- **Revisar dependências**: Verifique se há atualizações necessárias no `pyproject.toml`

### 2. Planejamento e Organização
- **Identificar escopo**: Analise todas as modificações necessárias e agrupe por contexto/funcionalidade
- **Separar em temas**: Organize as mudanças em categorias lógicas para criar PRs separados:
  - Features novas
  - Correções de bugs
  - Melhorias de documentação
  - Refatorações
  - Atualizações de dependências
  - Configurações e setup

### 3. Execução por Branch/PR
Para cada grupo de mudanças identificado:

**a) Criação da Branch**
- Crie uma branch com nome descritivo seguindo o padrão: `tipo/descricao-curta`
  - Exemplos: `feat/user-authentication`, `fix/memory-leak`, `docs/api-documentation`, `refactor/database-layer`

**b) Implementação**
- Faça as modificações necessárias para o escopo específico
- Execute testes com `uv run pytest` para garantir qualidade
- Execute linting com `uv run ruff check` e formatação com `uv run ruff format`
- Realize quantos commits forem necessários, seguindo as convenções estabelecidas

**c) Abertura do Pull Request**
- Use o MCP do GitHub para criar o PR com:
  - Título claro e descritivo em português
  - Descrição detalhada explicando as mudanças e motivação
  - Referência a issues relacionadas, se houver
  - Labels apropriadas para categorização

### 4. Revisão e Merge
- Aguarde revisão (se aplicável) ou auto-aprove para projetos pessoais
- Use squash merge para manter histórico limpo na main branch
- Após merge, atualize branch local e delete branches remotas obsoletas

### 5. Verificação Final
- Confirme que todas as mudanças foram integradas corretamente
- Execute testes finais na main branch atualizada
- Verifique se não há conflitos ou issues pendentes

### Exemplo de Fluxo Prático:
```
Mudanças detectadas:
- Novas funções de API (feat/api-endpoints)
- Correção de bug na validação (fix/validation-error)
- Atualização da documentação (docs/update-readme)
- Refatoração do módulo de database (refactor/db-module)

Resultado: 4 branches + 4 PRs separados, cada um com escopo bem definido
```

Esta abordagem garante:
- **Rastreabilidade**: Cada mudança tem seu próprio contexto e histórico
- **Revisão focada**: PRs menores são mais fáceis de revisar
- **Rollback seguro**: Possibilidade de reverter mudanças específicas sem afetar outras
- **Organização**: Histórico limpo e bem documentado do projeto