#
# TODO:
#	- Currently this package conflicts with freeradius - should we use Obsolete header ?
#	- check log files permisions - should be writable by radius user/group
#	(log files are created by server)
#
%include	/usr/lib/rpm/macros.perl
#
Summary:	High-performance and highly configurable RADIUS server
Summary(pl.UTF-8):	Szybki i wysoce konfigurowalny serwer RADIUS
Name:		freeradius-server
Version:	2.1.1
Release:	0.1
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
Provides:	group(radius)
Provides:	user(radius)
Provides:	freeradius = %{version}-%{release}
Obsoletes:	cistron-radius
Obsoletes:	freeradius < 2.0
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
find -name 'configure.[ia][nc]' -type f | while read FILE; do
    cd $(dirname "$FILE")
    %{__libtoolize}
    %{__aclocal} -I $OLDPWD
    %{__autoconf}
    [ -f config.h.in ] && %{__autoheader}
    cd -
done

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

%{__make} -j1 install \
	R=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/%{_docdir}/freeradius
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.a
rm -rf $RPM_BUILD_ROOT/%{_sbindir}/rc.*
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/*.pl

install -d		$RPM_BUILD_ROOT/etc/logrotate.d
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/logrotate.d/%{name}

install -d		$RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE2}	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

install -d		$RPM_BUILD_ROOT/etc/pam.d
install %{SOURCE3}	$RPM_BUILD_ROOT/etc/pam.d/radius

install -d $RPM_BUILD_ROOT%{_var}/log/{,archive}/freeradius/radacct

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

%files
%defattr(644,root,root,755)
%doc doc/*
%dir %{_libdir}/freeradius
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
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/freeradius/*.la
%attr(755,root,root) %{_libdir}/freeradius/*.so
%{_datadir}/freeradius
%{_includedir}/freeradius
%{_mandir}/man?/*
