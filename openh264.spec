Name:           openh264
Version:        1.5.0
Release:        1%{?dist}
Summary:        Open Source H.264 Codec
License:        BSD
URL:            http://www.openh264.org/

Source0:        https://github.com/cisco/%{name}/archive/v%{version}tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  nasm

%description
OpenH264 is a codec library which supports H.264 encoding and decoding. It is
suitable for use in real time applications such as WebRTC.

%package        libs
Summary:        H.264 codec %{name} libraries

%description    libs
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}. This package contains the shared libraries.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
sed -i \
    -e 's@PREFIX=/usr/local@PREFIX=%{_prefix}@g' \
    -e 's@SHAREDLIB_DIR=$(PREFIX)/lib@SHAREDLIB_DIR=%{_libdir}@g' \
    -e 's@LIBDIR_NAME=lib@LIBDIR_NAME=%{_lib}@g' \
    -e 's@CFLAGS_OPT=-O3@CFLAGS_OPT=%{optflags}@g' \
    Makefile

%build
make %{?_smp_mflags} 

%install
%make_install
find %{buildroot} -name "*.a" -delete

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md CONTRIBUTORS
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 1.5.0-1
- First build.
