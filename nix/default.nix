{ stdenv
, buildPythonPackage
, root
, pyyaml
, lark-parser
}:

buildPythonPackage rec {
  pname = "pyBabyMaker";
  version = "0.2.1";

  src = builtins.path { path = ./..; name = pname; };

  buildInputs = [ root ];
  propagatedBuildInputs = [
    pysnmp
  ];

  doCheck = false;
}
