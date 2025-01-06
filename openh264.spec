# To get the commit:
# git clone https://github.com/cisco/openh264.git
# cd openh264
# rm -rf gmp-api; make gmp-bootstrap; cd gmp-api
# git rev-parse HEAD
%global commit1 e7d30b921df736a1121a0c8e0cf3ab1ce5b8a4b7
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# Makefile expects V=Yes instead of V=1:
%global _make_verbose V=Yes

Name:           openh264
Version:        2.5.0
Release:        2%{?dist}
Epoch:          1
Summary:        Open Source H.264 Codec
License:        BSD
URL:            https://www.openh264.org/

Source0:        https://github.com/cisco/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/mozilla/gmp-api/archive/%{commit1}/gmp-api-%{shortcommit1}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  nasm

Obsoletes:  noopenh264 < 1:0
Obsoletes:  %{name}-libs < %{?epoch}:%{version}-%{release}
Provides:   %{name}-libs = %{?epoch}:%{version}-%{release}
Provides:   %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}

%description
OpenH264 is a codec library which supports H.264 encoding and decoding. It is
suitable for use in real time applications such as WebRTC.

%package devel
Summary:    Development files for %{name}
Obsoletes:  noopenh264-devel < 1:0
Requires:   %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n mozilla-%{name}
Summary:    H.264 codec support for Mozilla browsers
Requires:   %{name}%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:   mozilla-filesystem%{?_isa}

%description -n mozilla-openh264
The mozilla-openh264 package contains a H.264 codec plugin for Mozilla browsers.

%prep
%autosetup -n %{name}-%{version}

# Extract gmp-api archive
tar -xf %{S:1}
mv gmp-api-%{commit1} gmp-api

%build
sed -i \
  -e 's@PREFIX=/usr/local@PREFIX=%{_prefix}@g' \
  -e 's@SHAREDLIB_DIR=$(PREFIX)/lib@SHAREDLIB_DIR=%{_libdir}@g' \
  -e 's@LIBDIR_NAME=lib@LIBDIR_NAME=%{_lib}@g' \
  -e 's@CFLAGS_OPT=-O3@CFLAGS_OPT=%{optflags}@g' \
  -e '/^CFLAGS_OPT=/i LDFLAGS=%{__global_ldflags}' \
  Makefile
%make_build
%make_build plugin

%install
%make_install
find %{buildroot} -name "*.a" -delete

# Install mozilla plugin
mkdir -p %{buildroot}%{_libdir}/mozilla/plugins/gmp-gmpopenh264/system-installed
cp -a libgmpopenh264.so* gmpopenh264.info %{buildroot}%{_libdir}/mozilla/plugins/gmp-gmpopenh264/system-installed/

mkdir -p %{buildroot}%{_libdir}/firefox/defaults/pref
cat > %{buildroot}%{_libdir}/firefox/defaults/pref/gmpopenh264.js << EOF
pref("media.gmp-gmpopenh264.autoupdate", false);
pref("media.gmp-gmpopenh264.version", "system-installed");
pref("media.gmp-gmpopenh264.enabled", true);
pref("media.gmp-gmpopenh264.provider.enabled", true);
pref("media.peerconnection.video.h264_enabled", true);
EOF

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/gmpopenh264.sh << EOF
MOZ_GMP_PATH="%{_libdir}/mozilla/plugins/gmp-gmpopenh264/system-installed"
export MOZ_GMP_PATH
EOF

%files
%license LICENSE
%doc README.md CONTRIBUTORS
%{_libdir}/lib%{name}.so.7
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n mozilla-%{name}
%{_sysconfdir}/profile.d/gmpopenh264.sh
%dir %{_libdir}/firefox
%dir %{_libdir}/firefox/defaults
%dir %{_libdir}/firefox/defaults/pref
%{_libdir}/firefox/defaults/pref/gmpopenh264.js
%{_libdir}/mozilla/plugins/gmp-gmpopenh264/

%changelog
* Mon Jan 06 2025 Simone Caronni <negativo17@gmail.com> - 1:2.5.0-2
- Rename openh264-libs package to openh264, like in Fedora.
- Obsolete nopenh264.
- Trim changelog.

* Sat Nov 09 2024 Simone Caronni <negativo17@gmail.com> - 1:2.5.0-1
- Update to version 2.5.0.

* Wed Feb 07 2024 Simone Caronni <negativo17@gmail.com> - 1:2.4.1-1
- Update to 2.4.1.

* Sun Nov 26 2023 Simone Caronni <negativo17@gmail.com> - 1:2.4.0-1
- Update to 2.4.0.
