{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.poetry
    pkgs.pkg-config
    pkgs.libmysqlclient
    pkgs.python312Packages.setuptools
    pkgs.python312Packages.wheel
  ];

  shellHook = ''
    export PKG_CONFIG_PATH=${pkgs.libmysqlclient.dev}/lib/pkgconfig:$PKG_CONFIG_PATH
    export MYSQLCLIENT_CFLAGS=$(pkg-config --cflags mysqlclient)
    export MYSQLCLIENT_LDFLAGS=$(pkg-config --libs mysqlclient)
  '';
}
