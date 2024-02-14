{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "aarch64-darwin" "aarch64-linux" "x86_64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in
    {
      overlay = final: prev: {
        python3-venv = prev.python3.withPackages (ps: [
          ps.pybind11
        ]);
      };

      packages = forAllSystems (system: with import nixpkgs { inherit system; overlays = [ self.overlay ]; }; {
        inherit python3-venv;
      });

      devShell = forAllSystems (system: with import nixpkgs { inherit system; overlays = [ self.overlay ]; }; pkgs.mkShell {

        buildInputs = [
        ];
        packages = [
          pkgs.python3-venv
          pkgs.pkg-config
          pkgs.meson
          pkgs.ninja
        ];
      });
    };
}
