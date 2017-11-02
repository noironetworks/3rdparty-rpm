%{!?buildversion:%define buildversion 1}

Name: rapidjson-devel
Epoch:   1
Version: 1.1.0
Release: %{buildversion}%{?dist}
Summary: RapidJSON is a JSON parser and generator for C++.

Group: Development/Tools
License: BSD
URL: https://github.com/miloyip/rapidjson
Source0: https://github.com/miloyip/rapidjson/archive/v1.1.0.tar.gz

BuildRequires: cmake
BuildRequires: doxygen

%description
RapidJSON is small but complete. It supports both SAX and DOM style
API. The SAX parser is only a half thousand lines of code.

RapidJSON is fast. Its performance can be comparable to strlen(). It
also optionally supports SSE2/SSE4.1 for acceleration.

RapidJSON is self-contained. It does not depend on external libraries
such as BOOST. It even does not depend on STL.

%prep
%setup -q -n rapidjson-1.1.0

%build
%cmake .

%install
make install DESTDIR=%{buildroot}

%check

%files
%{_includedir}/rapidjson
%{_libdir}/pkgconfig/RapidJSON.pc
%{_libdir}/cmake/RapidJSON/RapidJSONConfig.cmake
%{_libdir}/cmake/RapidJSON/RapidJSONConfigVersion.cmake
%doc %{_docdir}/RapidJSON/

%changelog
* Thu Nov 02 2017 Rob Adams <readams@readams.net> - 1.1.0
- Upgrade to 1.1.0
* Tue May 19 2015 Rob Adams <readams@readams.net> - 1.0.2
- Upgrade to 1.0.2
* Tue May 05 2015 Rob Adams <readams@readams.net> - 1.0.1
- Upgrade to 1.0.1
* Wed Apr 08 2015 Rob Adams <readams@readams.net> - 1.0~beta
- Upgrade to 1.0 beta
* Fri Dec 12 2014 Rob Adams <readams@readams.net> - 0.12~git879def80f2
- Initial package
