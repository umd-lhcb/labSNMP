let
  pkgs = import <nixpkgs> {};
  python = pkgs.python3;
  pythonPackages = python.pkgs;
  stdenv = pkgs.stdenv;
in

pkgs.mkShell {
  name = "labSNMP";
  buildInputs = with pythonPackages; [
    pysnmp
  ]
  ++ stdenv.lib.optionals (stdenv.isx86_64) [
    # Python auto-complete
    jedi

    # Linters
    flake8
    pylint
  ];
}
