#% define with test 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%bcond_with test

%define squid_date 20130108
%define squid_beta 0
##%define their_version 3.2.1.%{squid_beta}-%{squid_date}
%define their_version 3.4.9

## Redefine configure values.
%define	_bindir %{_prefix}/sbin
%define _libexecdir %{_libdir}/squid
%define _initrddir /etc/rc.d/init.d/
%define _sysconfdir /etc/squid
%define  _localstatedir /var
%define _datadir %{_usr}/share/squid
%define _mandir %{_usr}/share/man
%define _infodir %{_usr}/share/info

%define major %(echo %{their_version} |cut -d. -f1)
%define majorminor %(echo %{their_version} |cut -d. -f1-2)

%define defaultmaxfiles 8192

Summary:	The Squid proxy caching server
Name:		squid
Version:	%{their_version}
Release:	2
License:	GPLv2
Group:		System/Servers
URL:		http://www.squid-cache.org/
Source0:	http://www.squid-cache.org/Versions/v%{major}/%{majorminor}/squid-%{their_version}.tar.xz
Source1:	http://www.squid-cache.org/Versions/v%{major}/%{majorminor}/squid-%{their_version}.tar.xz.asc
Source2:	http://www.squid-cache.org/Doc/FAQ/FAQ.tar.bz2
Source3:	squid.init
Source4:	squid.logrotate
Source5:	squid.conf.authenticate
Source6:	smb.conf
Source7:	squid.conf.transparent
Source8:	rc.firewall
Source9:	ERR_CUSTOM_ACCESS_DENIED.English
Source10:	ERR_CUSTOM_ACCESS_DENIED.French
Source11: 	squid.sysconfig
Source12:	squid.pam-0.77
Source13:	squid.pam
Source14:	squid.ifup
Patch1:		squid-config.diff
Patch2:		squid-user_group.diff
Patch3:		squid-ssl.diff
#Patch4:		squid-3.0-with_new_linux_headers_capability.patch
Patch8:		squid-visible_hostname.diff
Patch9:		squid-smb-auth.diff
Patch11:	squid-shutdown_lifetime.diff
#Patch12:	squid-no_-Werror.diff
Patch13:	squid-datadir.diff
#Patch14:	squid-digest-rfc2069.diff
#Patch15:	squid-3.1-error-make.diff
Patch16:	squid-3.1.4-mysql-helper-joomla.diff
Patch301:	squid-getconf_mess.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	bzip2
BuildRequires:	libtool-devel
BuildRequires:	db-devel
BuildRequires:	sasl-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	libtool
BuildRequires:	krb5-devel
BuildRequires:	ecap-devel
BuildRequires:	cap-devel
#BuildRequires:	automake1.9
#BuildRequires:	autoconf2.5
%if %{with test}
BuildRequires:	cppunit-devel
%endif
Provides:	webproxy

%description
Squid is a high-performance proxy caching server for web clients, supporting 
FTP, gopher, and HTTP data objects over IPv4 or IPv6. Unlike traditional 
caching software, Squid handles all requests in a single, non-blocking, 
asynchronous process.
Squid keeps meta data and especially hot objects cached in RAM, caches DNS 
lookups, supports non-blocking DNS lookups, and implements negative caching 
of failed requests.  Squid supports SSL, extensive access controls, and full 
request logging. By using the lightweight Internet Cache Protocol (ICP) and 
HTTP Cache Protocol (HTCP) Squid caches can be arranged in a hierarchy or 
mesh for additional bandwidth savings.

Install squid if you need a proxy caching server.

This package defaults to a maximum of %{defaultmaxfiles} filedescriptors. You
can change these values at build time by using for example:

--define 'maxfiles 4096'

The package was built to support a maximum of %{?!maxfiles:%{defaultmaxfiles}}%{?maxfiles:%{maxfiles}} filedescriptors.

You can build %{name} with some conditional build swithes;

(ie. use with rpm --rebuild):
    --with[out]	test	Initiate the test suite

%package	cachemgr
Summary:	The Squid Cache Manager
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache >= 2.0.54
Requires(pre):	%{name} = %{version}
Requires:	apache >= 2.0.54
Requires:	%{name} = %{version}

%description	cachemgr
This package contains the Squid Cache Manager.


%prep

%setup -q -n squid-%{their_version}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done


%patch1 -p1 -b .config
%patch2 -p1 -b .user_group
%patch3 -p1 -b .ssl
#patch4 -p0 -b .with_new_linux_headers_capability
%patch8 -p1 -b .visible_hostname
%patch9 -p1 -b .backslashes
%patch11 -p0 -b .shutdown_lifetime
#patch12 -p1 -b .no_-Werror
%patch13 -p1 -b .datadir
#patch14 -p1 -b .digest-rfc2069
#patch15 -p1 -b .errordir
%patch16 -p0 -b .joomla
#%patch301 -p1 -b .getconf

mkdir -p faq
tar -jxf %{SOURCE2} -C faq

install -m 0755 %{SOURCE3} squid.init
install -m 0644 %{SOURCE4} squid.logrotate
install -m 0644 %{SOURCE5} squid.conf.authenticate
install -m 0644 %{SOURCE6} smb.conf
install -m 0644 %{SOURCE7} squid.conf.transparent
install -m 0755 %{SOURCE8} rc.firewall
install -m 0644 %{SOURCE11} squid.sysconfig
install -m 0755 %{SOURCE14} squid.ifup

# fix conditional pam config file
install -m 0644 %{SOURCE13} squid.pam

perl -p -i -e "s|^SAMBAPREFIX.*|SAMBAPREFIX = /usr|" helpers/basic_auth/SMB/Makefile.*
#perl -p -i -e "s|^icondir.*|icondir = \\$\(libexecdir\)/icons|" icons/Makefile.am icons/Makefile.*
grep -r "local/bin/perl" . |sed -e "s/:.*$//g" | xargs perl -p -i -e "s@local/bin/perl@bin/perl@g"

# libtool
perl -pi -e "s|AC_PROG_RANLIB|AC_PROG_LIBTOOL|g" configure*

%build

%serverbuild
rm -rf configure autom4te.cache
#libtoolize --copy --force
#aclocal
#autoheader
#autoconf --force
#automake --foreign --add-missing --copy --force-missing

sh ./bootstrap.sh

export SSLLIB="-L%{_libdir} `pkg-config --libs openssl`"
export CPPFLAGS="-I%{_includedir}/openssl -I`find /usr/include -type f -name db_185.h|head -n1|xargs dirname` %optflags "

%ifarch x86_64
export CFLAGS="$CFLAGS -I`find /usr/include -type f -name db_185.h|head -n1|xargs dirname` -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CXXFLAGS -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
%else
export CFLAGS="$CFLAGS -I`find /usr/include -type f -name db_185.h|head -n1|xargs dirname` -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CXXFLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
%endif

# --enable-external-acl-helpers="ip_user,ldap_group,session,unix_group,wbinfo_group" \
CC=gcc CXX=g++ \
%configure2_5x \
    --disable-strict-error-checking \
    --enable-shared=yes \
    --enable-static=no \
    --enable-xmalloc-statistics \
    --enable-carp \
    --enable-async-io \
    --enable-storeio="aufs,diskd,ufs" \
    --enable-removal-policies="heap,lru" \
    --enable-icmp \
    --enable-delay-pools \
    --disable-esi \
    --enable-icap-client \
    --enable-ecap \
    --enable-useragent-log \
    --enable-referer-log \
    --enable-wccp \
    --enable-wccpv2 \
    --disable-kill-parent-hack \
    --enable-snmp \
    --enable-cachemgr-hostname="localhost" \
    --enable-arp-acl \
    --enable-htcp \
    --enable-ssl \
    --enable-forw-via-db \
    --enable-follow-x-forwarded-for \
    --enable-cache-digests \
    --disable-poll \
    --enable-epoll \
    --enable-linux-netfilter \
    --disable-ident-lookups \
    --enable-default-hostsfile=/etc/hosts \
    --enable-auth \
    --enable-basic-auth="getpwnam,LDAP,MSNT,multi-domain-NTLM,NCSA,PAM,SMB,YP,SASL,POP3,DB,squid_radius_auth" \
    --enable-ntlm-auth="fakeauth,no_check,smb_lm" \
    --enable-negotiate-auth="squid_kerb_auth" \
    --enable-digest-auth="password,ldap,eDirectory" \
    --enable-external-acl-helpers \
    --with-default-user=%{name} \
    --with-pthreads \
    --with-dl \
    --with-openssl=%{_prefix} \
    --with-large-files \
    --with-swapdir=%{_localstatedir}/spool/squid \
    --with-build-environment=default \
    --enable-mit=`/usr/bin/krb5-config --prefix` \
    --with-logdir=%{_logdir}/squid \
    --enable-http-violations \
    --enable-zph-qos \
    %{?!maxfiles:--with-filedescriptors=%{defaultmaxfiles}}%{?maxfiles:%{maxfiles}}


#    --enable-disk-io="AIO,Blocking,DiskDaemon,DiskThreads" \

# Some versions of autoconf fail to detect sys/resource.h correctly;
# apparently because it generates a compiler warning.

if [ -e /usr/include/sys/resource.h ]; then
cat >> include/autoconf.h <<EOF
#ifndef HAVE_SYS_RESOURCE_H
#define HAVE_SYS_RESOURCE_H 1
#define HAVE_STRUCT_RUSAGE 1
#endif
EOF
fi

# move the errors files
#grep -r errors * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/%{_lib}/squid/errors|g" 
#grep -r iconsdir * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/%{_lib}/squid/errors|g" 

%make

#grep -r errors * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/%{_lib}/squid/errors|g" 

%if %{with test}
%check
make check
%endif

%install
rm -rf %{buildroot}

%makeinstall icondir=%{buildroot}%{_datadir}/icons DEFAULT_LOG_DIR=%{buildroot}%{_logdir}/squid DEFAULT_ERROR_DIR=%{buildroot}%{_datadir}/errors DEFAULT_ICON_DIR=%{buildroot}%{_datadir}/icons



# make some directories
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/etc/{logrotate.d,pam.d,sysconfig}
install -d %{buildroot}/etc/sysconfig/network-scripts/ifup.d
install -d %{buildroot}/etc/httpd/conf/webapps.d
install -d %{buildroot}%{_datadir}/{errors,icons}
install -d %{buildroot}%{_datadir}/errors/{English,French}
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_var}/www/cgi-bin
install -d %{buildroot}%{_var}/log/squid
#install -d %{buildroot}%{_var}/run/squid
install -d %{buildroot}%{_var}/spool/squid
install -d %{buildroot}/usr/share/snmp/mibs

# fix error docs location	
rm -rf %{buildroot}%{_sysconfdir}/errors
pushd errors
    for i in *; do
	if [ -d $i ]; then
	    install -d %{buildroot}%{_datadir}/errors/$i
	    install -m0644 $i/* %{buildroot}%{_datadir}/errors/$i
	fi
    done
popd
ln -fs %{_datadir}/errors/templates %{buildroot}%{_sysconfdir}/errors

# install config
install -m0755 squid.init %{buildroot}%{_initrddir}/squid
install -m0644 squid.logrotate %{buildroot}/etc/logrotate.d/squid
install -m0644 squid.sysconfig %{buildroot}/etc/sysconfig/squid
install -m0755 squid.ifup %{buildroot}/etc/sysconfig/network-scripts/ifup.d/squid
install -m0644 helpers/basic_auth/MSNT/msntauth.conf.default %{buildroot}%{_sysconfdir}

# fix docs
cp helpers/basic_auth/LDAP/README README.auth_ldap

cp helpers/basic_auth/MSNT/README.html README.auth_msnt.html
cp helpers/basic_auth/MSNT/msntauth.conf.default .

cp helpers/basic_auth/SASL/basic_sasl_auth.conf .

cp helpers/external_acl/file_userip/example.conf ip_user_external_acl.example.conf
cp helpers/external_acl/file_userip/example-deny_all_but.conf ip_user_external_acl.example-deny_all_but.conf

cp helpers/external_acl/LDAP_group/ChangeLog ChangeLog.ldap_group_external_acl

head -19 helpers/basic_auth/NCSA/basic_ncsa_auth.cc > README.NCSA_basic_auth
head -56 helpers/basic_auth/PAM/basic_pam_auth.cc > README.PAM_basic_auth
head -21 helpers/basic_auth/getpwnam/basic_getpwnam_auth.cc > README.getpwnam_basic_auth
head -32 helpers/digest_auth/LDAP/digest_pw_auth.cc > README.ldap_digest_auth

install -m0755 helpers/basic_auth/SMB/basic_smb_auth.sh %{buildroot}%{_libexecdir}
install -m0755 helpers/basic_auth/SASL/basic_sasl_auth %{buildroot}%{_libexecdir}

for manpage in `find -name "*.8"`; do
    install -m0644 $manpage %{buildroot}/%{_mandir}/man8/
done

install -m 0644 %{SOURCE9} %{buildroot}%{_datadir}/errors/English/ERR_CUSTOM_ACCESS_DENIED
install -m 0644 %{SOURCE10} %{buildroot}%{_datadir}/errors/French/ERR_CUSTOM_ACCESS_DENIED

install -m644 squid.pam %{buildroot}/etc/pam.d/squid

# move the mib in-place
mv %{buildroot}%{_datadir}/mib.txt %{buildroot}/usr/share/snmp/mibs/SQUID.txt

# move cachemgr.cgi to a more safe location
mv %{buildroot}%{_libexecdir}/cachemgr.cgi %{buildroot}%{_var}/www/cgi-bin/

# provide a simple apache config
cat > %{buildroot}/etc/httpd/conf/webapps.d/squid-cachemgr.conf << EOF
<Location /cgi-bin/cachemgr.cgi>
%if %{mdvver} < 2013
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
%endif
%if %{mdvver} >= 2013
    Require local granted
%endif
    ErrorDocument 403 "Access denied per /etc/httpd/conf/webapps.d/squid-cachemgr.conf"
</Location>
EOF

# some cleaning
rm -f %{buildroot}%{_libdir}/squid/no_check.pl
#rm -rf %{buildroot}%{_datadir}/errors

# nuke zero length files
find %{buildroot}%{_datadir}/errors/ -type f -size 0 -exec rm -f {} \;

%pre
%_pre_useradd squid %{_var}/spool/squid /bin/false

for i in %{_var}/log/squid %{_var}/spool/squid ; do
        if [ -d $i ] ; then
                for adir in `find $i -maxdepth 0 \! -user squid`; do
                        chown -R squid:squid $adir
                done
        fi
done

%post
%_create_ssl_certificate squid

%_post_service squid
 case "$LANG" in
  az*)
     DIR=Azerbaijani
     ;;
  bg*)
     DIR=Bulgarian
     ;;
  ca*)
     DIR=Catalan
     ;;
  cs*)
     DIR=Czech
     ;;
  da*)
     DIR=Danish
     ;;
  nl*)
     DIR=Dutch
     ;;
  en*)
     DIR=English
     ;;
  ea*)
     DIR=Estonian
     ;;
  fi*)
     DIR=Finnish
     ;;
  fr*)
     DIR=French
     ;;
  de*)
     DIR=German
     ;;
  el*)
     DIR=Greek
     ;;
  he*)
     DIR=Hebrew
     ;;
  hu*)
     DIR=Hungarian
     ;;
  it*)
     DIR=Italian
     ;;
  ja*)
     DIR=Japanese
     ;;
  kr*)
     DIR=Korean
     ;;
  lt*)
     DIR=Lithuanian
     ;;
  pl*)
     DIR=Polish
     ;;
  pt*)
     DIR=Portuguese
     ;;
  ro*)
     DIR=Romanian
     ;;
  ru*)
     DIR=Russian-koi8-r
     ;;
  sr*)
     DIR=Serbian
     ;;
  sk*)
     DIR=Slovak
     ;;
  es*)
     DIR=Spanish
     ;;
  sv*)
     DIR=Swedish
     ;;
  zh*)
     DIR=Traditional_Chinese
     ;;
  tr*)
     DIR=Turkish
     ;;
  *)
     DIR=English
     ;;
 esac

%preun
%_preun_service squid
if [ $1 = 0 ] ; then
	rm -f %{_var}/log/squid/*
        /sbin/chkconfig --del squid
fi

%postun
%_postun_userdel squid

%files
%doc faq/* C* R* Q* rc.firewall *.conf* doc/*.txt
%exclude %{_sysconfdir}/cachemgr.conf
%dir %_sysconfdir
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.default
%attr(0644,root,root) %config(noreplace) /etc/pam.d/squid
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/squid
%attr(0644,root,root) %config(noreplace) /etc/logrotate.d/squid
%attr(0755,root,squid) %config(noreplace) /etc/sysconfig/network-scripts/ifup.d/squid
%attr(0755,root,squid) %{_initrddir}/squid
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.css
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.documented
%{_sysconfdir}/errors
%{_datadir}/errors
%{_datadir}/icons
%{_libexecdir}/diskd
%{_libexecdir}/unlinkd
%attr(0755,root,squid) %{_libexecdir}/digest_ldap_auth
%attr(0755,root,squid) %{_libexecdir}/digest_file_auth
%attr(0755,root,squid) %{_libexecdir}/basic_fake_auth
%attr(0755,root,squid) %{_libexecdir}/basic_getpwnam_auth
%attr(0755,root,squid) %{_libexecdir}/basic_msnt_auth
%attr(0755,root,squid) %{_libexecdir}/basic_ncsa_auth
#%attr(0755,root,squid) %{_libexecdir}/ntlm_auth
%attr(0755,root,squid) %{_libexecdir}/basic_pam_auth
%attr(4755,root,squid) %{_libexecdir}/pinger
%attr(0755,root,squid) %{_libexecdir}/basic_pop3_auth
%attr(0755,root,squid) %{_libexecdir}/basic_sasl_auth
%attr(0755,root,squid) %{_libexecdir}/basic_smb_auth
%attr(0755,root,squid) %{_libexecdir}/basic_smb_auth.sh
%attr(0755,root,squid) %{_libexecdir}/basic_db_auth
%attr(0755,root,squid) %{_libexecdir}/basic_ldap_auth
%attr(0755,root,squid) %{_libexecdir}/basic_radius_auth
%attr(0755,root,squid) %{_libexecdir}/ext_session_acl
%attr(0755,root,squid) %{_libexecdir}/ext_unix_group_acl
%attr(0755,root,squid) %{_libexecdir}/negotiate_kerberos_auth
%attr(0755,root,squid) %{_libexecdir}/negotiate_kerberos_auth_test
%attr(0755,root,squid) %{_libexecdir}/ntlm_smb_lm_auth
%attr(0755,root,squid) %{_libexecdir}/basic_msnt_multi_domain_auth
%attr(0755,root,squid) %{_libexecdir}/ext_wbinfo_group_acl
%attr(0755,root,squid) %{_libexecdir}/helper-mux.pl
%attr(0755,root,squid) %{_libexecdir}/log_file_daemon
%attr(0755,root,squid) %{_libexecdir}/negotiate_wrapper_auth
%attr(0755,root,squid) %{_libexecdir}/ntlm_fake_auth
%attr(0755,root,squid) %{_libexecdir}/url_fake_rewrite
%attr(0755,root,squid) %{_libexecdir}/url_fake_rewrite.sh
%attr(0755,root,squid) %{_libexecdir}/basic_nis_auth
%attr(0755,root,squid) %{_libexecdir}/cert_tool
%attr(0755,root,squid) %{_libexecdir}/cert_valid.pl
%attr(0755,root,squid) %{_libexecdir}/ext_edirectory_userip_acl
%attr(0755,root,squid) %{_libexecdir}/ext_file_userip_acl
%attr(0755,root,squid) %{_libexecdir}/ext_kerberos_ldap_group_acl
%attr(0755,root,squid) %{_libexecdir}/ext_ldap_group_acl
%attr(0755,root,squid) %{_libexecdir}/ext_sql_session_acl
%attr(0755,root,squid) %{_libexecdir}/ext_time_quota_acl
%attr(0755,root,squid) %{_libexecdir}/log_db_daemon
%attr(0755,root,squid) %{_libexecdir}/storeid_file_rewrite


%{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0644,root,root) %{_mandir}/man1/*
#%attr(0755,squid,squid) %dir %{_var}/run/squid
%attr(0755,squid,squid) %dir %{_var}/log/squid
%attr(0755,squid,squid) %dir %{_var}/spool/squid
%attr(0644,root,squid) /usr/share/snmp/mibs/SQUID.txt

%files cachemgr
%attr(0644,root,root) %config(noreplace) /etc/httpd/conf/webapps.d/squid-cachemgr.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cachemgr.conf
%attr(0755,root,squid) %{_var}/www/cgi-bin/cachemgr.cgi
