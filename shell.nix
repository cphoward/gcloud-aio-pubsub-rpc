{ pkgs ? import <nixpkgs> {} }:

# let
#   gcloud-aio-pubsub = import ./gcloud-aio-pubsub.nix { inherit (pkgs) lib python3Packages fetchFromGitHub poetry2nix; };
# in
pkgs.mkShell {
  buildInputs = [
    # gcloud-aio-pubsub
    pkgs.poetry
    pkgs.python311
    pkgs.python311Packages.cachetools
    pkgs.python311Packages.python-lsp-server
    pkgs.python311Packages.python-lsp-server
    pkgs.python311Packages.prometheus-client
  ];
}
