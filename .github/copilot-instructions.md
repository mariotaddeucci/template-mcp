Utilize o uv como gerenciador de pacotes para instalar o Copilot CLI. O uv é uma ferramenta que facilita a instalação e o gerenciamento de pacotes no ambiente de desenvolvimento.
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