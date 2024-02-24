#!/bin/bash

###############################################################################

# Any shared and default aliases (terminal shortcuts) to be loaded with
# .bashrc go here.
# This is called and loaded with .bashrc
#
# Examples:
#    - alias ll="ls -la"

###############################################################################

alias zshconfig="vim ~/.bashrc"
alias vimconfig="vim ~/.vimrc"

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Change directory shortcuts
alias cd2='cd ../..'
alias cd3='cd ../../..'
alias cd4='cd ../../..'
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

# Create a directory and cd into it
function mkdircd () { mkdir -p "$@" && eval cd "\"\$$#\""; }

# Find largest file
function find-largest-files () { du -h -x -s -- * | sort -r -h | head -20; }

# Search history better
function hg () { history | grep "$1"; }

# Reload the shell
alias reload-shell="exec $SHELL"
