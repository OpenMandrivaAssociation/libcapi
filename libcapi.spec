# wine can use libcapi
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define devname %mklibname -d capi20
%define dev32name %mklib32name -d capi20

Name:		libcapi
Summary:	CAPI (ISDN) library
Version:	2.0.3
Release:	2
Source0:	https://github.com/ISDN4Linux/libcapi/archive/master/%{name}-%{version}.tar.gz
Patch0:		libcapi-compile.patch
Group:		System/Libraries
License:	MIT
BuildRequires:	make
BuildRequires:	pkgconfig(libbsd)
%if %{with compat32}
BuildRequires:	devel(libbsd)
BuildRequires:	devel(libunwind)
%endif

%description
CAPI (ISDN) library

%libpackage capi20 1

%package -n %{devname}
Summary: Development files for the CAPI ISDN library
Group: Development/C++ and C
Requires: %{mklibname capi20 1}
# capi headers #include <bsd/sys/endian.h>
Requires: pkgconfig(libbsd)

%description -n %{devname}
Development files for the CAPI ISDN library

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/*.so
%{_mandir}/man3/*

%if %{with compat32}
%lib32package capi20 1

%package -n %{dev32name}
Summary: Development files for the CAPI ISDN library (32-bit)
Group: Development/C++ and C
Requires: %{devname} = %{EVRD}
Requires: %{mklib32name capi20 1}
# capi headers #include <bsd/sys/endian.h>
Requires: devel(libbsd)

%description -n %{dev32name}
Development files for the CAPI ISDN library

%files -n %{dev32name}
%{_prefix}/lib/*.so
%endif

%prep
%autosetup -p1 -n libcapi-master
%if %{with compat32}
mkdir build32
for i in *.c; do
	%{__cc} $(echo %{optflags} |sed -e 's,-m64,,;s,-mx32,,') -m32 -fPIC -D_BSD_SOURCE=1 -DHAVE_ALL=1 -DHAVE_BINTEC=1 -DHAVE_CAPI_CLIENT=1 -o build32/${i/.c/.o} -c $i
done
%{__cc} -shared $(echo %{optflags} |sed -e 's,-m64,,;s,-mx32,,') $(echo %{build_ldflags} |sed -e 's,-m64,,;s,-mx32,,') -m32 -fPIC -o build32/libcapi20.so.1.0 -Wl,-soname,libcapi20.so.1 build32/*.o -lbsd
%endif

mkdir build
for i in *.c; do
	%{__cc} %{optflags} -fPIC -D_BSD_SOURCE=1 -DHAVE_ALL=1 -DHAVE_BINTEC=1 -DHAVE_CAPI_CLIENT=1 -o build/${i/.c/.o} -c $i
done
%{__cc} -shared %{optflags} %{build_ldflags} -fPIC -o build/libcapi20.so.1.0 -Wl,-soname,libcapi20.so.1 build/*.o -lbsd

%install
%if %{with compat32}
mkdir -p %{buildroot}%{_prefix}/lib
install -m 755 build32/libcapi20.so.1.0 %{buildroot}%{_prefix}/lib/
ln -s libcapi20.so.1.0 %{buildroot}%{_prefix}/lib/libcapi20.so.1
ln -s libcapi20.so.1.0 %{buildroot}%{_prefix}/lib/libcapi20.so
%endif
mkdir -p %{buildroot}%{_libdir}
install -m 755 build/libcapi20.so.1.0 %{buildroot}%{_libdir}/
ln -s libcapi20.so.1.0 %{buildroot}%{_libdir}/libcapi20.so.1
ln -s libcapi20.so.1.0 %{buildroot}%{_libdir}/libcapi20.so
mkdir -p %{buildroot}%{_includedir}
install -m 644 *.h %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_mandir}/man3
install -m 644 *.3 %{buildroot}%{_mandir}/man3/
