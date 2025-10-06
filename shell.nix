{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    # --- Dependências do Aplicativo Python ---
    pyqt6
    pydbus # Para interagir com a interface DBus do picom
  ]);
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    # --- Ambiente Python ---
    pythonEnv

    # --- Ferramentas de Compilação (para o picom) ---
    gcc
    meson
    ninja
    pkg-config
    
    # --- O Compositor que vamos modificar ---
    picom

    # --- Bibliotecas de Desenvolvimento (para o picom) ---
    dbus # Para a interface DBus
    libconfig
    libev
    pcre2
    uthash
    libepoxy
    xorg.libX11
    xorg.libXcomposite
    xorg.libXdamage
    xorg.libXfixes
    xorg.libXrender
    xorg.libXext
    xorg.xorgproto
    xorg.utilmacros
    pixman # Dependência faltando para o picom
    xorg.xcbutilimage
    xorg.xcbutilrenderutil
    xorg.xcbutil
  ];

  # Remove o hook de fonte que não é mais necessário
  shellHook = ''
    echo "Ambiente Power-Dev (Picom) pronto."
  '';
}
