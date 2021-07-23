# Maintainer: Bruno Goncalves <biglinux.com.br>

pkgname=calamares-biglinux
pkgver=1_r21_2021_07_23
pkgrel=1
arch=('any')
license=('')
url="https://github.com/biglinux/bigbashview"
pkgdesc="Calamares tweaks to BigLinux, like using btrfs+zstd for default"

source=('git+https://github.com/biglinux/calamares-biglinux.git')
sha256sums=('SKIP')
makedepends=('git')
install=${pkgname}.install

pkgver() {
    cd ${pkgname}
    printf "1_r$(git rev-list --count HEAD)_$(date "+%Y_%m_%d")"
}


package() {
    depends=('calamares')
    
    cp -r "${srcdir}/${pkgname}/usr" "${pkgdir}/usr"
}

