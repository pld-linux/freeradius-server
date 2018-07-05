#
# Conditional build:
%bcond_without	ldap			# rlm_ldap extension module
%bcond_without	firebird		# rlm_sql_firebird extension module
%bcond_without	eap_ikev2		# rlm_eap_ikev2 extension module
%bcond_without	kerberos5		# rlm_krb5 extension module
%bcond_with	krb5			# use MIT Kerberos instead of heimdal
%bcond_with	oci			# Oracle SQL extension module
%bcond_without	instantclient		# build Oracle SQL extension module against oracle-instantclient package
%bcond_without	redis			# rlm_redis and rlm_rediswho extension modules
%bcond_without	ruby			# rlm_ruby extension module
%bcond_with	failed_calls_acc	# with failed calls accounting support
#
%include	/usr/lib/rpm/macros.perl
#
Summary:	High-performance and highly configurable RADIUS server
Summary(pl.UTF-8):	Szybki i wysoce konfigurowalny serwer RADIUS
Name:		freeradius-server
Version:	2.2.10
Release:	4
License:	GPL v2
Group:		Networking/Daemons/Radius
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.bz2
# Source0-md5:	f1ce12d2b8258585cb3d525f5bdfeb17
Source1:	%{name}.logrotate
Source2:	%{name}.init
Source3:	%{name}.pam
Source4:	%{name}.tmpfiles
Patch0:		%{name}-config.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-makefile.patch
Patch3:		%{name}-rundir.patch
Patch4:		%{name}-heimdal.patch
Patch5:		%{name}-rubyhdrs.patch
# Patch taken from http://download.ag-projects.com/CDRTool/contrib/freeradius-brandinger/
Patch6:		failed_calls_accounting.patch
Patch7:		http://eduroam.pl/Dokumentacja/cui-fr-2.2.0.patch
Patch8:		format-security.patch
Patch9:		am.patch
Patch10:	%{name}-oracle.patch
URL:		http://www.freeradius.org/
%{?with_firebird:BuildRequires:	Firebird-devel}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel
BuildRequires:	gdbm-devel
%if %{with kerberos5} && %{without krb5}
BuildRequires:	heimdal-devel
%endif
%{?with_redis:BuildRequires:	hiredis-devel}
%if %{with kerberos5} && %{with krb5}
BuildRequires:	krb5-devel
%endif
%{?with_eap_ikev2:BuildRequires:	libeap-ikev2-devel}
BuildRequires:	libltdl-devel
BuildRequires:	libpcap-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel
%{?with_oci:%{?with_instantclient:BuildRequires:	oracle-instantclient-devel >= 9}}
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-devel >= 2.3
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_ruby:BuildRequires:	ruby-devel >= 1.8}
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
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssl-tools
Requires:	rc-scripts
Provides:	freeradius = %{version}-%{release}
Provides:	group(radius)
Provides:	user(radius)
Obsoletes:	cistron-radius
Obsoletes:	freeradius < 2.0
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mibdir		%{_datadir}/mibs
%define		filterout_ld	-Wl,--as-needed

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

%package module-krb5
Summary:	Kerberos module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł Kerberos do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-krb5
Kerberos module for FreeRADIUS server.

%description module-krb5 -l pl.UTF-8
Moduł Kerberos do serwera FreeRADIUS.

%package module-ldap
Summary:	LDAP module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł LDAP do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-ldap
LDAP module for FreeRADIUS server.

%description module-ldap -l pl.UTF-8
Moduł LDAP do serwera FreeRADIUS.

%package module-otp
Summary:	OTP module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł OTP do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-otp
OTP module for FreeRADIUS server.

%description module-otp -l pl.UTF-8
Moduł OTP do serwera FreeRADIUS.

%package module-pam
Summary:	PAM module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł PAM do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-pam
PAM module for FreeRADIUS server.

%description module-pam -l pl.UTF-8
Moduł PAM do serwera FreeRADIUS.

%package module-perl
Summary:	Perl module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł Perl do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-perl
Perl module for FreeRADIUS server.

%description module-perl -l pl.UTF-8
Moduł Perl do serwera FreeRADIUS.

%package module-python
Summary:	Python module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł Python do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-python
Python module for FreeRADIUS server.

%description module-python -l pl.UTF-8
Moduł Python do serwera FreeRADIUS.

%package module-redis
Summary:	Redis and RedisWho modules for FreeRADIUS server
Summary(pl.UTF-8):	Moduł Redis i RedisWho do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-redis
Redis and RedisWho modules for FreeRADIUS server.

%description module-redis -l pl.UTF-8
Moduł Redis i RedisWho do serwera FreeRADIUS.

%package module-ruby
Summary:	Ruby module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł Ruby do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-ruby
Ruby module for FreeRADIUS server.

%description module-ruby -l pl.UTF-8
Moduł Ruby do serwera FreeRADIUS.

%package module-sql-firebird
Summary:	Firebird driver for FreeRADIUS server SQL module
Summary(pl.UTF-8):	Sterownik Firebird dla modułu SQL serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}
Obsoletes:	freeradius-server-module-sql_firebird

%description module-sql-firebird
Firebird driver for FreeRADIUS server SQL module.

%description module-sql-firebird -l pl.UTF-8
Sterownik Firebird dla modułu SQL serwera FreeRADIUS.

%package module-sql-mysql
Summary:	MySQL driver for FreeRADIUS server SQL module
Summary(pl.UTF-8):	Sterownik MySQL dla modułu SQL serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}
Obsoletes:	freeradius-server-module-mysql

%description module-sql-mysql
MySQL driver for FreeRADIUS server SQL module.

%description module-sql-mysql -l pl.UTF-8
Sterownik MySQL dla modułu SQL serwera FreeRADIUS.

%package module-sql-oracle
Summary:	Oracle driver for FreeRADIUS server SQL module
Summary(pl.UTF-8):	Sterownik Oracle dla modułu SQL serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-sql-oracle
Oracle driver for FreeRADIUS server SQL module.

%description module-sql-oracle -l pl.UTF-8
Sterownik Oracle dla modułu SQL serwera FreeRADIUS.

%package module-sql-postgresql
Summary:	PostgreSQL driver for FreeRADIUS server SQL module
Summary(pl.UTF-8):	Sterownik PostgreSQL dla modułu SQL serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}
Obsoletes:	freeradius-server-module-postgresql

%description module-sql-postgresql
PostgreSQL driver for FreeRADIUS server SQL module.

%description module-sql-postgresql -l pl.UTF-8
Sterownik PostgreSQL dla modułu SQL serwera FreeRADIUS.

%package module-sql-sqlite
Summary:	SQLite driver for FreeRADIUS server SQL module
Summary(pl.UTF-8):	Sterownik SQLite dla modułu SQL serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}
Obsoletes:	freeradius-server-module-sqlite

%description module-sql-sqlite
SQLite driver for FreeRADIUS server SQL module.

%description module-sql-sqlite -l pl.UTF-8
Sterownik SQLite dla modułu SQL serwera FreeRADIUS.

%package module-sql-unixodbc
Summary:	UnixODBC driver for FreeRADIUS server SQL module
Summary(pl.UTF-8):	Sterownik UnixODBC dla modułu SQL serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}
Obsoletes:	freeradius-server-module-unixodbc

%description module-sql-unixodbc
UnixODBC driver for FreeRADIUS server SQL module.

%description module-sql-unixodbc -l pl.UTF-8
Sterownik UnixODBC dla modułu SQL serwera FreeRADIUS.

%package module-unix
Summary:	Unix module for FreeRADIUS server
Summary(pl.UTF-8):	Moduł Unix do serwera FreeRADIUS
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-unix
Unix module for FreeRADIUS server.

%description module-unix -l pl.UTF-8
Moduł Unix do serwera FreeRADIUS.

%package libs
Summary:	FreeRADIUS server libraries
Summary(pl.UTF-8):	Biblioteki serwera FreeRADIUS
License:	LGPL v2 (libfreeradius-radius), GPL v2 (libfreeradius-eap)
Group:		Libraries

%description libs
FreeRADIUS server libraries.

%description libs -l pl.UTF-8
Biblioteki serwera FreeRADIUS.

%package devel
Summary:	Header files for FreeRADIUS server libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek serwera FreeRADIUS
License:	LGPL v2 (libfreeradius-radius), GPL v2 (libfreeradius-eap)
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for FreeRADIUS server libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek serwera FreeRADIUS.

%package -n mibs-%{name}
Summary:	MIB database for FreeRADIUS server
Summary(pl.UTF-8):	Baza danych MIB dla serwera FreeRADIUS
Group:		Applications/System
Requires:	mibs-dirs
Suggests:	libsmi
Obsoletes:	freeradius-server-mibs

%description -n mibs-%{name}
MIB database for FreeRADIUS server.

%description -n mibs-%{name} -l pl.UTF-8
Baza danych MIB dla serwera FreeRADIUS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%{?with_failed_calls_acc:%patch6 -p0}
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%{__rm} aclocal.m4 libtool.m4

%build
# Keep it for future when ac/am regeneration will be ok
TOPDIR="$(pwd)"
find -name 'configure.[ia][nc]' -type f | while read FILE; do
	cd $(dirname "$FILE")
	grep -q 'A[CM]_PROG_LIBTOOL' configure.[ia][nc] && %{__libtoolize}
	%{__aclocal} -I "$TOPDIR"
	%{__autoconf}
	[ -f config.h.in ] && %{__autoheader}
	cd -
done

# NOTE:
# system-libtool conflicts with --disable-static
# rlm_opendirectory is Mac OS specific
# rlm_sql_db2 requires proprietary library (IBM DB2 SDK)
# rlm_sql_iodbc disabled because libiodbc-devel conflicts with unixODBC-devel
%configure \
	SNMPGET=/usr/bin/snmpget \
	SNMPWALK=/usr/bin/snmpwalk \
	ac_cv_lib_nsl_inet_ntoa=no \
	ac_cv_lib_resolv_inet_aton=no \
	--disable-static \
	%{!?with_krb5:--enable-heimdal-krb5} \
	--enable-strict-dependencies \
	--with-experimental-modules \
	--with-logdir=%{_var}/log/freeradius \
	%{?with_instantclient:--with-oracle-include-dir=/usr/include/oracle/client} \
	--with-system-libltdl \
	--with-udpfromto \
	%{!?with_eap_ikev2:--without-rlm_eap_ikev2} \
	--without-rlm_eap_tnc \
	%{!?with_kerberos5:--without-rlm_krb5} \
	%{!?with_ldap:--without-rlm_ldap} \
	--without-rlm_opendirectory \
	%{!?with_redis:--without-rlm_redis} \
	%{!?with_redis:--without-rlm_rediswho} \
	%{!?with_ruby:--without-rlm_ruby} \
	--without-rlm_sql_db2 \
	%{!?with_firebird:--without-rlm_sql_firebird} \
	--without-rlm_sql_iodbc \
	%{!?with_oci:--without-rlm_sql_oracle}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d} \
	$RPM_BUILD_ROOT%{_var}/log/{,archive}/freeradius/radacct \
	$RPM_BUILD_ROOT%{mibdir} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} -j1 install \
	R=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE4} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

# Install mibs:
install mibs/FREERADIUS-*.txt $RPM_BUILD_ROOT%{mibdir}

# Cleanups:
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{_sbindir}/rc.*
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/freeradius \
	%{!?with_oci:$RPM_BUILD_ROOT%{_sysconfdir}/raddb/sql/oracle}

# prepare cleaned up docs for rpm
install -d docs-rpm
cp -a doc scripts docs-rpm
%{__rm} docs-rpm/doc/{.gitignore,CYGWIN.rst,DIFFS.rst,MACOSX,OS2,Makefile*,examples/Makefile,rfc/{Makefile,update.sh,*.pl}}
%{__rm} docs-rpm/scripts/{.gitignore,Makefile,*.in,radsqlrelay,radwatch,raddebug,cryptpasswd}
%{__rm} -r docs-rpm/scripts/solaris

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

%define module_scripts() \
%post %1 \
%service %{name} restart \
\
%postun %1 \
%service %{name} restart

%module_scripts module-krb5
%module_scripts module-ldap
%module_scripts module-otp
%module_scripts module-pam
%module_scripts module-perl
%module_scripts module-python
%module_scripts module-redis
%module_scripts module-ruby
%module_scripts module-sql-firebird
%module_scripts module-sql-mysql
%module_scripts module-sql-oracle
%module_scripts module-sql-postgresql
%module_scripts module-sql-sqlite
%module_scripts module-sql-unixodbc
%module_scripts module-unix

%files
%defattr(644,root,root,755)
%doc COPYRIGHT CREDITS README.rst docs-rpm/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/freeradius-server
%attr(754,root,root) /etc/rc.d/init.d/freeradius-server
%attr(755,root,root) %{_bindir}/rad_counter
%attr(755,root,root) %{_bindir}/radclient
%attr(755,root,root) %{_bindir}/radconf2xml
%attr(755,root,root) %{_bindir}/radcrypt
%attr(755,root,root) %{_bindir}/radeapclient
%attr(755,root,root) %{_bindir}/radlast
%attr(755,root,root) %{_bindir}/radsniff
%attr(755,root,root) %{_bindir}/radsqlrelay
%attr(755,root,root) %{_bindir}/radtest
%attr(755,root,root) %{_bindir}/radwho
%attr(755,root,root) %{_bindir}/radzap
%attr(755,root,root) %{_bindir}/rlm_dbm_cat
%attr(755,root,root) %{_bindir}/rlm_dbm_parser
%attr(755,root,root) %{_bindir}/rlm_ippool_tool
%attr(755,root,root) %{_bindir}/smbencrypt
%attr(755,root,root) %{_sbindir}/checkrad
%attr(755,root,root) %{_sbindir}/raddebug
%attr(755,root,root) %{_sbindir}/radiusd
%attr(755,root,root) %{_sbindir}/radmin
%attr(755,root,root) %{_sbindir}/radwatch
%dir %{_libdir}/freeradius
%attr(755,root,root) %{_libdir}/freeradius/rlm_acctlog*.so
%{_libdir}/freeradius/rlm_acctlog*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_acct_unique*.so
%{_libdir}/freeradius/rlm_acct_unique*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_always*.so
%{_libdir}/freeradius/rlm_always*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_attr_filter*.so
%{_libdir}/freeradius/rlm_attr_filter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_attr_rewrite*.so
%{_libdir}/freeradius/rlm_attr_rewrite*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_cache*.so
%{_libdir}/freeradius/rlm_cache*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_caching*.so
%{_libdir}/freeradius/rlm_caching*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_chap*.so
%{_libdir}/freeradius/rlm_chap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_checkval*.so
%{_libdir}/freeradius/rlm_checkval*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_copy_packet*.so
%{_libdir}/freeradius/rlm_copy_packet*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_counter*.so
%{_libdir}/freeradius/rlm_counter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_cram*.so
%{_libdir}/freeradius/rlm_cram*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_dbm*.so
%{_libdir}/freeradius/rlm_dbm*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_detail*.so
%{_libdir}/freeradius/rlm_detail*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_digest*.so
%{_libdir}/freeradius/rlm_digest*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_dynamic_clients*.so
%{_libdir}/freeradius/rlm_dynamic_clients*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_eap*.so
%{_libdir}/freeradius/rlm_eap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_example*.so
%{_libdir}/freeradius/rlm_example*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_exec*.so
%{_libdir}/freeradius/rlm_exec*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_expiration*.so
%{_libdir}/freeradius/rlm_expiration*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_expr*.so
%{_libdir}/freeradius/rlm_expr*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_fastusers*.so
%{_libdir}/freeradius/rlm_fastusers*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_files*.so
%{_libdir}/freeradius/rlm_files*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_ippool*.so
%{_libdir}/freeradius/rlm_ippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_jradius*.so
%{_libdir}/freeradius/rlm_jradius*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_linelog*.so
%{_libdir}/freeradius/rlm_linelog*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_logintime*.so
%{_libdir}/freeradius/rlm_logintime*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_mschap*.so
%{_libdir}/freeradius/rlm_mschap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_pap*.so
%{_libdir}/freeradius/rlm_pap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_passwd*.so
%{_libdir}/freeradius/rlm_passwd*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_policy*.so
%{_libdir}/freeradius/rlm_policy*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_preprocess*.so
%{_libdir}/freeradius/rlm_preprocess*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_protocol_filter*.so
%{_libdir}/freeradius/rlm_protocol_filter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_radutmp*.so
%{_libdir}/freeradius/rlm_radutmp*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_realm*.so
%{_libdir}/freeradius/rlm_realm*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_replicate*.so
%{_libdir}/freeradius/rlm_replicate*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sim_files*.so
%{_libdir}/freeradius/rlm_sim_files*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_smsotp*.so
%{_libdir}/freeradius/rlm_smsotp*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_soh*.so
%{_libdir}/freeradius/rlm_soh*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql-%{version}.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql.so
%{_libdir}/freeradius/rlm_sql-%{version}.la
%{_libdir}/freeradius/rlm_sql.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlcounter*.so
%{_libdir}/freeradius/rlm_sqlcounter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlhpwippool*.so
%{_libdir}/freeradius/rlm_sqlhpwippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlippool*.so
%{_libdir}/freeradius/rlm_sqlippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_log*.so
%{_libdir}/freeradius/rlm_sql_log*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_wimax*.so
%{_libdir}/freeradius/rlm_wimax*.la
%{_datadir}/freeradius
%{_mandir}/man1/radclient.1*
%{_mandir}/man1/radeapclient.1*
%{_mandir}/man1/radlast.1*
%{_mandir}/man1/radtest.1*
%{_mandir}/man1/radwho.1*
%{_mandir}/man1/radzap.1*
%{_mandir}/man1/smbencrypt.1*
%{_mandir}/man5/acct_users.5*
%{_mandir}/man5/checkrad.5*
%{_mandir}/man5/clients.conf.5*
%{_mandir}/man5/dictionary.5*
%{_mandir}/man5/radiusd.conf.5*
%{_mandir}/man5/radrelay.conf.5*
%{_mandir}/man5/rlm_acct_unique.5*
%{_mandir}/man5/rlm_always.5*
%{_mandir}/man5/rlm_attr_filter.5*
%{_mandir}/man5/rlm_attr_rewrite.5*
%{_mandir}/man5/rlm_chap.5*
%{_mandir}/man5/rlm_counter.5*
%{_mandir}/man5/rlm_detail.5*
%{_mandir}/man5/rlm_digest.5*
%{_mandir}/man5/rlm_expr.5*
%{_mandir}/man5/rlm_files.5*
%{_mandir}/man5/rlm_mschap.5*
%{_mandir}/man5/rlm_pap.5*
%{_mandir}/man5/rlm_passwd.5*
%{_mandir}/man5/rlm_policy.5*
%{_mandir}/man5/rlm_realm.5*
%{_mandir}/man5/rlm_sql.5*
%{_mandir}/man5/rlm_sql_log.5*
%{_mandir}/man5/unlang.5*
%{_mandir}/man5/users.5*
%{_mandir}/man8/radconf2xml.8*
%{_mandir}/man8/radcrypt.8*
%{_mandir}/man8/raddebug.8*
%{_mandir}/man8/radiusd.8*
%{_mandir}/man8/radmin.8*
%{_mandir}/man8/radrelay.8*
%{_mandir}/man8/radsniff.8*
%{_mandir}/man8/radsqlrelay.8*
%{_mandir}/man8/radwatch.8*
%{_mandir}/man8/rlm_dbm_cat.8*
%{_mandir}/man8/rlm_dbm_parser.8*
%{_mandir}/man8/rlm_ippool_tool.8*
%attr(771,root,radius) %dir %{_var}/log/freeradius
%attr(771,root,radius) %dir %{_var}/log/freeradius/radacct
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius/radacct
%attr(775,root,radius) %dir /var/run/freeradius
/usr/lib/tmpfiles.d/%{name}.conf
%defattr(640,root,radius,750)
%dir %{_sysconfdir}/raddb
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/acct_users
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/attrs*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/clients.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/dictionary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/eap.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/experimental.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/hints
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/huntgroups
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/panic.gdb
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/preproxy_users
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/proxy.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/radiusd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sqlippool.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/templates.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/users
%dir %{_sysconfdir}/raddb/certs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/*.cnf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/xpextensions
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/Makefile
%doc %{_sysconfdir}/raddb/certs/README
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/bootstrap
%dir %{_sysconfdir}/raddb/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/acct_unique
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/always
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/attr_filter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/attr_rewrite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/chap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/checkval
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/counter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/cui
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/detail
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/detail.example.com
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/detail.log
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/dhcp_sqlippool
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/digest
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/dynamic_clients
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/echo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/etc_group
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/exec
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/expiration
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/expr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/files
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/inner-eap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/ippool
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/linelog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/logintime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/mac2ip
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/mac2vlan
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/mschap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/ntlm_auth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/opendirectory
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/pap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/passwd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/policy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/preprocess
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/radutmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/radrelay
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/realm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/replicate
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/smbpasswd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/smsotp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/soh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/sql_log
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/sqlcounter_expire_on_login
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/sradutmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/wimax
%dir %{_sysconfdir}/raddb/sites-available
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sites-available/*
%dir %{_sysconfdir}/raddb/sites-enabled
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sites-enabled/*
%dir %{_sysconfdir}/raddb/sql
%dir %{_sysconfdir}/raddb/sql/mssql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql/mssql/*
%dir %{_sysconfdir}/raddb/sql/ndb
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql/ndb/*

%if %{with kerberos5}
%files module-krb5
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/krb5
%attr(755,root,root) %{_libdir}/freeradius/rlm_krb5*.so
%{_libdir}/freeradius/rlm_krb5*.la
%endif

%if %{with ldap}
%files module-ldap
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/ldap.attrmap
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/ldap
%attr(755,root,root) %{_libdir}/freeradius/rlm_ldap*.so
%{_libdir}/freeradius/rlm_ldap*.la
%endif

%files module-otp
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/otp
%attr(755,root,root) %{_libdir}/freeradius/rlm_otp*.so
%{_libdir}/freeradius/rlm_otp*.la

%files module-pam
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/pam
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/radius
%attr(755,root,root) %{_libdir}/freeradius/rlm_pam*.so
%{_libdir}/freeradius/rlm_pam*.la

%files module-perl
%defattr(644,root,root,755)
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/example.pl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/perl
%attr(755,root,root) %{_libdir}/freeradius/rlm_perl*.so
%{_libdir}/freeradius/rlm_perl*.la

%files module-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_python*.so
%{_libdir}/freeradius/rlm_python*.la

%if %{with redis}
%files module-redis
%defattr(644,root,root,755)
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/redis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/rediswho
%attr(755,root,root) %{_libdir}/freeradius/rlm_redis-%{version}.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_redis.so
%{_libdir}/freeradius/rlm_redis-%{version}.la
%{_libdir}/freeradius/rlm_redis.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_rediswho-%{version}.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_rediswho.so
%{_libdir}/freeradius/rlm_rediswho-%{version}.la
%{_libdir}/freeradius/rlm_rediswho.la
%endif

%if %{with ruby}
%files module-ruby
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_ruby*.so
%{_libdir}/freeradius/rlm_ruby*.la
%endif

%if %{with firebird}
%files module-sql-firebird
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_firebird*.so
%{_libdir}/freeradius/rlm_sql_firebird*.la
%endif

%files module-sql-mysql
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/sql/mysql
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql/mysql/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_mysql*.so
%{_libdir}/freeradius/rlm_sql_mysql*.la

%if %{with oci}
%files module-sql-oracle
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/sql/oracle
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql/oracle/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_oracle*.so
%{_libdir}/freeradius/rlm_sql_oracle*.la
%endif

%files module-sql-postgresql
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/sql/postgresql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql/postgresql/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_postgresql*.so
%{_libdir}/freeradius/rlm_sql_postgresql*.la

%files module-sql-sqlite
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_sqlite*.so
%{_libdir}/freeradius/rlm_sql_sqlite*.la

%files module-sql-unixodbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_unixodbc*.so
%{_libdir}/freeradius/rlm_sql_unixodbc*.la

%files module-unix
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/modules/unix
%attr(755,root,root) %{_libdir}/freeradius/rlm_unix*.so
%{_libdir}/freeradius/rlm_unix*.la
%{_mandir}/man5/rlm_unix.5*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeradius-eap-%{version}.so
%attr(755,root,root) %{_libdir}/libfreeradius-radius-??????.so
%dir %{_libdir}/freeradius

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeradius-eap.so
%attr(755,root,root) %{_libdir}/libfreeradius-radius.so
%{_includedir}/freeradius

%files -n mibs-%{name}
%defattr(644,root,root,755)
%doc mibs/RADIUS-*.chart
%{mibdir}/FREERADIUS-PRODUCT-RADIUSD-MIB.txt
%{mibdir}/FREERADIUS-SMI.txt
