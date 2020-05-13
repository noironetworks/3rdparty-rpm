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
echo "the value of mymacro is --%{cmake}--"
%setup -q -n prometheus-cpp-%{version}

%package lib
Summary: library
Requires: %{name}-lib = %{version}-%{release}


%package devel
Summary: devel
Requires: %{name}-devel = %{version}-%{release}

%description devel
Development libraries for prometheus

%description lib
Development libraries for prometheus

%build
cmake3 . -DCMAKE_INSTALL_PREFIX:PATH=/usr

%install
make -j4
make install DESTDIR=%{buildroot}

%files lib
%{_libdir}/cmake/prometheus-cpp/prometheus*
%{_libdir}/libprometheus-cpp*
/usr/lib/pkgconfig/prometheus*

%files devel
%{_includedir}/prometheus/*

%changelog
* Sat Apr 18 2020 Adam Miller <bashokba@cisco.com>
- Promtheus changes                                                                                                                              



