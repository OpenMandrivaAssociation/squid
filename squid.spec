%define their_version 2.6.STABLE16
%define version 2.6.STABLE16

## Redefine configure values.
%define         _bindir %{_prefix}/sbin
%define         _libexecdir %{_libdir}/squid
%define         _initrddir /etc/rc.d/init.d/
%define         _sysconfdir /etc/squid
%define         _localstatedir /var
%define         defaultmaxfiles 1024

Summary:	The Squid proxy caching server
Name:		squid
Version:	%{version}
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://www.squid-cache.org/
Source0:	http://www.squid-cache.org/Versions/v2/2.6/squid-%{their_version}.tar.gz
Source1:	http://www.squid-cache.org/Versions/v2/2.6/squid-%{their_version}.tar.gz.asc
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
Patch0:		squid-2.6.STABLE6-make.patch
Patch1:		squid-2.6-config.patch
Patch2:		squid-2.5.STABLE9-user_group.patch
Patch3:		squid-2.5.STABLE2-ssl.patch
Patch6: 	http://dansguardian.org/downloads/squid-xforward_logging.patch
Patch7: 	squid-2.6.STABLE1-db4.diff
Patch8: 	squid-2.6.STABLE1-visible_hostname.diff
Patch9: 	squid-2.6.STABLE-smb-auth.diff
# http://devel.squid-cache.org/projects.html#icap
# http://devel.squid-cache.org/cgi-bin/diff2/icap-2.6.patch
Patch300:	squid-2.6.STABLE16-icap.diff
Patch301:	squid-2.6.STABLE1-getconf_mess.diff
Patch400:	squid-2.6.STABLE12-fixcompile.diff
Patch401:	squid-2.6.STABLE12-fd_note_static.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	db4-devel
BuildRequires:	libsasl-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	libtool
#BuildRequires:	automake1.9
#BuildRequires:	autoconf2.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Squid is a high-performance proxy caching server for Web clients,
supporting FTP, gopher, and HTTP data objects. Unlike traditional
caching software, Squid handles all requests in a single,
non-blocking, I/O-driven process. Squid keeps meta data and especially
hot objects cached in RAM, caches DNS lookups, supports non-blocking
DNS lookups, and implements negative caching of failed requests.

Squid consists of a main server program squid, a Domain Name System
lookup program (dnsserver), a program for retrieving FTP data
(ftpget), and some management and client tools.

Install squid if you need a proxy caching server.

This package defaults to a maximum of %defaultmaxfiles filedescriptors. You can change 
this value at build time by using for example:

--define 'maxfiles 4096'

The package was built to support a maximum of %{?!maxfiles:%defaultmaxfiles}%{?maxfiles:%maxfiles} filedescriptors.

%package	cachemgr
Summary:	The Squid Cache Manager
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.54
Requires(pre):	apache >= 2.0.54
Requires(pre):	apache-modules >= 2.0.54
Requires(pre):	%{name} = %{version}
Requires:	apache-conf >= 2.0.54
Requires:	apache >= 2.0.54
Requires:	apache-modules >= 2.0.54
Requires:	%{name} = %{version}

%description	cachemgr
This package contains the Squid Cache Manager.

%prep

%setup -q -n squid-%their_version

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .ssl
%patch6 -p1 -b .forward_logging
%patch7 -p1 -b .db4
%patch8 -p0 -b .visible_hostname
%patch9 -p0 -b .backslashes

%patch300 -p1 -b .ICAP
%patch301 -p0 -b .getconf
%patch400 -p1 -b .fixcompile
%patch401 -p1 -b .note_static

mkdir -p faq
tar -jxf %{SOURCE2} -C faq

install -m 0755 %{SOURCE3} squid.init
install -m 0644 %{SOURCE4} squid.logrotate
install -m 0644 %{SOURCE5} squid.conf.authenticate
install -m 0644 %{SOURCE6} smb.conf
install -m 0644 %{SOURCE7} squid.conf.transparent
install -m 0755 %{SOURCE8} rc.firewall
install -m 0644 %{SOURCE11} squid.sysconfig

# fix conditional pam config file
%if %{mdkversion} < 200610
install -m 0644 %{SOURCE12} squid.pam
%else
install -m 0644 %{SOURCE13} squid.pam
%endif

perl -p -i -e "s|^SAMBAPREFIX.*|SAMBAPREFIX = /usr|" helpers/basic_auth/SMB/Makefile.*
perl -p -i -e "s|^icondir.*|icondir = \\$\(libexecdir\)/icons|" icons/Makefile.am icons/Makefile.*
grep -r "local/bin/perl" . |sed -e "s/:.*$//g" | xargs perl -p -i -e "s@local/bin/perl@bin/perl@g"

%build
%serverbuild
rm -rf configure autom4te.cache
libtoolize --copy --force
aclocal
autoheader
autoconf --force
automake --foreign --add-missing --copy --force-missing

export SSLLIB="-L%{_libdir} `pkg-config --libs openssl`"
export CPPFLAGS="-I%{_includedir}/openssl $CPPFLAGS"

%ifarch x86_64
export CFLAGS="$CFLAGS -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
%else
export CFLAGS="$CFLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
%endif

%configure2_5x \
    --enable-icap-support \
    %{?!maxfiles:--with-maxfd=%defaultmaxfiles}%{?maxfiles:%maxfiles} \
    --disable-poll \
    --enable-epoll \
    --enable-snmp \
    --enable-useragent-log \
    --enable-referer-log \
    --enable-removal-policies="heap,lru" \
    --enable-storeio="aufs,coss,diskd,ufs,null" \
    --enable-cachemgr-hostname="localhost" \
    --enable-truncate \
    --enable-underscores \
    --enable-carp \
    --enable-async-io \
    --enable-htcp \
    --enable-icmp \
    --enable-delay-pools \
    --enable-linux-netfilter \
    --enable-default-hostsfile=/etc/hosts \
    --enable-ssl \
    --with-openssl=%{_prefix} \
    --enable-arp-acl \
    --enable-wccp \
    --enable-wccpv2 \
    --enable-auth="basic,digest,ntlm,negotiate" \
    --enable-basic-auth-helpers="getpwnam,LDAP,MSNT,multi-domain-NTLM,NCSA,PAM,SASL,SMB,YP" \
    --enable-ntlm-auth-helpers="fakeauth,no_check,SMB" \
    --enable-digest-auth-helpers="ldap,password" \
    --enable-external-acl-helpers="ip_user,ldap_group,session,unix_group,wbinfo_group" \
    --enable-follow-x-forwarded-for \
    --with-pthreads \
    --disable-dependency-tracking \
    --disable-ident-lookups \
    --enable-large-cache-files \
    --with-large-files \
    --with-build-environment=default

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
grep -r errors * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/%{_lib}/squid/errors|g" 
grep -r iconsdir * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/%{_lib}/squid/errors|g" 

%make

grep -r errors * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/%{_lib}/squid/errors|g" 

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall 

# make some directories
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/etc/{logrotate.d,pam.d,sysconfig}
install -d %{buildroot}/etc/httpd/conf/webapps.d
install -d %{buildroot}%{_libexecdir}/{errors,icons}
install -d %{buildroot}%{_libexecdir}/errors/{English,French}
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_var}/www/cgi-bin
install -d %{buildroot}%{_var}/log/squid
install -d %{buildroot}%{_var}/run/squid
install -d %{buildroot}%{_var}/spool/squid
install -d %{buildroot}%{_datadir}/snmp/mibs

# fix error docs location
rm -rf %{buildroot}%{_sysconfdir}/errors
pushd errors
    for i in *; do
	if [ -d $i ]; then
	    install -d %{buildroot}%{_libexecdir}/errors/$i
	    install -m0644 $i/* %{buildroot}%{_libexecdir}/errors/$i
	fi
    done
popd
ln -fs %{_libexecdir}/errors/English %{buildroot}%{_sysconfdir}/errors

# install config
install -m0755 squid.init %{buildroot}%{_initrddir}/squid
install -m0644 squid.logrotate %{buildroot}/etc/logrotate.d/squid
install -m0644 squid.sysconfig %{buildroot}/etc/sysconfig/squid
install -m0644 helpers/basic_auth/MSNT/msntauth.conf.default %{buildroot}%{_sysconfdir}

# fix docs
cp helpers/basic_auth/LDAP/README README.auth_ldap

cp helpers/basic_auth/MSNT/README.html README.auth_msnt.html
cp helpers/basic_auth/MSNT/msntauth.conf.default .

cp helpers/basic_auth/SASL/README README.auth_sasl
cp helpers/basic_auth/SASL/squid_sasl_auth.conf .

cp helpers/basic_auth/SMB/README README.auth_smb
cp helpers/basic_auth/multi-domain-NTLM/README.txt README.multi-domain-NTLM_basic_auth

cp helpers/external_acl/ip_user/README README.ip_user_external_acl
cp helpers/external_acl/ip_user/example.conf ip_user_external_acl.example.conf
cp helpers/external_acl/ip_user/example-deny_all_but.conf ip_user_external_acl.example-deny_all_but.conf

cp helpers/external_acl/ldap_group/README README.ldap_group_external_acl
cp helpers/external_acl/ldap_group/ChangeLog ChangeLog.ldap_group_external_acl

cp helpers/external_acl/unix_group/README README.unix_group_external_acl
cp helpers/ntlm_auth/no_check/README.no_check_ntlm_auth README.no_check_ntlm_auth

head -19 helpers/basic_auth/NCSA/ncsa_auth.c > README.NCSA_basic_auth
head -56 helpers/basic_auth/PAM/pam_auth.c > README.PAM_basic_auth
head -21 helpers/basic_auth/getpwnam/getpwnam_auth.c > README.getpwnam_basic_auth
head -32 helpers/digest_auth/password/digest_pw_auth.c > README.password_digest_auth
head -32 helpers/digest_auth/ldap/digest_pw_auth.c > README.ldap_digest_auth

install -m0755 helpers/basic_auth/SMB/smb_auth.sh %{buildroot}%{_libexecdir}
install -m0755 helpers/basic_auth/SASL/squid_sasl_auth %{buildroot}%{_libexecdir}

for manpage in `find -name "*.8"`; do
    install -m0644 $manpage %{buildroot}/%{_mandir}/man8/
done

install -m 0644 %{SOURCE9} %{buildroot}%{_libexecdir}/errors/English/ERR_CUSTOM_ACCESS_DENIED
install -m 0644 %{SOURCE10} %{buildroot}%{_libexecdir}/errors/French/ERR_CUSTOM_ACCESS_DENIED

install -m644 squid.pam %{buildroot}/etc/pam.d/squid

# move the mib in-place
mv %{buildroot}%{_datadir}/mib.txt %{buildroot}%{_datadir}/snmp/mibs/SQUID.txt

# move cachemgr.cgi to a more safe location
mv %{buildroot}%{_libexecdir}/cachemgr.cgi %{buildroot}%{_var}/www/cgi-bin/

# provide a simple apache config
cat > %{buildroot}/etc/httpd/conf/webapps.d/squid-cachemgr.conf << EOF
<Location /cgi-bin/cachemgr.cgi>
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
</Location>
EOF

# some cleaning
rm -f %{buildroot}%{_libdir}/squid/no_check.pl
rm -rf %{buildroot}%{_datadir}/errors

# nuke zero length files
find %{buildroot}%{_libdir}/squid/errors/ -type f -size 0 -exec rm -f {} \;

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

%post cachemgr
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun cachemgr
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc faq/* C* S* R* Q* rc.firewall *.conf* doc/*.txt
%exclude %{_sysconfdir}/cachemgr.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/*.default
%attr(0644,root,root) %config(noreplace) /etc/pam.d/squid
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/squid
%attr(0644,root,root) %config(noreplace) /etc/logrotate.d/squid
%attr(0755,root,squid) %{_initrddir}/squid
%{_sysconfdir}/errors
%{_libexecdir}/errors
%{_libexecdir}/icons
%{_libexecdir}/diskd-daemon
%{_libexecdir}/unlinkd
%attr(0755,root,squid) %{_libexecdir}/digest_ldap_auth
%attr(0755,root,squid) %{_libexecdir}/digest_pw_auth
%attr(0755,root,squid) %{_libexecdir}/fakeauth_auth
%attr(0755,root,squid) %{_libexecdir}/getpwname_auth
%attr(0755,root,squid) %{_libexecdir}/ip_user_check
%attr(0755,root,squid) %{_libexecdir}/msnt_auth
%attr(0755,root,squid) %{_libexecdir}/ncsa_auth
%attr(0755,root,squid) %{_libexecdir}/ntlm_auth
%attr(0755,root,squid) %{_libexecdir}/pam_auth
%attr(0755,root,squid) %{_libexecdir}/pinger
%attr(0755,root,squid) %{_libexecdir}/sasl_auth
%attr(0755,root,squid) %{_libexecdir}/smb_auth
%attr(0755,root,squid) %{_libexecdir}/smb_auth.pl
%attr(0755,root,squid) %{_libexecdir}/smb_auth.sh
%attr(0755,root,squid) %{_libexecdir}/squid_ldap_auth
%attr(0755,root,squid) %{_libexecdir}/squid_ldap_group
%attr(0755,root,squid) %{_libexecdir}/squid_sasl_auth
%attr(0755,root,squid) %{_libexecdir}/squid_session
%attr(0755,root,squid) %{_libexecdir}/squid_unix_group
%attr(0755,root,squid) %{_libexecdir}/wbinfo_group.pl
%attr(0755,root,squid) %{_libexecdir}/yp_auth
%{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0755,squid,squid) %dir %{_var}/run/squid
%attr(0755,squid,squid) %dir %{_var}/log/squid
%attr(0755,squid,squid) %dir %{_var}/spool/squid
%attr(0644,root,squid) %{_datadir}/snmp/mibs/SQUID.txt

%files cachemgr
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) /etc/httpd/conf/webapps.d/squid-cachemgr.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cachemgr.conf
%attr(0755,root,squid) %{_var}/www/cgi-bin/cachemgr.cgi
