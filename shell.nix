{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.poetry
    pkgs.pkg-config
    pkgs.libmysqlclient
    pkgs.python312Packages.setuptools
    pkgs.nodejs
  ];
}
