# wine can use libcapi
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define libname %mklibname capi20 3
%define lib32name %mklib32name capi20 3
%define obsname %mklibname capi20 1
%define obs32name %mklibname capi20 1
%define devname %mklibname -d capi20
%define dev32name %mklib32name -d capi20

Name:		libcapi
Summary:	CAPI (ISDN) library
Version:	3.27
Release:	1
Source0:	https://github.com/leggewie-DM/libcapi20/archive/refs/heads/master.tar.gz
Group:		System/Libraries
License:	MIT
BuildRequires:	make
%if %{with compat32}
BuildRequires:	devel(libunwind)
%endif

%description
CAPI (ISDN) library

%package -n %{libname}
Summary: ISDN CAPI library
Group: System/Libraries
Obsoletes: %{obsname} < %{EVRD}

%description -n %{libname}
ISDN CAPI library

%files -n %{libname}
%{_libdir}/libcapi20.so.3*
%{_libdir}/capi

%package -n %{devname}
Summary: Development files for the CAPI ISDN library
Group: Development/C++ and C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files for the CAPI ISDN library

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/libcapi20.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/capi20.pc

%if %{with compat32}
%package -n %{dev32name}
Summary: Development files for the CAPI ISDN library (32-bit)
Group: Development/C++ and C
Requires: %{devname} = %{EVRD}
Requires: %{lib32name} = %{EVRD}

%description -n %{dev32name}
Development files for the CAPI ISDN library

%files -n %{dev32name}
%{_prefix}/lib/libcapi20.so
%{_prefix}/lib/*.a
%{_prefix}/lib/pkgconfig/capi20.pc

%package -n %{lib32name}
Summary: ISDN CAPI library
Group: System/Libraries
Obsoletes: %{obs32name} < %{EVRD}

%description -n %{lib32name}
ISDN CAPI library

%files -n %{lib32name}
%{_prefix}/lib/libcapi20.so.3*
%{_prefix}/lib/capi
%endif

%prep
%autosetup -p1 -n libcapi20-master
export CPPFLAGS=-I$(pwd)
CONFIGURE_TOP=$(pwd)

%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
%endif

mkdir build
cd build
%configure

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build
