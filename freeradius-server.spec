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
#   /usr/lib/freeradius/rlm_unix-2.1.1.so
# - After install/uninstall every module perform daemon restart
#
%include	/usr/lib/rpm/macros.perl
#
Summary:	High-performance and highly configurable RADIUS server
Summary(pl.UTF-8):	Szybki i wysoce konfigurowalny serwer RADIUS
Name:		freeradius-server
Version:	2.1.1
Release:	0.11
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

%package module-mysql
Summary:	Mysql module for %{name}
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-mysql
Mysql module for %{name}.

%package module-unixodbc
Summary:	odbcunix module for %{name}
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-unixodbc
UnixODBC module for %{name}.

%package module-postgresql
Summary:	PostgreSQL module for %{name}
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-postgresql
PostgreSQL module for %{name}.

%package module-sqlite
Summary:	Sqlite module for %{name}
Group:		Networking/Daemons/Radius
Requires:	%{name} = %{version}-%{release}

%description module-sqlite
Sqlite module for %{name}.

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
	$RPM_BUILD_ROOT%{_sysconfdir}/*.pl \
	$RPM_BUILD_ROOT%{_sysconfdir}/raddb/sql/oracle

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/*
# To separate package:
%exclude %{_sysconfdir}/raddb/sql/mysql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/freeradius
%attr(755,root,root) %{_libdir}/freeradius/rlm_acctlog*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_acctlog*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_acct_unique*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_acct_unique*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_always*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_always*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_attr_filter*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_attr_filter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_attr_rewrite*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_attr_rewrite*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_chap*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_chap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_checkval*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_checkval*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_copy_packet*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_copy_packet*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_counter*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_counter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_cram*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_cram*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_dbm*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_dbm*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_detail*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_detail*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_digest*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_digest*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_dynamic_clients*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_dynamic_clients*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_eap*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_eap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_example*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_example*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_exec*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_exec*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_expiration*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_expiration*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_expr*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_expr*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_fastusers*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_fastusers*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_files*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_files*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_ippool*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_ippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_jradius*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_jradius*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_krb5*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_krb5*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_ldap*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_ldap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_linelog*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_linelog*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_logintime*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_logintime*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_mschap*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_mschap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_otp*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_otp*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_pam*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_pam*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_pap*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_pap*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_passwd*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_passwd*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_perl*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_perl*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_policy*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_policy*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_preprocess*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_preprocess*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_protocol_filter*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_protocol_filter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_python*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_python*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_radutmp*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_radutmp*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_realm*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_realm*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sim_files*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sim_files*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql-*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql-*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlcounter*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlcounter*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_firebird*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_firebird*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlhpwippool*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlhpwippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlippool*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sqlippool*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_log*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_log*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_unix*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_unix*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_wimax*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_wimax*.la
%{_datadir}/freeradius
%{_mandir}/man?/*
%attr(771,root,radius) %dir %{_var}/log/freeradius
%attr(771,root,radius) %dir %{_var}/log/freeradius/radacct
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius
%attr(771,root,radius) %dir %{_var}/log/archive/freeradius/radacct
%attr(775,root,radius) %dir /var/run/freeradius

%files module-mysql
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/sql/mysql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql/mysql/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_mysql*.la
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_mysql*.so

%files module-sqlite
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_sqlite*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_sqlite*.la

%files module-postgresql
%defattr(644,root,root,755)
%dir %{_sysconfdir}/raddb/sql/postgresql
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/raddb/sql/postgresql/*
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_postgresql*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_postgresql*.la

%files module-unixodbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_unixodbc*.so
%attr(755,root,root) %{_libdir}/freeradius/rlm_sql_unixodbc*.la

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
