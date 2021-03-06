%{!?buildversion:%define buildversion 1}

Name: prometheus-cpp
Version: 0.12.1
Release: %{buildversion}%{?dist}
Summary: Prometheus-cpp

License: BSD
URL: https://github.com/jupp0r/prometheus-cpp
Source0: prometheus-cpp-%{version}.tar.gz

%description
This library aims to enable Metrics-Driven Development for C++ services. It implements the Prometheus Data Model, a powerful abstraction on which to collect and expose metrics.
We offer the possibility for metrics to be collected by Prometheus, but other push/pull collections can be added as plugins.

%global debug_package %{nil}

%prep
%setup -q -n prometheus-cpp-%{version}
export https_proxy=http://proxy.esl.cisco.com
wget https://github.com/Kitware/CMake/releases/download/v3.17.0/cmake-3.17.0-Linux-x86_64.sh
sh cmake-3.17.0-Linux-x86_64.sh -- --skip-license --prefix=/root

%package lib
Summary: library
Requires: %{name}-lib = %{version}-%{release}
%if 0%{?rhel} == 7
BuildRequires: devtoolset-8-toolchain
%endif
BuildRequires: wget
BuildRequires: zlib-devel
BuildRequires: libcurl-devel

%package devel
Summary: devel
Requires: %{name}-devel = %{version}-%{release}
%if 0%{?rhel} == 7
BuildRequires: devtoolset-8-toolchain
%endif
BuildRequires: wget
BuildRequires: zlib-devel
BuildRequires: libcurl-devel

%description devel
Development libraries for prometheus

%description lib
Development libraries for prometheus

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-8/enable
%define __strip /opt/rh/devtoolset-8/root/usr/bin/strip
%endif
/root/bin/cmake -B_build -DCPACK_GENERATOR=RPM -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=ON -DENABLE_PUSH=OFF
/root/bin/cmake --build _build --target package --parallel $(nproc)

%install
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-8/enable
%define __strip /opt/rh/devtoolset-8/root/usr/bin/strip
%endif
cd _build
make -j4
make install DESTDIR=%{buildroot}

%files lib
%{_libdir}/cmake/prometheus-cpp/prometheus*
%{_libdir}/libprometheus-cpp*
%{_libdir}/pkgconfig/prometheus*

%files devel
%{_includedir}/prometheus/*

%changelog
* Sat Apr 18 2020 Bhavana babu <bashokba@cisco.com>
- Prometheus-spec changes
