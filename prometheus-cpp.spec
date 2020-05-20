%{!?buildversion:%define buildversion 1}

Name: prometheus-cpp
Version: 0.9.0
Release: %{buildversion}%{?dist}
Summary: Prometheus-cpp

License: BSD
URL: https://github.com/jupp0r/prometheus-cpp
Source0: prometheus-cpp-%{version}.tar.gz

%description
This library aims to enable Metrics-Driven Development for C++ services. It implements the Prometheus Data Model, a powerful abstraction on which to collect and expose metrics.
We offer the possibility for metrics to be collected by Prometheus, but other push/pull collections can be added as plugins.

%prep
%setup -q -n prometheus-cpp-%{version}

%package lib
Summary: library
Requires: %{name}-lib = %{version}-%{release}
BuildRequires: devtoolset-7-toolchain

%package devel
Summary: devel
Requires: %{name}-devel = %{version}-%{release}
BuildRequires: devtoolset-7-toolchain

%description devel
Development libraries for prometheus

%description lib
Development libraries for prometheus

%build
. /opt/rh/devtoolset-7/enable
%define __strip /opt/rh/devtoolset-7/root/usr/bin/strip
cmake3 -B_build -DCPACK_GENERATOR=RPM -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=ON
cmake3 --build _build --target package --parallel $(nproc)

%install
. /opt/rh/devtoolset-7/enable
%define __strip /opt/rh/devtoolset-7/root/usr/bin/strip
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



