# upstream version of phpvirtualbox
%define upstreamversion 5.2-1
%define virtualboxversion 5.2

Name: nethserver-virtualbox-%{virtualboxversion}
Summary: Configure phpvirtualbox and VirtualBox for nethserver
Version: 1.0.1
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
BuildArch: noarch
Source: %{name}-%{version}.tar.gz
Source1: https://github.com/phpvirtualbox/phpvirtualbox/archive/%{upstreamversion}.zip
%description
A rpm to configure VirtualBox and phpvirtualbox

%package VirtualBox
Summary: Configure VirtualBox for NethServer
BuildArch: noarch
Requires: VirtualBox-%{virtualboxversion}
Requires: gcc <= 4.9.0
Requires: make
Requires: kernel-devel
Requires: kernel-headers
Requires: dkms
BuildRequires: nethserver-devtools
%description VirtualBox
rpm to configure VirtualBox settings

%package phpvirtualbox
Summary: Configure phpvirtualbox for NethServer
BuildRequires: nethserver-devtools
BuildArch: noarch
Requires: mod_ssl
Requires: php-soap
Requires: php-gd
Requires: php-xml
Requires: php-ldap
Requires: nethserver-virtualbox-%{virtualboxversion}-VirtualBox 
%description phpvirtualbox
Configure phpvirtualbox for NethServer

%prep
%setup

%build
rm -rf %{buildroot}

#Install the  phpvirtualbox binary
mkdir -p phpvirtualbox/usr/share/phpvirtualbox
unzip %{SOURCE1}
cp -r phpvirtualbox-%{upstreamversion}/* phpvirtualbox/usr/share/phpvirtualbox
cp phpvirtualbox/usr/share/phpvirtualbox/config.php-example phpvirtualbox/usr/share/phpvirtualbox/config.php
# Link config file to location required by phpvirtualbox
mkdir -p  phpvirtualbox/etc/phpvirtualbox
ln -s  /usr/share/phpvirtualbox/config.php phpvirtualbox/etc/phpvirtualbox/config.php
# Install a default httpd config
install -D phpvirtualbox/usr/share/phpvirtualbox/phpvirtualbox.conf phpvirtualbox/etc/httpd/conf.d/phpvirtualbox.conf  

for package in VirtualBox phpvirtualbox ; do
    if [[ -f createlinks-${package} ]]; then
        # Hack around createlinks output dir prefix, hardcoded as "root/":
        rm -f root
        ln -sf ${package} root
        perl createlinks-${package}
    fi
    ( cd ${package} ; %{makedocs} )
    %{genfilelist} ${PWD}/${package} \
          >> ${package}.lst
    # !!! Do not create any file or directory after genfilelist invocation !!!
done

#
# Create additional directories and override permissions from genfilelist
#


cat >>VirtualBox.lst <<'EOF'
%dir %{_nseventsdir}/%{name}-VirtualBox-update
EOF

cat >>phpvirtualbox.lst <<'EOF'
%dir %{_nseventsdir}/%{name}-phpvirtualbox-update
%config(noreplace) %{_sysconfdir}/httpd/conf.d/phpvirtualbox.conf
%attr(644, root, root) %{_sysconfdir}/httpd/conf.d/phpvirtualbox.conf
%config(noreplace) %{_datadir}/phpvirtualbox/config.php
%attr(640, root, apache) %{_datadir}/phpvirtualbox/config.php
EOF

%install
for package in VirtualBox phpvirtualbox; do
    (cd ${package}; find . -depth -print | cpio -dump %{buildroot})
done

%files VirtualBox -f VirtualBox.lst
%defattr(-,root,root)
%doc COPYING
%doc README.md

%files phpvirtualbox -f phpvirtualbox.lst
%defattr(-,root,root)
%doc COPYING
%doc README.md

%pre VirtualBox

%pre phpvirtualbox

%changelog
* Fri Mar 29 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.0.1-1

* Sat Jan 12 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.0.0-1
  Initial Release to nethforge stable

* Mon Dec 24 2018 stephane de Labrusse <stephdl@de-labrusse.fr> - 5.2.1
- Initial release
