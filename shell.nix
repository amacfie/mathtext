{
  pkgs ? import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/59b1aef59071cae6e87859dc65de973d2cc595c0.tar.gz";
    sha256 = "0kla405dbqmgbpq59svgbfv7q01z2nnpmq8q2x614r9rrfwfyyrn";
  }) {}
}:

pkgs.mkShell {
  packages = [
    pkgs.s3cmd
    pkgs.p7zip
    pkgs.parallel
    pkgs.pv
    pkgs.git
    pkgs.silver-searcher
    pkgs.ripgrep
    pkgs.wget
    pkgs.unp
    (pkgs.buildGoModule rec {
      pname = "codesearch";
      version = "1.3.0";

      src = pkgs.fetchFromGitHub {
        owner = "junkblocker";
        repo = "codesearch";
        rev = "v${version}";
        sha256 = "sha256-04dW+5grozApbgogowoQ5dle0xHy8LoComhwTE5c4q4=";
      };

      vendorHash = null;

      ldflags = [ "-s" "-w" ];

      meta = with pkgs.lib; {
        description = "Fork of Google codesearch with more options";
        homepage = "https://github.com/junkblocker/codesearch";
        license = [ licenses.bsd3 ];
        maintainers = [];
      };
    })
    (pkgs.perl538Packages.buildPerlPackage {
      pname = "XML-Twig";
      version = "3.52";
      src = pkgs.fetchurl {
        url = "mirror://cpan/authors/id/M/MI/MIROD/XML-Twig-3.52.tar.gz";
        hash = "sha256-/vdYJsJPK4d9Cg0mRSEvxPuXVu1NJxFhSsFcSX6GgK0=";
      };
      postInstall = ''
        mkdir -p $out/bin
        cp tools/xml_split/xml_split $out/bin
      '';
      propagatedBuildInputs = [ pkgs.perl538Packages.XMLParser ];
      doCheck = false;  # requires lots of extra packages
      meta = {
        description = "A Perl module for processing huge XML documents in tree mode";
        license = with pkgs.lib.licenses; [ artistic1 gpl1Plus ];
        mainProgram = "xml_split";
      };
    })
    (pkgs.python311.withPackages (ps: [
      ps.beautifulsoup4
      ps.chromadb
      ps.unidecode
      ps.tqdm
      ps.psutil
      ps.lxml
    ]))
  ];
}

