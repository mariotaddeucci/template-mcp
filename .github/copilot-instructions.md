# GitHub Copilot Instructions

## Project Overview
This project is a secure MCP (Model Context Protocol) server using FastMCP and Eunomia Authorization. It will become public, so follow security and documentation best practices.

## Package Management
- **Use uv**: Use `uv` as the package manager for all Python dependencies and tool installations
- **Python Version**: Requires Python >= 3.12 as specified in pyproject.toml
- **Ruff**: Use Ruff as the official formatter and linter for code quality and consistency
- **Taskipy**: Use Taskipy with uv for task automation via `uv run task <task-name>`

## Development Tools

### Code Quality
- **Ruff as Formatter**: Use `uv run ruff format` to format code according to project standards
- **Ruff as Linter**: Use `uv run ruff check` to lint code and catch potential issues
- **Pre-commit integration**: Ruff should be configured to run before commits for consistent code quality

### Task Automation
- **Taskipy integration**: Use Taskipy for common development tasks
- **Task execution**: Run tasks using `uv run task <task-name>` format
- **Common tasks**: Examples include `uv run task lint`, `uv run task format`, `uv run task test`
- **Custom tasks**: Define project-specific tasks in pyproject.toml under `[tool.taskipy.tasks]`

## Workflow and Task Management

### Pre-Task Checklist
Before starting tasks from `./Task.md`:
1. Check for existing approved PRs related to your intended work
2. Review open issues to avoid duplication of effort
3. If approved PRs exist, perform squash merge using GitHub MCP tools
4. Update local branch with latest changes from main branch

### Task Execution Rules
- **One task at a time**: Execute only one task from `./Task.md` at a time
- **Complete verification**: Ensure all steps are successfully completed before marking task as done
- **Use GitHub MCP**: Utilize GitHub MCP tools for opening issues and pull requests

## Git Workflow

### Branch Management
- **Never commit directly to main/master**: Always create separate branches for features or fixes
- **Branch naming**: Use descriptive branch names (e.g., `feat/setup-mcp-server`, `fix/auth-middleware`)
- **Pull requests required**: All changes must go through PR review process

### Commit Conventions
Follow conventional commits format with English messages:

**Format**: `<type>(<scope>): <description>`

**Types**:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(auth): add Eunomia middleware integration
fix(config): resolve environment variable loading issue
docs(api): update FastMCP tool documentation
test(security): add authorization policy tests
```

**Commit Guidelines**:
- Keep commits small and focused on single changes
- Use clear, descriptive English messages
- Make meaningful commits that represent functional changes
- Avoid empty or unnecessary commits

### Pull Request Standards
- **Clear descriptions**: Explain changes made and reasoning
- **Request reviews**: Always request review before merging
- **Squash merge**: Use squash merge to maintain clean commit history on main branch

## Language and Documentation Standards

### Code and Technical Content
- **English only**: All code, comments, docstrings, and commit messages must be in English
- **Global audience**: Ensure code is understandable to international developers
- **Documentation**: Maintain comprehensive documentation with examples

### Issues and PRs
- **Portuguese allowed**: Since this is a Brazilian project, issues and PRs can be written in Portuguese
- **Clear communication**: Use the language that best communicates the issue or change

## Security and Best Practices
- **Public repository**: Follow security best practices as this will be a public project
- **No sensitive data**: Never commit secrets, API keys, or sensitive information
- **Audit trail**: Ensure all changes are traceable through proper Git workflow
- **Testing**: Maintain test coverage and validate security implementations

## MCP-Specific Guidelines
- **FastMCP framework**: Use FastMCP as the base framework for MCP server implementation
- **Eunomia Authorization**: Implement granular access control using Eunomia Authorization system
- **JSON policies**: Configure authorization policies using JSON format
- **Audit logging**: Implement comprehensive logging for security auditing