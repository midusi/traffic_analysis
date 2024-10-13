{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.poetry
    pkgs.pkg-config
    pkgs.libmysqlclient
    pkgs.python312Packages.setuptools
    pkgs.nodejs
    pkgs.libGL
    pkgs.stdenv.cc.cc.lib
  ];
  LD_LIBRARY_PATH="${pkgs.libGL}/lib/:${pkgs.stdenv.cc.cc.lib}/lib/:${pkgs.glib.out}/lib/";

  shellHook = ''
    echo "Iniciando servidores con tmux..."

    # Iniciar una sesión de tmux si no está ya corriendo
    if ! tmux ls | grep -q "civil"; then
      tmux new-session -d -s civil

      # Ventana 1: Backend Flask
      tmux rename-window -t civil 'backend'
      tmux send-keys -t civil 'cd backend && poetry run flask --debug run' C-m

      # Ventana 2: Frontend npm
      tmux new-window -t civil -n 'frontend'
      tmux send-keys -t civil:1 'cd frontend && npm run dev' C-m

      # Abrir nvim en 2 ventanas más
      tmux new-window -t civil -n 'vim-back'
      tmux send-keys -t civil:2 'cd backend && nvim' C-m
      tmux new-window -t civil -n 'vim-front'
      tmux send-keys -t civil:3 'cd frontend && nvim' C-m

      # Adjuntar a la sesión al iniciar el shell
      tmux attach-session -t civil
    else
      echo "La sesión de tmux ya está corriendo."
    fi
  '';
}
