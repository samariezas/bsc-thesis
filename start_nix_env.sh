#!/usr/bin/env bash
nix develop --command bash -c "export LOCALE_ARCHIVE=/usr/lib/locale/locale-archive; export SHELL=zsh; tmux"
