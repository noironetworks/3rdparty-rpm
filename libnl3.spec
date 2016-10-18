%bcond_without python

Name: libnl3
Version: 3.2.27
Release: 1%{?dist}
Summary: Convenience library for kernel netlink sockets
Group: Development/Libraries
License: LGPLv2
URL: http://www.infradead.org/~tgr/libnl/

%define fullversion %{version}

Source: http://www.infradead.org/~tgr/libnl/files/libnl-%{fullversion}.tar.gz
Source1: http://www.infradead.org/~tgr/libnl/files/libnl-doc-%{fullversion}.tar.gz

BuildRequires: flex bison
BuildRequires: python
BuildRequires: libtool autoconf automake
BuildRequires: swig
%if %{with python}
BuildRequires: python2-devel
BuildRequires: python3-devel
%endif

%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation

%package devel
Summary: Libraries and headers for using libnl3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}
Requires: kernel-headers

%description devel
This package contains various headers for using libnl3

%package cli
Summary: Command line interface utils for libnl3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description cli
This package contains various libnl3 utils and additional
libraries on which they depend

%package doc
Summary: API documentation for libnl3
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
This package contains libnl3 API documentation

%if %{with python}
%package -n python-libnl3
Summary: libnl3 binding for Python 2
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description -n python-libnl3
Python 2 bindings for libnl3

%package -n python3-libnl3
Summary: libnl3 binding for Python 3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description -n python3-libnl3
Python 3 bindings for libnl3
%endif

%prep
%setup -q -n libnl-%{fullversion}

tar -xzf %SOURCE1

%build
autoreconf -vif
%configure --disable-static
make %{?_smp_mflags}

%if %{with python}
pushd ./python/
# build twice, otherwise capi.py is not copied to the build directory.
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
popd
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name \*.la -delete

%if %{with python}
pushd ./python/
%{__python3} setup.py install --skip-build --root "$RPM_BUILD_ROOT"
%{__python2} setup.py install --skip-build --root "$RPM_BUILD_ROOT"
popd
%endif

%check
make check

%if %{with python}
pushd ./python/
%{__python3} setup.py check
%{__python2} setup.py check
popd
%endif

%post -p /sbin/ldconfig
%post cli -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%postun cli -p /sbin/ldconfig

%files
%doc COPYING
%exclude %{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl-*.so.*
%config(noreplace) %{_sysconfdir}/*

%files devel
%doc COPYING
%{_includedir}/libnl3/netlink/
%dir %{_includedir}/libnl3/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files cli
%doc COPYING
%{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl/
%{_bindir}/*
%{_mandir}/man8/* 

%files doc
%doc COPYING
%doc libnl-doc-%{fullversion}/*.html
%doc libnl-doc-%{fullversion}/*.css
%doc libnl-doc-%{fullversion}/stylesheets/*
%doc libnl-doc-%{fullversion}/images/*
%doc libnl-doc-%{fullversion}/images/icons/*
%doc libnl-doc-%{fullversion}/images/icons/callouts/*
%doc libnl-doc-%{fullversion}/api/*

%if %{with python}
%files -n python-libnl3
%defattr(-,root,root,-)
%{python2_sitearch}/netlink
%{python2_sitearch}/netlink-*.egg-info

%files -n python3-libnl3
%defattr(-,root,root,-)
%{python3_sitearch}/netlink
%{python3_sitearch}/netlink-*.egg-info
%endif

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.27-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 16 2015 Thomas Haller <thaller@redhat.com> - 3.2.27-1
- Update to 3.2.27

* Mon Sep 21 2015 Thomas Haller <thaller@redhat.com> - 3.2.27-0.1
- Update to 3.2.27-rc1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-4
- Update to 3.2.26
- cli package brings more commands and installs them to /bin

* Mon Mar  9 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-3
- Update to 3.2.26-rc1
- fix broken symbols from 3.2.26-1
- backport upstream fix for nl_socket_set_fd()

* Sat Mar  7 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-2
- Revert update to 3.2.26-rc1 to previous 3.2.25-6

* Fri Mar  6 2015 Thomas Haller <thaller@redhat.com> - 3.2.26-1
- Update to 3.2.26-rc1

* Tue Feb  3 2015 Thomas Haller <thaller@redhat.com> - 3.2.25-6
- add new packages with language bindings for Python 2 and Python 3 (rh #1167112)

* Tue Dec  9 2014 Thomas Haller <thaller@redhat.com> - 3.2.25-5
- Add support for IPv6 link local address generation

* Fri Oct 10 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.2.25-4
- Add support for IPv6 tokenized interface identifiers

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Thomas Haller <thaller@redhat.com> 3.2.25-2
- Update to 3.2.25

* Fri Jul  4 2014 Thomas Haller <thaller@redhat.com> 3.2.25-1
- Update to 3.2.25-rc1

* Sun Jun  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.2.24-5
- Run autoreconf for new automake, cleanup spec

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Thomas Haller <thaller@redhat.com> - 3.2.24-3
- add nl_has_capability() function
- retry local port on ADDRINUSE (rh #1097175)
- python: fix passing wrong argument in netlink/core.py
- fix return value of nl_rtgen_request()
- fix nl_msec2str()
- fix crash in rtnl_act_msg_parse()
- fix rtnl_route_build_msg() not to guess the route scope if RT_SCOPE_NOWHERE

* Fri Apr  4 2014 Thomas Haller <thaller@redhat.com> - 3.2.24-2
- fix breaking on older kernels due to IFA_FLAGS attribute (rh #1063885)

* Thu Jan 23 2014 Thomas Haller <thaller@redhat.com> - 3.2.24-1
- Update to 3.2.24 (rhbz#963111)

* Mon Sep 23 2013 Paul Wouters <pwouters@redhat.com> - 3.2.22-2
- Update to 3.2.22 (rhbz#963111)
- Add patch for double tree crasher in rtnl_link_set_address_family()

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jan 25 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.21-1
- Update to 3.2.21

* Wed Jan 23 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.20-1
- Update to 3.2.20

* Sun Jan 20 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-2
- Age fix

* Thu Jan 17 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-1
- Update to 3.2.19

* Tue Oct 30 2012 Dan Williams <dcbw@redhat.com> - 3.2.14-1
- Update to 3.2.14

* Mon Sep 17 2012 Dan Williams <dcbw@redhat.com> - 3.2.13-1
- Update to 3.2.13

* Fri Feb 10 2012 Dan Williams <dcbw@redhat.com> - 3.2.7-1
- Update to 3.2.7

* Tue Jan 17 2012 Jiri Pirko <jpirko@redhat.com> - 3.2.6-1
- Initial build
