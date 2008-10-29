#
# TODO:
# - check log files permisions - should be writable by radius user/group
#   (log files are created by server)
# - prepare to use with --as-needed
# - ac/am regeneration doesn't work
# - move plugins into separate packages:
#   /usr/sbin/radsniff: libpcap
#   /usr/lib/freeradius/rlm_eap_ikev2-2.1.1.so: libeap-ikev2
#   /usr/lib/freeradius/rlm_krb5-2.1.1.so: libkrb5, libcom_err, libkrb5support, libkeyutils
#   /usr/lib/freeradius/rlm_ldap-2.1.1.so: libldap_r, liblber, libsasl2, libcrypt, libssl
#   /usr/lib/freeradius/rlm_otp-2.1.1.so
#   /usr/lib/freeradius/rlm_pam-2.1.1.so
#   /usr/lib/freeradius/rlm_perl-2.1.1.so
#   /usr/lib/freeradius/rlm_python-2.1.1.so
#   /usr/lib/freeradius/rlm_sql_mysql-2.1.1.so
#   /usr/lib/freeradius/rlm_sql_postgresql-2.1.1.so
#   /usr/lib/freeradius/rlm_sql_sqlite-2.1.1.so
#   /usr/lib/freeradius/rlm_sql_unixodbc-2.1.1.so
#   /usr/lib/freeradius/rlm_unix-2.1.1.so
#
%include	/usr/lib/rpm/macros.perl
#
Summary:	High-performance and highly configurable RADIUS server
Summary(pl.UTF-8):	Szybki i wysoce konfigurowalny serwer RADIUS
Name:		freeradius-server
Version:	2.1.1
Release:	0.10
License:	GPL
Group:		Networking/Daemons/Radius
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.bz2
# Source0-md5:	4ccf748ef9851d90844d085647351ca4
Source1:	%{name}.logrotate
Source2:	%{name}.init
Source3:	%{name}.pam
Patch0:		%{name}-config.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-makefile.patch
Patch3:		%{name}-rundir.patch
URL:		http://www.freeradius.org/
BuildRequires:	Firebird-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel
BuildRequires:	gdbm-devel
BuildRequires:	libeap-ikev2-devel
BuildRequires:	libtool
BuildRequires:	net-snmp-utils
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sqlite3-devel
BuildRequires:	unixODBC-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires:	perl(DynaLoader) = %(%{__perl} -MDynaLoader -e 'print DynaLoader->VERSION')
Requires:	rc-scripts
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(radius)
Provides:	user(radius)
Provides:	freeradius = %{version}-%{release}
Obsoletes:	cistron-radius
Obsoletes:	freeradius < 2.0
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mibdir	%{_datadir}/snmp/mibs
%define         filterout_ld    -Wl,--as-needed

%description
The FreeRADIUS Server Project is an attempt to create a
high-performance and highly configurable GPL'd RADIUS server. It is
generally similar to the Livingston 2.0 RADIUS server, but has a lot
more features, and is much more configurable.

%description -l pl.UTF-8
Projekt FreeRadius ma na celu stworzenie szybkiego i wysoce
konfigurowalnego serwera RADIUS na licencji GPL. Ten jest podobny do
Livingston 2.0 RADIUS server ale ma o wiele więcej funkcji i posiada
większe możliwości konfigurowania.

%package mibs
Summary:        MIB database for %{name}
Summary(pl.UTF-8):      Baza danych MIB dla %{name}
Group:          Applications/System
Suggests:	libsmi

%description mibs
MIB database for %{name}.

%description mibs -l pl.UTF-8
Baza danych MIB dla %{name}.


%package libs
Summary:	Freeradius libraries
Group:          Libraries

%description libs
Freeradius libraries.

%package devel
Summary:	Header files and devel library
Group:          Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files and libraries.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# Keep it for future when ac/am regeneration will be ok
#find -name 'configure.[ia][nc]' -type f | while read FILE; do
#    cd $(dirname "$FILE")
#    %{__libtoolize}
#    %{__aclocal} -I $OLDPWD
#    %{__autoconf}
#    [ -f config.h.in ] && %{__autoheader}
#    cd -
#done

LIBS="-lgdbm" \
%configure \
	--enable-strict-dependencies \
	--with-experimental-modules \
	--with-logdir=%{_var}/log/freeradius \
	--with-system-libtool \
	--without-rlm_eap_tnc \
	--without-rlm_opendirectory \
	--without-rlm_sql_db2 \
	--without-rlm_sql_iodbc \
	--without-rlm_sql_oracle

%{make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d} \
	$RPM_BUILD_ROOT%{_var}/log/{,archive}/freeradius/radacct \
	$RPM_BUILD_ROOT%{mibdir}

%{__make} -j1 install \
	R=$RPM_BUILD_ROOT

install %{SOURCE1}	$RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE2}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3}	$RPM_BUILD_ROOT/etc/pam.d/radius

# Install mibs:
install mibs/FREERADIUS-*.txt $RPM_BUILD_ROOT%{mibdir}

# Cleanups:
rm -rf $RPM_BUILD_ROOT%{_docdir}/freeradius \
	$RPM_BUILD_ROOT%{_libdir}/*.{a,la} \
	$RPM_BUILD_ROOT%{_libdir}/freeradius/*.a \
	$RPM_BUILD_ROOT%{_sbindir}/rc.* \
	$RPM_BUILD_ROOT%{_sysconfdir}/*.pl

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 29 -r -f radius
%useradd -u 29 -d %{_localstatedir} -s /bin/false -M -r -c "%{name}" -g radius radius

# TODO: should be in trigger instead.
# upgrade from previous versions of the package, where radius' gid was "nobody"
if [ "`id -g radius`" = "99" ]; then
	usermod -g 29 radius
	chown radius:radius /var/log/%{name}/*.log >/dev/null 2>&1 || :
	chown radius:radius /var/log/%{name}/radacct/* >/dev/null 2>&1 || :
fi

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "%{name} daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove radius
	%groupremove radius
fi

%post   libs -p /sbin/ldconfig                                                                                        
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/* scripts
%dir %{_sysconfdir}/raddb
%attr(771,root,radius) %dir %{_var}/log/freeradius
%attr(771,root,radius) %dir %{_var}/log/freeradius/radacct
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius/radacct
%attr(775,root,radius) %dir /var/run/freeradius
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/freeradius/*.la
%attr(755,root,root) %{_libdir}/freeradius/*.so
%{_datadir}/freeradius
%{_mandir}/man?/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeradius-eap-?.?.?.so
%attr(755,root,root) %{_libdir}/libfreeradius-radius-?.?.?.so
%dir %{_libdir}/freeradius

%files devel
%defattr(644,root,root,755)
%{_includedir}/freeradius
%{_libdir}/libfreeradius-eap.so
%{_libdir}/libfreeradius-radius.so

%files mibs
%defattr(644,root,root,755)
%doc mibs/*.chart
%{mibdir}/*.*
