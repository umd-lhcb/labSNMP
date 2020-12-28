{
  description = "A Python library to control lab PSUs with SNMP protocol.";

  inputs = rec {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.09";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    {
      overlay = import ./nix/overlay.nix;
    }
    //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
        stdenv = pkgs.stdenv;
      in
      {
        devShell = pkgs.mkShell {
          name = "labSNMP";
          buildInputs = with pythonPackages; [
            labSNMP
          ]
          ++ stdenv.lib.optionals (stdenv.isx86_64) [
            # Python auto-complete
            jedi

            # Linters
            flake8
            pylint
          ];
        };
      });
}
