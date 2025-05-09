%define major 1
%define libname %mklibname uv
%define oldlibname %mklibname uv 1
%define devname %mklibname uv -d

Name:		libuv
Version:	1.51.0
Release:	1
Summary:	Platform layer for node.js and neovim

Group:		Development/Other
# the licensing breakdown is described in detail in the LICENSE file
License:	MIT and BSD and ISC
URL:		https://libuv.org/
Source0:	https://github.com/libuv/libuv/archive/v%{version}/%{name}-%{version}.tar.gz

#BuildRequires:	gyp

%description
libuv is a new platform layer for Node providing a cross-platform event loop.

It is currently used by node.js and neovim.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries
%rename %{oldlibname}

%description -n	%{libname}
%{summary}.

%package -n %{devname}
Summary:	Development libraries for libuv
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
Development libraries for libuv.

%prep
%autosetup -p1
echo "m4_define([UV_EXTRA_AUTOMAKE_FLAGS], [serial-tests])" \
        > m4/libuv-extra-automake-flags.m4
libtoolize --install --copy --force --automake
aclocal -I m4
autoconf
automake --add-missing --copy --foreign

%build

export CFLAGS='%{optflags}'
export CXXFLAGS='%{optflags}'
%configure
%make_build CC="%{__cc}"

%install
%make_install

%check
# Tests are currently disabled because some require network access
# Working with upstream to split these out
#./run-tests
#./run-benchmarks

%files -n %{libname}
%{_libdir}/libuv.so.%{major}*

%files -n %{devname}
%doc README.md AUTHORS LICENSE
%{_libdir}/libuv.so
%{_libdir}/pkgconfig/libuv.pc
%{_includedir}/uv/*.h
%{_includedir}/uv.h
