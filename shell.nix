let
  pkgs = import <nixpkgs>;
  python = pkgs.python3;
  pythonPackages = python.pkgs;
in

pkgs.mkShell {
  name = "labSNMP";
  buildInputs = with pythonPackages; [
    pysnmp
  ];
}
