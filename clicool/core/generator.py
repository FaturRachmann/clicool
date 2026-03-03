"""Advanced prompt generator with beautiful ANSI colors and effects."""

from typing import Optional
from .theme_loader import LayerConfig, ThemeConfig


class AdvancedPromptGenerator:
    """Generate beautiful shell prompts with advanced ANSI colors."""

    def generate(self, theme: ThemeConfig, shell_type: str, layers: Optional[list[LayerConfig]] = None) -> str:
        """Generate complete shell configuration."""
        
        if shell_type == 'bash':
            return self._generate_bash(theme)
        elif shell_type == 'zsh':
            return self._generate_zsh(theme)
        elif shell_type == 'fish':
            return self._generate_fish(theme)
        else:
            return self._generate_bash(theme)

    def _generate_bash(self, theme: ThemeConfig) -> str:
        """Generate beautiful bash prompt."""
        
        theme_name = theme.name.lower()
        
        # Cyberpunk theme - NEON COLORS
        if theme_name == 'cyberpunk':
            return '''
# CLICOOL Theme: cyberpunk
# Neon Cyberpunk Style

# Color codes
CYAN='\\[\\033[1;96m\\]'
MAGENTA='\\[\\033[1;95m\\]'
YELLOW='\\[\\033[1;93m\\]'
GREEN='\\[\\033[1;92m\\]'
RED='\\[\\033[1;91m\\]'
BLUE='\\[\\033[1;94m\\]'
WHITE='\\[\\033[1;97m\\]'
DIM='\\[\\033[2m\\]'
RESET='\\[\\033[0m\\]'

# Git branch
clicool_git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo -n "${DIM}(${GREEN}${branch}${DIM})${RESET}"
    fi
}

# Git status
clicool_git_status() {
    local status=$(git status --porcelain 2>/dev/null)
    if [ -n "$status" ]; then
        echo -n " ${RED}*${RESET}"
    fi
}

# Exit code
clicool_exit_code() {
    local code=$?
    if [ $code -ne 0 ]; then
        echo -n " ${RED}[${code}]${RESET}"
    fi
}

# Main prompt
PS1="${CYAN}\\u${WHITE}@${MAGENTA}\\h${WHITE}:${YELLOW}\\w${RESET}$(clicool_git_branch)$(clicool_git_status)\\n${GREEN}>${WHITE} ${RESET}"

# Terminal title
PROMPT_COMMAND='echo -ne "\\033]0;${USER}@${HOSTNAME}: ${PWD}\\007"'
'''

        # Matrix theme - GREEN HACKER
        elif theme_name == 'matrix':
            return '''
# CLICOOL Theme: matrix
# Hacker Green Style

# Color codes
GREEN='\\[\\033[1;92m\\]'
DARK_GREEN='\\[\\033[0;32m\\]'
BLACK='\\[\\033[0;30m\\]'
DIM='\\[\\033[2m\\]'
RESET='\\[\\033[0m\\]'

# Git branch
clicool_git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo -n "${DIM}[${GREEN}${branch}${DIM}]${RESET}"
    fi
}

# Main prompt
PS1="${GREEN}\\u${DIM}@${GREEN}\\h${DIM}:${GREEN}\\w${RESET}$(clicool_git_branch)\\n${GREEN}$${RESET} "
'''

        # Retro theme - AMBER
        elif theme_name == 'retro':
            return '''
# CLICOOL Theme: retro
# Amber CRT Style

# Color codes
AMBER='\\[\\033[1;93m\\]'
DARK_AMBER='\\[\\033[0;33m\\]'
DIM='\\[\\033[2m\\]'
RESET='\\[\\033[0m\\]'

# Git branch
clicool_git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo -n "${DIM}<${AMBER}${branch}${DIM}>${RESET}"
    fi
}

# Main prompt
PS1="${AMBER}\\u${DIM}@${AMBER}\\h${DIM}:${AMBER}\\w${RESET}$(clicool_git_branch)\\n${AMBER}>${RESET} "
'''

        # Minimal theme - CLEAN
        elif theme_name == 'minimal':
            return '''
# CLICOOL Theme: minimal
# Clean Minimal Style

# Color codes
GRAY='\\[\\033[90m\\]'
BLUE='\\[\\033[1;34m\\]'
RESET='\\[\\033[0m\\]'

# Git branch
clicool_git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo -n "${GRAY} ±${BLUE}${branch}${RESET}"
    fi
}

# Main prompt
PS1="${GRAY}\\w${RESET}$(clicool_git_branch)\\n${GRAY}❯${RESET} "
'''

        # DevOps theme - PROFESSIONAL
        elif theme_name == 'devops' or theme_name == 'devops pro':
            return '''
# CLICOOL Theme: devops
# DevOps Professional Style

# Color codes
CYAN='\\[\\033[1;96m\\]'
ORANGE='\\[\\033[1;38;5;208m\\]'
GREEN='\\[\\033[1;92m\\]'
PINK='\\[\\033[1;95m\\]'
BLUE='\\[\\033[1;94m\\]'
DIM='\\[\\033[2m\\]'
RESET='\\[\\033[0m\\]'

# Git branch
clicool_git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo -n " ${GREEN}[${branch}]${RESET}"
    fi
}

# Kubernetes context
clicool_k8s() {
    local ctx=$(kubectl config current-context 2>/dev/null)
    if [ -n "$ctx" ]; then
        echo -n " ${PINK}[K8S:${ctx}]${RESET}"
    fi
}

# Docker containers
clicool_docker() {
    local count=$(docker ps --format '{{.ID}}' 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
        echo -n " ${BLUE}[D:${count}]${RESET}"
    fi
}

# AWS profile
clicool_aws() {
    if [ -n "$AWS_PROFILE" ]; then
        echo -n " ${ORANGE}[AWS:${AWS_PROFILE}]${RESET}"
    elif [ -n "$AWS_DEFAULT_PROFILE" ]; then
        echo -n " ${ORANGE}[AWS:${AWS_DEFAULT_PROFILE}]${RESET}"
    fi
}

# Main prompt
PS1="${CYAN}\\u${DIM}@${CYAN}\\h${DIM}:${ORANGE}\\w${RESET}$(clicool_git_branch)$(clicool_k8s)$(clicool_docker)$(clicool_aws)\\n${CYAN}>${RESET} "
'''

        # Default theme
        else:
            return '''
# CLICOOL Theme: default
# Clean Default Style

GREEN='\\[\\033[1;32m\\]'
BLUE='\\[\\033[1;34m\\]'
DIM='\\[\\033[2m\\]'
RESET='\\[\\033[0m\\]'

clicool_git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    [ -n "$branch" ] && echo -n " (${branch})"
}

PS1="${GREEN}\\u@\\h${DIM}:${BLUE}\\w${RESET}$(clicool_git_branch)\\n\\$ "
'''

    def _generate_zsh(self, theme: ThemeConfig) -> str:
        """Generate beautiful zsh prompt."""
        
        theme_name = theme.name.lower()
        
        if theme_name == 'cyberpunk':
            return '''
# CLICOOL Theme: cyberpunk (zsh)

autoload -U colors && colors
setopt PROMPT_SUBST

git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo "%{$fg_bold[green]%}($branch)%{$reset_color%}"
    fi
}

PROMPT='%{$fg_bold[cyan]%}⚡ %n%{$reset_color%}@%{$fg_bold[magenta]%}%m%{$reset_color%}:%{$fg_bold[yellow]%}%~%{$reset_color%}$(git_branch)
%{$fg_bold[green]%}λ %{$reset_color%}'
'''
        elif theme_name == 'matrix':
            return '''
# CLICOOL Theme: matrix (zsh)

autoload -U colors && colors
setopt PROMPT_SUBST

git_branch() {
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    [ -n "$branch" ] && echo "%{$fg_bold[green]%}[$branch]%{$reset_color%}"
}

PROMPT='%{$fg_bold[green]%}%n@%m:%~$(git_branch)
$%{$reset_color%} '
'''
        else:
            return self._generate_bash(theme)

    def _generate_fish(self, theme: ThemeConfig) -> str:
        """Generate beautiful fish prompt."""
        
        return '''
# CLICOOL Theme: fish

function fish_prompt
    set -l last_status $status
    
    # Colors
    set -g fish_color_cwd blue
    set -g fish_color_command green
    set -g fish_color_comment cyan
    
    # Git branch
    set -l branch (git rev-parse --abbrev-ref HEAD 2>/dev/null)
    
    # Prompt
    echo -n "\\e[1;36m⚡ $USER\\e[0m@"
    echo -n "\\e[1;35m"(hostname)"\\e[0m:"
    echo -n "\\e[1;33m"(pwd)"\\e[0m"
    
    if [ -n "$branch" ]
        echo -n " \\e[1;32m($branch)\\e[0m"
    end
    
    echo ""
    echo -n "\\e[1;32mλ \\e[0m"
end
'''


__all__ = ["AdvancedPromptGenerator"]
