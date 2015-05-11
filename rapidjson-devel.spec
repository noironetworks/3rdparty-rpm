Name: rapidjson-devel
Epoch:   1
Version: 1.0.1
Release: 1%{?dist}
Summary: RapidJSON is a JSON parser and generator for C++.

Group: Development/Tools
BuildArch: noarch
License: BSD
URL: https://github.com/miloyip/rapidjson
Source0: https://github.com/miloyip/rapidjson/archive/v1.0.1.tar.gz

%description
RapidJSON is small but complete. It supports both SAX and DOM style
API. The SAX parser is only a half thousand lines of code.

RapidJSON is fast. Its performance can be comparable to strlen(). It
also optionally supports SSE2/SSE4.1 for acceleration.

RapidJSON is self-contained. It does not depend on external libraries
such as BOOST. It even does not depend on STL.

%prep
%setup -q -n rapidjson-1.0.1

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_includedir}
cp -R include/rapidjson $RPM_BUILD_ROOT/%{_includedir}

%check

%files
%{_includedir}/rapidjson

%changelog
* Tue May 05 2015 Rob Adams <readams@readams.net> - 1.0.1
- Upgrade to 1.0.1
* Wed Apr 08 2015 Rob Adams <readams@readams.net> - 1.0~beta
- Upgrade to 1.0 beta
* Fri Dec 12 2014 Rob Adams <readams@readams.net> - 0.12~git879def80f2
- Initial package
