# 🔄 Prompt de Automação - Gerenciamento Completo de PRs

Este prompt implementa um fluxo completo de verificação e organização de Pull Requests, garantindo que o repositório mantenha um estado limpo e organizado.

## 🎯 Objetivos do Fluxo

### 1. **Análise Completa do Estado**
- Verificar PRs pendentes, aprovados e já mergeados
- Identificar branches locais e remotas órfãs
- Avaliar issues abertas relacionadas
- Mapear dependências entre tarefas

### 2. **Limpeza e Organização**
- Fazer squash merge de PRs aprovados
- Remover branches já mergeadas (local e remoto)
- Sincronizar branch local com main atualizada
- Limpar referências obsoletas

### 3. **Validação de Integridade**
- Garantir que todas as branches locais tenham PRs correspondentes
- Verificar se não há trabalho perdido ou não rastreado
- Confirmar sincronização completa com repositório remoto

## 🔧 Fluxo de Execução

### **Etapa 1: Diagnóstico Completo**
```prompt
1. Liste todas as notificações GitHub do repositório
2. Verifique PRs em todos os estados (open, closed, merged)
3. Compare branches locais vs remotas
4. Identifique issues abertas relacionadas
5. Analise dependências entre PRs/issues
```

### **Etapa 2: Processamento de PRs Aprovados**
```prompt
Para cada PR aprovado encontrado:
1. Verificar se todos os checks passaram
2. Executar squash merge para manter histórico limpo
3. Aguardar confirmação de merge bem-sucedido
4. Marcar notificação como lida
```

### **Etapa 3: Limpeza de Branches**
```prompt
Para cada branch já mergeada:
1. Identificar se há branch local correspondente
2. Verificar se branch remota ainda existe
3. Deletar branch local: `git branch -d <branch-name>`
4. Deletar branch remota: `git push origin --delete <branch-name>`
5. Executar cleanup: `git remote prune origin`
```

### **Etapa 4: Atualização Local**
```prompt
1. Checkout para main: `git checkout main`
2. Pull das últimas alterações: `git pull origin main`
3. Verificar se branch atual está limpa
4. Confirmar sincronização completa
```

### **Etapa 5: Validação Final**
```prompt
1. Listar branches locais restantes
2. Verificar se todas têm PRs correspondentes
3. Confirmar se não há trabalho não commitado
4. Validar estado limpo do repositório
```

## ✅ Critérios de Sucesso

- **✅ PRs Organizados**: Todos os PRs aprovados foram mergeados
- **✅ Branches Limpas**: Não há branches órfãs locais ou remotas
- **✅ Main Atualizada**: Branch local main sincronizada com origin
- **✅ Trabalho Preservado**: Nenhum trabalho foi perdido no processo
- **✅ Estado Limpo**: Repository em estado limpo para novo desenvolvimento

## 🚨 Verificações de Segurança

### **Antes de Deletar Branches:**
- Confirmar que branch foi realmente mergeada
- Verificar se não há commits únicos não integrados
- Garantir que não há trabalho local não pushado

### **Antes de Squash Merge:**
- Validar que PR passou em todos os checks
- Confirmar que não há conflitos pendentes
- Verificar se descrição do PR está adequada

## 🔄 Exemplo de Execução

```bash
# Estado inicial detectado:
PRs abertos: #5 (chore/update-pyproject-configuration)
PRs mergeados: #1, #2, #3, #4
Branches órfãs: feat/add-copilot-pr-prompt, feature/reorganize-copilot-structure

# Ações executadas:
1. ✅ Manter PR #5 aberto (em desenvolvimento)
2. ✅ Deletar branches de PRs já mergeados
3. ✅ Atualizar main local
4. ✅ Validar estado final limpo
```

## 📋 Checklist de Execução

- [ ] Analisar todas as notificações GitHub
- [ ] Identificar PRs em cada estado
- [ ] Processar PRs aprovados com squash merge
- [ ] Identificar e deletar branches órfãs
- [ ] Atualizar branch main local
- [ ] Validar que branches locais têm PRs correspondentes
- [ ] Confirmar estado limpo final
- [ ] Documentar ações executadas

---

**🎯 Resultado Esperado**: Repositório organizado, main atualizada, branches limpas, e estado pronto para novo desenvolvimento.
