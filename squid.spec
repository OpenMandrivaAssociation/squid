%define build_test 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_test: %{expand: %%global build_test 1}}
%{?_without_test: %{expand: %%global build_test 0}}

%define squid_date 20120514-r11557
%define squid_beta 17
##%define their_version 3.2.0.%{squid_beta}-%{squid_date}
%define their_version 3.2.0.17

## Redefine configure values.
%define	_bindir %{_prefix}/sbin
%define _libexecdir %{_libdir}/squid
%define _initrddir /etc/rc.d/init.d/
%define _sysconfdir /etc/squid
%define  _localstatedir /var
%define _datadir %{_usr}/share/squid
%define _mandir %{_usr}/share/man
%define _infodir %{_usr}/share/info

%define defaultmaxfiles 8192

Summary:	The Squid proxy caching server %{their_version}
Name:		squid
Version:	%{their_version}
Release:	1
License:	GPLv2
Group:		System/Servers
URL:		http://www.squid-cache.org/
Source0:	http://www.squid-cache.org/Versions/v3/3.2/squid-%{their_version}.tar.bz2
Source1:	http://www.squid-cache.org/Versions/v3/3.2/squid-%{their_version}.tar.bz2.asc
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
#Patch17:	squid-3.1-10320.patch
Patch301:	squid-getconf_mess.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	bzip2
BuildRequires:	libtool-devel
BuildRequires:	db-devel
BuildRequires:	libsasl-devel
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
%if %{build_test}
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

%setup -q -n squid-%{their_version}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done


%patch1 -p1 -b .config
%patch2 -p0 -b .user_group
%patch3 -p1 -b .ssl
#patch4 -p0 -b .with_new_linux_headers_capability
%patch8 -p0 -b .visible_hostname
%patch9 -p1 -b .backslashes
%patch11 -p0 -b .shutdown_lifetime
#patch12 -p1 -b .no_-Werror
%patch13 -p1 -b .datadir
#patch14 -p1 -b .digest-rfc2069
#patch15 -p1 -b .errordir
%patch16 -p0 -b .joomla
#patch17 -p0  -b .fix
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
    --enable-external-acl-helpers="ip_user,ldap_group,session,unix_group,wbinfo_group" \
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

%if %{build_test}
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
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
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
%doc faq/* C* S* R* Q* rc.firewall *.conf* doc/*.txt
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
%attr(0755,root,squid) %{_libexecdir}/digest_edirectory_auth
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
%attr(0755,root,squid) %{_libexecdir}/basic_nis_auth
%attr(0755,root,squid) %{_libexecdir}/ext_wbinfo_group_acl
%attr(0755,root,squid) %{_libexecdir}/helper-mux.pl
%attr(0755,root,squid) %{_libexecdir}/log_file_daemon
%attr(0755,root,squid) %{_libexecdir}/negotiate_wrapper_auth
%attr(0755,root,squid) %{_libexecdir}/ntlm_fake_auth
%attr(0755,root,squid) %{_libexecdir}/url_fake_rewrite
%attr(0755,root,squid) %{_libexecdir}/url_fake_rewrite.sh

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


%changelog
* Mon May 14 2012 Crispin Boylan <crisb@mandriva.org> 3.2.0.17-1
+ Revision: 798852
- New release (compatible with ecap 0.2.0)
- Rebuild

  + Luis Daniel Lucio Quiroz <dlucio@mandriva.org>
    - 3.1.19

* Sat Dec 10 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.18-1
+ Revision: 740153
- 3.1.18
  p18 to fix compilling
- 3.1.18
  p18 to fix compilling

* Sun Oct 16 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.16-1
+ Revision: 704840
- 3.1.16

* Tue Aug 30 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.15-1
+ Revision: 697414
- 3.1.15
  we keep sync with mageia :)
- Trying to make a single RPM compatible with both distros, anyway it helps me to maintain both
- 3.1.14
  P17 merged upstream

* Tue Jun 28 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.12.3-3
+ Revision: 687614
- P17 rediffed
- P17 fixed
- S1 out, no avaliable by now at mainstream
- 3.1.12.3

* Thu Jun 02 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.12.2-3
+ Revision: 682409
- 3.1.12.2

  + Funda Wang <fwang@mandriva.org>
    - really enable backport updates

* Tue Apr 26 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1.12.1-2
+ Revision: 659199
- db4 backport support

* Sat Apr 23 2011 Funda Wang <fwang@mandriva.org> 3.1.12.1-1
+ Revision: 656790
- use upstream version
- use system libtool
- use db5.1 path patch
- disable error checking

  + Luis Daniel Lucio Quiroz <dlucio@mandriva.org>
    - 3.1.12.1
      P0 rediffed

  + Zé <ze@mandriva.org>
    - fix config file (mandriva bug 63066) to avoid squid to exist abnormally due to a fatal error

* Tue Feb 08 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-26
+ Revision: 636915
- new BR
- 3.1.11
  P9 rediffed

* Wed Dec 29 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-24mdv2011.0
+ Revision: 625818
- build against new ecap

* Sun Dec 26 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-23mdv2011.0
+ Revision: 625267
- 3.1.10
  some patches diffed

* Tue Oct 26 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-22mdv2011.0
+ Revision: 589422
- 3.1.9

* Sun Sep 05 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-21mdv2011.0
+ Revision: 576170
- cap-devel need as BR because TPROXY
- 3.1.8

* Sun Sep 05 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-19mdv2011.0
+ Revision: 576158
- 3.1.8

* Tue Aug 24 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-18mdv2011.0
+ Revision: 572941
- 3.1.7
- 3.1.7

* Fri Aug 06 2010 Michael Scherer <misc@mandriva.org> 3.1-17mdv2011.0
+ Revision: 567144
- fix License
- do not let unowned configuration directory

* Thu Aug 05 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-16mdv2011.0
+ Revision: 566464
- P10 rediff
- 3.1.6

* Sat Jul 03 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-15mdv2011.0
+ Revision: 549771
- 3.1.5

* Tue Jun 01 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-14mdv2010.1
+ Revision: 546846
- 3.1.4
  P7 & P16 rediffed

* Fri May 07 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-13mdv2010.1
+ Revision: 543540
- P16 rediff for more cool options

* Wed May 05 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-12mdv2010.1
+ Revision: 542230
- typo

* Tue May 04 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-11mdv2010.1
+ Revision: 542203
- Some cool options to make squid rocks

* Sun May 02 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-10mdv2010.1
+ Revision: 541661
- 3.1.3

* Sat May 01 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-9mdv2010.1
+ Revision: 541454
- 3.1.2
  P16 rediffed
- Dont reload ifup if squid is not running
- icapd as suggest

* Sun Apr 25 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-7mdv2010.1
+ Revision: 538529
- P16 fixin a dbh->disconnect issue

* Fri Apr 23 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-6mdv2010.1
+ Revision: 538071
- P16: we get rid  of lot of warnings

* Thu Apr 22 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-5mdv2010.1
+ Revision: 538045
- typo in P16

* Thu Apr 22 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-4mdv2010.1
+ Revision: 538033
- P16 to add support to auth against joomla db

* Tue Apr 20 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-3mdv2010.1
+ Revision: 537235
- Typo

* Mon Apr 05 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-2mdv2010.1
+ Revision: 531755
- Rebuild for new OpenSSL

* Tue Mar 30 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-1mdv2010.1
+ Revision: 528940
- 3.1.1 stable

* Sat Mar 27 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100327.9mdv2010.1
+ Revision: 527891
- New snapshot
  Hopefully we have fixed the initrd start failure
  We put now pid file in /var/run as Squid3.1 can modify by configure option its path

* Thu Mar 25 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100324.8mdv2010.1
+ Revision: 527325
+ rebuild (emptylog)

* Thu Mar 25 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100324.7mdv2010.1
+ Revision: 527320
- New snapshoot:
  No pinger, as upstream has disable because there are problems
  We put now squid.pid file in place, so init.d service should start now okay

* Mon Mar 22 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100316.6mdv2010.1
+ Revision: 526606
-D off from squid.init

* Mon Mar 22 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100316.5mdv2010.1
+ Revision: 526404
- Getting rid of -D complain

* Sun Mar 21 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100316.4mdv2010.1
+ Revision: 526284
+ rebuild (emptylog)

* Sun Mar 21 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100316.3mdv2010.1
+ Revision: 525980
- P1 rediff to let squid 3.1 auto-localize feature work

* Sat Mar 20 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100316.2mdv2010.1
+ Revision: 525374
- Ecap enabled

* Sat Mar 20 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.1-0.0.beta18.20100316.1mdv2010.1
+ Revision: 525365
- No ecap by now
- 3.1 beta18 hits!
  P4, not needed anymore, Sq3.1 is awared of new kernel header
  P12, is not needed by now (could be  --disable-strict-error-checkin)
  P15, merged upstream
  New storio-io and disk-io handlers
  SMB auth helper has been renamed to smb_lm
  We need to tell Squid if it uses MIT or Heimdal, MIT by now
  Several files fixes

* Mon Mar 15 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-34mdv2010.1
+ Revision: 519942
- New stable 25

* Mon Mar 08 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-33mdv2010.1
+ Revision: 516138
- P15 to fix a cosmetic issue with Digest related to nonce, will remove on next stable

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0-32mdv2010.1
+ Revision: 511640
- rebuilt against openssl-0.9.8m

* Wed Feb 24 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-31mdv2010.1
+ Revision: 510496
- squid cert for https reverse

* Fri Feb 12 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-30mdv2010.1
+ Revision: 504967
- STABLE24, it fix a DoS with HTCP

* Tue Feb 02 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-29mdv2010.1
+ Revision: 499738
- P5 dropped, merged upstream
- New 3.0.23

* Mon Feb 01 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0-28mdv2010.1
+ Revision: 499085
- 3.0.STABLE22
- P5: fix build

* Tue Jan 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-27mdv2010.1
+ Revision: 493884
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Tue Jan 19 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-26mdv2010.1
+ Revision: 493476
- squid autoreload sintax error, fixed
- squid autoreload sintax error, fixed

* Mon Jan 18 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-25mdv2010.1
+ Revision: 493437
- new var in sysconfig

* Mon Jan 18 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-24mdv2010.1
+ Revision: 493430
- New S14 to fix #56191

* Thu Dec 24 2009 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-23mdv2010.1
+ Revision: 482163
- Stable 21

* Tue Nov 03 2009 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-22mdv2010.1
+ Revision: 460411
- P4 rediffed, P14 dropped merged upstream

* Thu Oct 15 2009 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-21mdv2010.0
+ Revision: 457479
- 8192 descriptors by default, this will help squid performance in mid-size to huge-size deployments

* Fri Sep 25 2009 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 3.0-20mdv2010.0
+ Revision: 448587
- SPEC minor change in .patch14
- Redif patch 14, to let it work
- Fix RFC2069 bug
  http://bugs.squid-cache.org/show_bug.cgi?id=2773

* Sat Sep 12 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-19mdv2010.0
+ Revision: 438551
- 3.0.STABLE19

* Wed Aug 05 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-18mdv2010.0
+ Revision: 410317
- 3.0.STABLE18

* Sun Jul 26 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-17mdv2010.0
+ Revision: 400457
- 3.0.STABLE17

* Thu Jun 18 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-16mdv2010.0
+ Revision: 387108
- 3.0.STABLE16
- rediffed one patch
- added a patch from gentoo that makes it build

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-15mdv2010.0
+ Revision: 375343
- 3.0.STABLE15

* Sat Apr 11 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-14mdv2009.1
+ Revision: 366234
- 3.0.STABLE14

* Thu Feb 05 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-13mdv2009.1
+ Revision: 337774
- 3.0.STABLE13

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-12mdv2009.1
+ Revision: 335757
- 3.0.STABLE12

* Tue Jan 13 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0-11mdv2009.1
+ Revision: 329210
- 3.0.STABLE11

* Wed Dec 17 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-10mdv2009.1
+ Revision: 315098
- rediffed fuzzy patches

* Mon Oct 27 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-9mdv2009.1
+ Revision: 297562
- 3.0.STABLE10
- rediffed P10

* Wed Sep 24 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-8mdv2009.0
+ Revision: 287774
- 3.0.STABLE9
- rediffed P1,P13

* Mon Aug 11 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-7mdv2009.0
+ Revision: 270890
- 3.0.STABLE8

* Tue Jun 24 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-6mdv2009.0
+ Revision: 228604
- 3.0.STABLE7
- really fix #41121
- revert to the old behaviour
- fix #41121 (squid init script reinitializes alternate format swap_dir's)

* Wed May 28 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-5mdv2009.0
+ Revision: 212752
- disable the cppunit test suite for now, enable it later
- 3.0.STABLE6

* Mon May 12 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-4mdv2009.0
+ Revision: 206214
- rebuild
- 3.0.STABLE5
- drop the squid-xforward_logging patch, it's not maintained
- revert the "conform to the 2008 specs (don't start the services per
  default)" changes and let this be handled some other way...
- enable the test suite (with a conditional twist)

* Fri Apr 18 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-2mdv2009.0
+ Revision: 195627
- 3.0.STABLE4

* Mon Feb 18 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-1mdv2008.1
+ Revision: 171230
- add a virtal provides of webproxy

* Tue Jan 29 2008 Andreas Hasenack <andreas@mandriva.com> 3.0-0.1mdv2008.1
+ Revision: 159758
- add krb5-devel to buildrequires
- from oden: updated to version 3.0.STABLE1

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 2.6.STABLE17-4mdv2008.1
+ Revision: 157273
- rebuild with fixed %%serverbuild macro

* Tue Jan 08 2008 Andreas Hasenack <andreas@mandriva.com> 2.6.STABLE17-3mdv2008.1
+ Revision: 146558
- fix icap memory leak (#35992)

* Fri Dec 21 2007 Oden Eriksson <oeriksson@mandriva.com> 2.6.STABLE17-2mdv2008.1
+ Revision: 136292
- rebuilt against new build deps

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 03 2007 Andreas Hasenack <andreas@mandriva.com> 2.6.STABLE17-1mdv2008.1
+ Revision: 114478
- updated to version 2.6.17

* Thu Sep 06 2007 Oden Eriksson <oeriksson@mandriva.com> 2.6.STABLE16-1mdv2008.0
+ Revision: 80633
- 2.6.STABLE16
- rediffed P1,P300

* Wed Aug 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.6.STABLE14-1mdv2008.0
+ Revision: 60347
- 2.6.STABLE13
- obey the 2008 specs (don't start it per default)

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 2.6.STABLE13-3mdv2008.0
+ Revision: 45067
- rebuild with new serverbuild macro (-fstack-protector-all)

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 2.6.STABLE13-2mdv2008.0
+ Revision: 43207
- use serverbuild macro

* Mon Jun 04 2007 Oden Eriksson <oeriksson@mandriva.com> 2.6.STABLE13-1mdv2008.0
+ Revision: 35116
- 2.6.STABLE13
- rediffed P300

* Mon Jun 04 2007 Oden Eriksson <oeriksson@mandriva.com> 2.6.STABLE12-1mdv2008.0
+ Revision: 35052
- 2.6.STABLE12
- new icap patch (P300)
- compile fixes conserning P300 by boklm (P400,P401)
- drop upstream applied patches; P10

