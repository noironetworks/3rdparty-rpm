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
wget https://github.com/Kitware/CMake/releases/download/v3.17.0/cmake-3.17.0-Linux-x86_64.sh
sh cmake-3.17.0-Linux-x86_64.sh -- --skip-license --prefix=/root

%package lib
Summary: library
Requires: %{name}-lib = %{version}-%{release}
BuildRequires: wget

%package devel
Summary: devel
Requires: %{name}-devel = %{version}-%{release}
BuildRequires: wget

%description devel
Development libraries for prometheus

%description lib
Development libraries for prometheus

%build
cmake --build _build -DCPACK_GENERATOR=RPM -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=ON
cmake --build _build --target package --parallel $(nproc)

%install
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



