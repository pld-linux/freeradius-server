#
# Conditional build:
%bcond_without	ldap			# rlm_ldap extension module
%bcond_without	firebird		# rlm_sql_firebird extension module
%bcond_with	eap_ikev2		# rlm_eap_ikev2 extension module
%bcond_without	kerberos5		# rlm_krb5 extension module
%bcond_with	krb5			# use MIT Kerberos instead of heimdal
%bcond_with	oci			# Oracle SQL extension module
%bcond_without	instantclient		# build Oracle SQL extension module against oracle-instantclient package
%bcond_without	redis			# rlm_redis and rlm_rediswho extension modules
%bcond_without	ruby			# rlm_ruby extension module
#
#
Summary:	High-performance and highly configurable RADIUS server
Summary(pl.UTF-8):	Szybki i wysoce konfigurowalny serwer RADIUS
Name:		freeradius-server
Version:	3.0.17
Release:	7
License:	GPL v2
Group:		Networking/Daemons/Radius
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.bz2
# Source0-md5:	1f4ad38f32101a7d50d818afa6f17339
Source1:	%{name}.logrotate
Source2:	%{name}.init
Source3:	%{name}.pam
Source4:	%{name}.tmpfiles
Patch0:		%{name}-config.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-rundir.patch
Patch3:		aclocal.patch
URL:		http://www.freeradius.org/
%{?with_firebird:BuildRequires:	Firebird-devel}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel
BuildRequires:	freetds-devel
BuildRequires:	gdbm-devel
%if %{with kerberos5} && %{without krb5}
BuildRequires:	heimdal-devel
%endif
%{?with_redis:BuildRequires:	hiredis-devel}
BuildRequires:	json-c-devel
%if %{with kerberos5} && %{with krb5}
BuildRequires:	krb5-devel
%endif
%{?with_eap_ikev2:BuildRequires:	libeap-ikev2-devel >= 0.2.1-5}
BuildRequires:	libltdl-devel
BuildRequires:	libmemcached-devel
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
BuildRequires:	talloc-devel
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
Obsoletes:	freeradius-server-module-unix < 3.0
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

%build
# Keep it for future when ac/am regeneration will be ok
TOPDIR="$(pwd)"
find -name 'configure.[ia][nc]' -type f | while read FILE; do
	cd $(dirname "$FILE")
	grep -q 'A[CM]_PROG_LIBTOOL' configure.[ia][nc] && %{__libtoolize}
	%{__aclocal} -I "$TOPDIR" -I "$TOPDIR/m4" $(if [ -d m4 ] ; then echo "-I m4" ; fi)
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
	%{!?with_oci:--without-rlm_sql_oracle} \
	--without-rlm_couchbase \
	--without-rlm_securid

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,pam.d} \
	$RPM_BUILD_ROOT%{_var}/log/{,archive}/freeradius/radacct \
	$RPM_BUILD_ROOT/var/run/freeradius \
	$RPM_BUILD_ROOT%{mibdir} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} -j1 install \
	R=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/radius
install %{SOURCE4} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

# Install mibs:
install mibs/FREERADIUS-*.mib $RPM_BUILD_ROOT%{mibdir}

# Cleanups:
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{_sbindir}/rc.*
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/freeradius

%if %{without oci}
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}/raddb/mods-config/sql/*/oracle
%endif
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}/raddb/mods-config/sql/*/mssql

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}{,/freeradius}/*.a

# prepare cleaned up docs for rpm
install -d docs-rpm
cp -a doc scripts docs-rpm
%{__rm} docs-rpm/doc/{.gitignore,Makefile*,rfc/{Makefile,update.sh,*.pl}}
%{__rm} docs-rpm/scripts/{.gitignore,*.in,raddebug,cryptpasswd}
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
if [ ! -e /etc/raddb/certs/server.pem ] ; then
	cd /etc/raddb/certs
	make client.key || : # otherwise it doesn't work
	./bootstrap || :
	chown root:radius * || :
	chmod 640 * || :
fi

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

%files
%defattr(644,root,root,755)
%doc COPYRIGHT CREDITS README.rst docs-rpm/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/freeradius-server
%attr(754,root,root) /etc/rc.d/init.d/freeradius-server
%attr(755,root,root) %{_bindir}/dhcpclient
%attr(755,root,root) %{_bindir}/map_unit
%attr(755,root,root) %{_bindir}/rad_counter
%attr(755,root,root) %{_bindir}/radattr
%attr(755,root,root) %{_bindir}/radclient
%attr(755,root,root) %{_bindir}/radcrypt
%attr(755,root,root) %{_bindir}/radeapclient
%attr(755,root,root) %{_bindir}/radlast
%attr(755,root,root) %{_bindir}/radsniff
%attr(755,root,root) %{_bindir}/radsqlrelay
%attr(755,root,root) %{_bindir}/radtest
%attr(755,root,root) %{_bindir}/radwho
%attr(755,root,root) %{_bindir}/radzap
%attr(755,root,root) %{_bindir}/rlm_ippool_tool
%attr(755,root,root) %{_bindir}/smbencrypt
%attr(755,root,root) %{_sbindir}/checkrad
%attr(755,root,root) %{_sbindir}/raddebug
%attr(755,root,root) %{_sbindir}/radiusd
%attr(755,root,root) %{_sbindir}/radmin
%dir %{_libdir}/freeradius
%attr(755,root,root) %{_libdir}/freeradius/proto_dhcp*.so
%{_libdir}/freeradius/proto_dhcp*.la
%attr(755,root,root) %{_libdir}/freeradius/proto_vmps*.so
%{_libdir}/freeradius/proto_vmps*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_always*.so
%{_libdir}/freeradius/rlm_always*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_attr_filter*.so
%{_libdir}/freeradius/rlm_attr_filter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_cache*.so
%{_libdir}/freeradius/rlm_cache*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_chap*.so
%{_libdir}/freeradius/rlm_chap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_counter*.so
%{_libdir}/freeradius/rlm_counter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_cram*.so
%{_libdir}/freeradius/rlm_cram*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_date*.so
%{_libdir}/freeradius/rlm_date*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_detail*.so
%{_libdir}/freeradius/rlm_detail*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_dhcp*.so
%{_libdir}/freeradius/rlm_dhcp*.la
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
%attr(755,root,root) %{_libdir}/freeradius/rlm_files*.so
%{_libdir}/freeradius/rlm_files*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_idn*.so
%{_libdir}/freeradius/rlm_idn*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_ippool*.so
%{_libdir}/freeradius/rlm_ippool*.la
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
%attr(755,root,root) %{_libdir}/freeradius/rlm_preprocess*.so
%{_libdir}/freeradius/rlm_preprocess*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_radutmp*.so
%{_libdir}/freeradius/rlm_radutmp*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_realm*.so
%{_libdir}/freeradius/rlm_realm*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_replicate*.so
%{_libdir}/freeradius/rlm_replicate*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_rest*.so
%{_libdir}/freeradius/rlm_rest*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_smsotp*.so
%{_libdir}/freeradius/rlm_smsotp*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_soh*.so
%{_libdir}/freeradius/rlm_soh*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sometimes*.so
%{_libdir}/freeradius/rlm_sometimes*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql.so
%{_libdir}/freeradius/rlm_sql.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_freetds*.so
%{_libdir}/freeradius/rlm_sql_freetds*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_null*.so
%{_libdir}/freeradius/rlm_sql_null*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlcounter*.so
%{_libdir}/freeradius/rlm_sqlcounter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlhpwippool*.so
%{_libdir}/freeradius/rlm_sqlhpwippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlippool*.so
%{_libdir}/freeradius/rlm_sqlippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_test*.so
%{_libdir}/freeradius/rlm_test*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_unbound*.so
%{_libdir}/freeradius/rlm_unbound*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_unix*.so
%{_libdir}/freeradius/rlm_unix*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_unpack*.so
%{_libdir}/freeradius/rlm_unpack*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_utf8*.so
%{_libdir}/freeradius/rlm_utf8*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_wimax*.so
%{_libdir}/freeradius/rlm_wimax*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_yubikey*.so
%{_libdir}/freeradius/rlm_yubikey*.la
%{_datadir}/freeradius
%{_mandir}/man1/dhcpclient.1*
%{_mandir}/man1/rad_counter.1*
%{_mandir}/man1/radclient.1*
%{_mandir}/man1/radeapclient.1*
%{_mandir}/man1/radlast.1*
%{_mandir}/man1/radtest.1*
%{_mandir}/man1/radwho.1*
%{_mandir}/man1/radzap.1*
%{_mandir}/man1/smbencrypt.1*
%{_mandir}/man5/checkrad.5*
%{_mandir}/man5/clients.conf.5*
%{_mandir}/man5/dictionary.5*
%{_mandir}/man5/radiusd.conf.5*
%{_mandir}/man5/radrelay.conf.5*
%{_mandir}/man5/rlm_always.5*
%{_mandir}/man5/rlm_attr_filter.5*
%{_mandir}/man5/rlm_chap.5*
%{_mandir}/man5/rlm_counter.5*
%{_mandir}/man5/rlm_detail.5*
%{_mandir}/man5/rlm_digest.5*
%{_mandir}/man5/rlm_expr.5*
%{_mandir}/man5/rlm_files.5*
%{_mandir}/man5/rlm_idn.5*
%{_mandir}/man5/rlm_mschap.5*
%{_mandir}/man5/rlm_pap.5*
%{_mandir}/man5/rlm_passwd.5*
%{_mandir}/man5/rlm_realm.5*
%{_mandir}/man5/rlm_sql.5*
%{_mandir}/man5/rlm_unbound.5*
%{_mandir}/man5/rlm_unix.5*
%{_mandir}/man5/unlang.5*
%{_mandir}/man5/users.5*
%{_mandir}/man8/radcrypt.8*
%{_mandir}/man8/raddebug.8*
%{_mandir}/man8/radiusd.8*
%{_mandir}/man8/radmin.8*
%{_mandir}/man8/radrelay.8*
%{_mandir}/man8/radsniff.8*
%{_mandir}/man8/radsqlrelay.8*
%{_mandir}/man8/rlm_ippool_tool.8*
%attr(771,root,radius) %dir %{_var}/log/freeradius
%attr(771,root,radius) %dir %{_var}/log/freeradius/radacct
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius/radacct
%attr(775,root,radius) %dir /var/run/freeradius
/usr/lib/tmpfiles.d/%{name}.conf
%defattr(640,root,radius,750)
%dir %{_sysconfdir}/raddb
%doc %{_sysconfdir}/raddb/README.rst
%dir %{_sysconfdir}/raddb/certs
%{_sysconfdir}/raddb/certs/Makefile
%doc %{_sysconfdir}/raddb/certs/README
%ghost %{_sysconfdir}/raddb/certs/01.pem
%ghost %{_sysconfdir}/raddb/certs/02.pem
%attr(755,root,root) %{_sysconfdir}/raddb/certs/bootstrap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/ca.cnf
%ghost %{_sysconfdir}/raddb/certs/ca.der
%ghost %{_sysconfdir}/raddb/certs/ca.key
%ghost %{_sysconfdir}/raddb/certs/ca.pem
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/client.cnf
%ghost %{_sysconfdir}/raddb/certs/client.crt
%{_sysconfdir}/raddb/certs/client.csr
%ghost %{_sysconfdir}/raddb/certs/client.key
%ghost %{_sysconfdir}/raddb/certs/client.p12
%ghost %{_sysconfdir}/raddb/certs/client.pem
%ghost %{_sysconfdir}/raddb/certs/dh
%ghost %{_sysconfdir}/raddb/certs/index.txt
%ghost %{_sysconfdir}/raddb/certs/index.txt.attr
%ghost %{_sysconfdir}/raddb/certs/index.txt.attr.old
%ghost %{_sysconfdir}/raddb/certs/index.txt.old
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/inner-server.cnf
%{_sysconfdir}/raddb/certs/passwords.mk
%ghost %{_sysconfdir}/raddb/certs/serial
%ghost %{_sysconfdir}/raddb/certs/serial.old
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/server.cnf
%ghost %{_sysconfdir}/raddb/certs/server.crt
%ghost %{_sysconfdir}/raddb/certs/server.csr
%ghost %{_sysconfdir}/raddb/certs/server.key
%ghost %{_sysconfdir}/raddb/certs/server.p12
%ghost %{_sysconfdir}/raddb/certs/server.pem
%ghost %{_sysconfdir}/raddb/certs/user@example.org.pem
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/certs/xpextensions
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/clients.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/dictionary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/experimental.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/hints
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/huntgroups
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/panic.gdb
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/proxy.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/radiusd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/templates.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/users
%dir %{_sysconfdir}/raddb/mods-available
%doc %{_sysconfdir}/raddb/mods-available/README.rst
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/abfab_psk_sql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/always
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/attr_filter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/cache_eap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/chap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/couchbase
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/counter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/cui
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/date
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/detail
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/detail.example.com
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/detail.log
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/dhcp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/dhcp_sqlippool
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/digest
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/dynamic_clients
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/eap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/echo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/etc_group
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/exec
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/expiration
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/expr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/files
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/idn
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/inner-eap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/ippool
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/linelog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/logintime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/mac2ip
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/mac2vlan
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/moonshot-targeted-ids
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/mschap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/ntlm_auth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/opendirectory
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/pap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/passwd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/preprocess
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/radutmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/realm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/replicate
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/rest
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/smbpasswd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/smsotp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/soh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/sometimes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/sql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/sqlcounter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/sqlippool
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/sradutmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/unbound
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/unix
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/unpack
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/utf8
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/wimax
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/yubikey
%dir %{_sysconfdir}/raddb/mods-config
%doc %{_sysconfdir}/raddb/mods-config/README.rst
%dir %{_sysconfdir}/raddb/mods-config/attr_filter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/attr_filter/access_challenge
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/attr_filter/access_reject
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/attr_filter/accounting_response
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/attr_filter/post-proxy
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/attr_filter/pre-proxy
%dir %{_sysconfdir}/raddb/mods-config/files
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/files/accounting
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/files/authorize
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/files/pre-proxy
%dir %{_sysconfdir}/raddb/mods-config/preprocess
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/preprocess/hints
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/preprocess/huntgroups
%dir %{_sysconfdir}/raddb/mods-config/sql
%dir %{_sysconfdir}/raddb/mods-config/sql/counter
%dir %{_sysconfdir}/raddb/mods-config/sql/cui
%dir %{_sysconfdir}/raddb/mods-config/sql/ippool
%dir %{_sysconfdir}/raddb/mods-config/sql/ippool-dhcp
%dir %{_sysconfdir}/raddb/mods-config/sql/main
%dir %{_sysconfdir}/raddb/mods-config/sql/moonshot-targeted-ids
%dir %{_sysconfdir}/raddb/mods-config/unbound
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/unbound/default.conf
%dir %{_sysconfdir}/raddb/mods-enabled
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/always
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/attr_filter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/cache_eap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/chap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/date
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/detail
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/detail.log
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/digest
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/dynamic_clients
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/eap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/echo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/exec
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/expiration
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/expr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/files
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/linelog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/logintime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/mschap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/ntlm_auth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/pap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/passwd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/preprocess
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/radutmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/realm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/replicate
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/soh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/sradutmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/unix
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/unpack
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-enabled/utf8
%dir %{_sysconfdir}/raddb/policy.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/abfab-tr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/accounting
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/canonicalization
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/control
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/cui
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/debug
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/dhcp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/eap
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/filter
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/moonshot-targeted-ids
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/policy.d/operator-name
%dir %{_sysconfdir}/raddb/sites-available
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sites-available/*
%dir %{_sysconfdir}/raddb/sites-enabled
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sites-enabled/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/trigger.conf

%if %{with kerberos5}
%files module-krb5
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/krb5
%attr(755,root,root) %{_libdir}/freeradius/rlm_krb5*.so
%{_libdir}/freeradius/rlm_krb5*.la
%endif

%if %{with ldap}
%files module-ldap
%defattr(644,root,root,755)
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/ldap
%attr(755,root,root) %{_libdir}/freeradius/rlm_ldap*.so
%{_libdir}/freeradius/rlm_ldap*.la
%endif

%files module-otp
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/otp
%attr(755,root,root) %{_libdir}/freeradius/rlm_otp*.so
%{_libdir}/freeradius/rlm_otp*.la

%files module-pam
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/pam
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/radius
%attr(755,root,root) %{_libdir}/freeradius/rlm_pam*.so
%{_libdir}/freeradius/rlm_pam*.la

%files module-perl
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/mods-config/perl
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/perl/example.pl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/perl
%attr(755,root,root) %{_libdir}/freeradius/rlm_perl*.so
%{_libdir}/freeradius/rlm_perl*.la

%files module-python
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/mods-config/python
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/python
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/python/example.py
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/python/radiusd.py
%attr(755,root,root) %{_libdir}/freeradius/rlm_python*.so
%{_libdir}/freeradius/rlm_python*.la

%if %{with redis}
%files module-redis
%defattr(644,root,root,755)
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/redis
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-available/rediswho
%attr(755,root,root) %{_libdir}/freeradius/rlm_redis.so
%{_libdir}/freeradius/rlm_redis.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_rediswho.so
%{_libdir}/freeradius/rlm_rediswho.la
%endif

%if %{with ruby}
%files module-ruby
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/mods-config/ruby
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/ruby/example.rb
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
%dir %{_sysconfdir}/raddb/mods-config/sql/*/mysql
%dir %{_sysconfdir}/raddb/mods-config/sql/*/ndb
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/sql/*/mysql/*
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/sql/*/ndb/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_mysql*.so
%{_libdir}/freeradius/rlm_sql_mysql*.la

%if %{with oci}
%files module-sql-oracle
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/mods-config/sql/*/oracle
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/sql/*/oracle/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_oracle*.so
%{_libdir}/freeradius/rlm_sql_oracle*.la
%endif

%files module-sql-postgresql
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/mods-config/sql/*/postgresql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/sql/*/postgresql/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_postgresql*.so
%{_libdir}/freeradius/rlm_sql_postgresql*.la

%files module-sql-sqlite
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/mods-config/sql/*/sqlite
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/mods-config/sql/*/sqlite/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_sqlite*.so
%{_libdir}/freeradius/rlm_sql_sqlite*.la

%files module-sql-unixodbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_unixodbc*.so
%{_libdir}/freeradius/rlm_sql_unixodbc*.la

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeradius-dhcp.so
%attr(755,root,root) %{_libdir}/libfreeradius-eap.so
%attr(755,root,root) %{_libdir}/libfreeradius-radius.so
%attr(755,root,root) %{_libdir}/libfreeradius-server.so
%dir %{_libdir}/freeradius

%files devel
%defattr(644,root,root,755)
%{_includedir}/freeradius

%files -n mibs-%{name}
%defattr(644,root,root,755)
%{mibdir}/FREERADIUS-MGMT-MIB.mib
%{mibdir}/FREERADIUS-NOTIFICATION-MIB.mib
%{mibdir}/FREERADIUS-PRODUCT-RADIUSD-MIB.mib
%{mibdir}/FREERADIUS-SMI.mib
