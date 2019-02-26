# Latest commit on the Firefox branch as defined in the Makefile:
# https://github.com/mozilla/gmp-api/tree/Firefox39
%global commit1 c5f1d0f3213178818cbfb3e16f31d07328980560
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

Name:           openh264
Version:        1.8.0
Release:        1%{?dist}
Epoch:          1
Summary:        Open Source H.264 Codec
License:        BSD
URL:            http://www.openh264.org/

Source0:        https://github.com/cisco/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/mozilla/gmp-api/archive/%{commit1}/gmp-api-%{shortcommit1}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  nasm

%description
OpenH264 is a codec library which supports H.264 encoding and decoding. It is
suitable for use in real time applications such as WebRTC.

%package libs
Summary:    H.264 codec %{name} libraries
Obsoletes:  %{name} < %{?epoch}:%{version}-%{release}
Provides:   %{name} = %{?epoch}:%{version}-%{release}
Provides:   %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description libs
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}. This package contains the shared libraries.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n mozilla-%{name}
Summary:    H.264 codec support for Mozilla browsers
Requires:   %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:   mozilla-filesystem%{?_isa}

%description -n mozilla-openh264
The mozilla-openh264 package contains a H.264 codec plugin for Mozilla browsers.

%prep
%setup -qn %{name}-%{version}

# Extract gmp-api archive
tar -xf %{S:1}
mv gmp-api-%{commit1} gmp-api

sed -i \
    -e 's@PREFIX=/usr/local@PREFIX=%{_prefix}@g' \
    -e 's@SHAREDLIB_DIR=$(PREFIX)/lib@SHAREDLIB_DIR=%{_libdir}@g' \
    -e 's@LIBDIR_NAME=lib@LIBDIR_NAME=%{_lib}@g' \
    -e 's@CFLAGS_OPT=-O3@CFLAGS_OPT=%{optflags}@g' \
    -e '/^CFLAGS_OPT=/i LDFLAGS=%{__global_ldflags}' \
    Makefile

%build
make %{?_smp_mflags}
make plugin %{?_smp_mflags}

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

%ldconfig_scriptlets libs

%files libs
%license LICENSE
%doc README.md CONTRIBUTORS
%{_libdir}/lib%{name}.so.4
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
* Tue Feb 26 2019 Simone Caronni <negativo17@gmail.com> - 1:1.8.0-1
- Update to 1.8.0.

* Thu Sep 20 2018 Simone Caronni <negativo17@gmail.com> - 1:1.7.0-2
- Add GCC build requirement.

* Tue Oct 24 2017 Simone Caronni <negativo17@gmail.com> - 1:1.7.0-1
- Update to version 1.7.0.

* Fri Nov 25 2016 Simone Caronni <negativo17@gmail.com> - 1:1.6.0-2
- Automatically enable the OpenH264 plugin.

* Wed Nov 09 2016 Simone Caronni <negativo17@gmail.com> - 1:1.6.0-1
- Update to 1.6.0 official release.

* Fri Aug 05 2016 Simone Caronni <negativo17@gmail.com> - 1:1.5.3-1
- Update to 1.5.3 branch.
- Obsoletes main package from the OpenH264 repository (prep for 1.6):
  https://fedoraproject.org/wiki/OpenH264

* Tue Apr 19 2016 Simone Caronni <negativo17@gmail.com> - 1.5.0-2
- Fix source URL.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 1.5.0-1
- First build.
