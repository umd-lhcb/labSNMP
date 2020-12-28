{ stdenv
, buildPythonPackage
, pysnmp
}:

buildPythonPackage rec {
  pname = "labSNMP";
  version = "0.2.1";

  src = builtins.path { path = ./..; name = pname; };

  propagatedBuildInputs = [
    pysnmp
  ];

  doCheck = false;
}
