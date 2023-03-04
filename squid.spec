%define __perl_requires %{SOURCE98}

Name:     squid
Version:  5.8
Release:  1
Summary:  The Squid proxy caching server
# See CREDITS for breakdown of non GPLv2+ code
License:  GPLv2+ and (LGPLv2+ and MIT and BSD and Public Domain)
URL:      http://www.squid-cache.org

Source0:  http://www.squid-cache.org/Versions/v5/squid-%{version}.tar.xz
Source1:  http://www.squid-cache.org/Versions/v5/squid-%{version}.tar.xz.asc
Source2:  http://www.squid-cache.org/pgp.asc
Source3:  https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid.logrotate
Source4:  https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid.sysconfig
Source5:  https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid.pam
Source6:  https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid.nm
Source7:  https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid.service
Source8:  https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/cache_swap.sh
Source9:  https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid.sysusers

Source98: https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/perl-requires-squid.sh

# Upstream patches

# Backported patches
Patch101: https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid-5.7-ip-bind-address-no-port.patch

# Fedora patches
# Applying upstream patches first makes it less likely that local patches
# will break upstream ones.
Patch201: https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid-4.0.11-config.patch
Patch202: https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid-3.1.0.9-location.patch
Patch203: https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid-3.0.STABLE1-perlpath.patch
Patch204: https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid-3.5.9-include-guards.patch
# revert this upstream patch - https://bugzilla.redhat.com/show_bug.cgi?id=1936422
# workaround for #1934919
Patch205: https://src.fedoraproject.org/rpms/squid/raw/rawhide/f/squid-5.0.5-symlink-lang-err.patch

# cache_swap.sh
Requires: bash gawk

# squid_ldap_auth and other LDAP helpers require OpenLDAP
BuildRequires: make
BuildRequires: openldap-devel
# squid_pam_auth requires PAM development libs
BuildRequires: pam-devel
# SSL support requires OpenSSL
BuildRequires: pkgconfig(openssl)
# squid_kerb_aut requires Kerberos development libs
BuildRequires: krb5-devel
# time_quota requires TrivialDB
BuildRequires: pkgconfig(tdb)
# ESI support requires Expat & libxml2
BuildRequires: expat-devel libxml2-devel
# TPROXY requires libcap, and also increases security somewhat
BuildRequires: libcap-devel
# eCAP support
BuildRequires: pkgconfig(libecap)
#ip_user helper requires
BuildRequires: gcc-c++
BuildRequires: libtool libltdl-devel
BuildRequires: atomic-devel
BuildRequires: perl-generators
# For test suite
BuildRequires: pkgconfig(cppunit)
# For verifying downloded src tarball
BuildRequires: gnupg2
# for _tmpfilesdir and _unitdir macro
# see https://docs.fedoraproject.org/en-US/packaging-guidelines/Systemd/#_packaging
BuildRequires: systemd-rpm-macros
# systemd notify
BuildRequires: pkgconfig(systemd)

%{?systemd_requires}
%{?sysusers_requires_compat}

# Old NetworkManager expects the dispatcher scripts in a different place
Conflicts: NetworkManager < 1.20

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

%prep
%setup -q

# Upstream patches

# Backported patches
%patch101 -p1 -b .ip-bind-address-no-port

# Local patches
%patch201 -p1 -b .config
%patch202 -p1 -b .location
%patch203 -p1 -b .perlpath
%patch204 -p0 -b .include-guards
%patch205 -p1 -R -b .symlink-lang-err

# https://bugzilla.redhat.com/show_bug.cgi?id=1679526
# Patch in the vendor documentation and used different location for documentation
sed -i 's|@SYSCONFDIR@/squid.conf.documented|%{_pkgdocdir}/squid.conf.documented|' src/squid.8.in

%build

# NIS helper has been removed because of the following bug
# https://bugzilla.redhat.com/show_bug.cgi?id=1531540
%configure \
   --libexecdir=%{_libdir}/squid \
   --datadir=%{_datadir}/squid \
   --sysconfdir=%{_sysconfdir}/squid \
   --with-logdir='%{_localstatedir}/log/squid' \
   --with-pidfile='/run/squid.pid' \
   --disable-dependency-tracking \
   --enable-eui \
   --enable-follow-x-forwarded-for \
   --enable-auth \
   --enable-auth-basic="DB,fake,getpwnam,LDAP,NCSA,PAM,POP3,RADIUS,SASL,SMB,SMB_LM" \
   --enable-auth-ntlm="SMB_LM,fake" \
   --enable-auth-digest="file,LDAP" \
   --enable-auth-negotiate="kerberos" \
   --enable-external-acl-helpers="LDAP_group,time_quota,session,unix_group,wbinfo_group,kerberos_ldap_group" \
   --enable-storeid-rewrite-helpers="file" \
   --enable-cache-digests \
   --enable-cachemgr-hostname=localhost \
   --enable-delay-pools \
   --enable-epoll \
   --enable-icap-client \
   --enable-ident-lookups \
   %ifnarch %{power64} ia64 x86_64 s390x aarch64
   --with-large-files \
   %endif
   --enable-linux-netfilter \
   --enable-removal-policies="heap,lru" \
   --enable-snmp \
   --enable-ssl \
   --enable-ssl-crtd \
   --enable-storeio="aufs,diskd,ufs,rock" \
   --enable-diskio \
   --enable-wccpv2 \
   --enable-esi \
   --enable-ecap \
   --with-aio \
   --with-default-user="squid" \
   --with-dl \
   --with-openssl \
   --with-pthreads \
   --disable-arch-native \
   --disable-security-cert-validators \
   --disable-strict-error-checking \
   --with-swapdir=%{_localstatedir}/spool/squid

rm libltdl/config-h.in
cp -f /usr/share/libtool/config-h.in libltdl/

# workaround to build squid v5
mkdir -p src/icmp/tests
mkdir -p tools/squidclient/tests
mkdir -p tools/tests

%make_build

%check
#make check

%install
%make_install

echo "
#
# This is %{_sysconfdir}/httpd/conf.d/squid.conf
#

ScriptAlias /Squid/cgi-bin/cachemgr.cgi %{_libdir}/squid/cachemgr.cgi

# Only allow access from localhost by default
<Location /Squid/cgi-bin/cachemgr.cgi>
 Require local
 # Add additional allowed hosts as needed
 # Require host example.com
</Location>" > $RPM_BUILD_ROOT/squid.httpd.tmp


mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/NetworkManager/dispatcher.d
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/squid
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/squid
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/squid
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/squid
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}
install -m 755 %{SOURCE8} $RPM_BUILD_ROOT%{_libexecdir}/squid
install -m 644 $RPM_BUILD_ROOT/squid.httpd.tmp $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/squid.conf
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_prefix}/lib/NetworkManager/dispatcher.d/20-squid
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/squid
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/spool/squid
mkdir -p $RPM_BUILD_ROOT/run/squid
chmod 644 contrib/url-normalizer.pl contrib/user-agents.pl

# install /usr/lib/tmpfiles.d/squid.conf
mkdir -p ${RPM_BUILD_ROOT}%{_tmpfilesdir}
cat > ${RPM_BUILD_ROOT}%{_tmpfilesdir}/squid.conf <<EOF
# See tmpfiles.d(5) for details

d /run/squid 0755 squid squid - -
EOF

# Move the MIB definition to the proper place (and name)
mkdir -p $RPM_BUILD_ROOT/usr/share/snmp/mibs
mv $RPM_BUILD_ROOT/usr/share/squid/mib.txt $RPM_BUILD_ROOT/usr/share/snmp/mibs/SQUID-MIB.txt

# squid.conf.documented is documentation. We ship that in doc/
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/squid/squid.conf.documented

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT/squid.httpd.tmp

# sysusers.d
install -p -D -m 0644 %{SOURCE9} %{buildroot}%{_sysusersdir}/squid.conf

%files
%license COPYING 
%doc CONTRIBUTORS README ChangeLog QUICKSTART src/squid.conf.documented
%doc contrib/url-normalizer.pl contrib/user-agents.pl

%{_unitdir}/squid.service
%attr(755,root,root) %dir %{_libexecdir}/squid
%attr(755,root,root) %{_libexecdir}/squid/cache_swap.sh
%attr(755,root,root) %dir %{_sysconfdir}/squid
%attr(755,root,root) %dir %{_libdir}/squid
%attr(770,squid,root) %dir %{_localstatedir}/log/squid
%attr(750,squid,squid) %dir %{_localstatedir}/spool/squid
%attr(755,squid,squid) %dir /run/squid

%config(noreplace) %attr(644,root,root) %{_sysconfdir}/httpd/conf.d/squid.conf
%config(noreplace) %attr(640,root,squid) %{_sysconfdir}/squid/squid.conf
%config(noreplace) %attr(644,root,squid) %{_sysconfdir}/squid/cachemgr.conf
%config(noreplace) %{_sysconfdir}/squid/mime.conf
%config(noreplace) %{_sysconfdir}/squid/errorpage.css
%config(noreplace) %{_sysconfdir}/sysconfig/squid
# These are not noreplace because they are just sample config files
%config %{_sysconfdir}/squid/squid.conf.default
%config %{_sysconfdir}/squid/mime.conf.default
%config %{_sysconfdir}/squid/errorpage.css.default
%config %{_sysconfdir}/squid/cachemgr.conf.default
%config(noreplace) %{_sysconfdir}/pam.d/squid
%config(noreplace) %{_sysconfdir}/logrotate.d/squid

%dir %{_datadir}/squid
%attr(-,root,root) %{_datadir}/squid/errors
%{_prefix}/lib/NetworkManager
%{_datadir}/squid/icons
%{_sbindir}/squid
%{_bindir}/squidclient
%{_bindir}/purge
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_libdir}/squid/*
%{_datadir}/snmp/mibs/SQUID-MIB.txt
%{_tmpfilesdir}/squid.conf
%{_sysusersdir}/squid.conf

%pre
%sysusers_create_compat %{SOURCE9}

for i in /var/log/squid /var/spool/squid ; do
        if [ -d $i ] ; then
                for adir in `find $i -maxdepth 0 \! -user squid`; do
                        chown -R squid:squid $adir
                done
        fi
done

exit 0

%pretrans -p <lua>
-- temporarilly commented until https://bugzilla.redhat.com/show_bug.cgi?id=1936422 is resolved
--
-- previously /usr/share/squid/errors/es-mx was symlink, now it is directory since squid v5
-- see https://docs.fedoraproject.org/en-US/packaging-guidelines/Directory_Replacement/
-- Define the path to the symlink being replaced below.
--
-- path = "/usr/share/squid/errors/es-mx"
-- st = posix.stat(path)
-- if st and st.type == "link" then
--   os.remove(path)
-- end

-- Due to a bug #447156
paths = {"/usr/share/squid/errors/zh-cn", "/usr/share/squid/errors/zh-tw"}
for key,path in ipairs(paths)
do
  st = posix.stat(path)
  if st and st.type == "directory" then
    status = os.rename(path, path .. ".rpmmoved")
    if not status then
      suffix = 0
      while not status do
        suffix = suffix + 1
        status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
      end
      os.rename(path, path .. ".rpmmoved")
    end
  end
end

%post
%systemd_post squid.service

%preun
%systemd_preun squid.service

%postun
%systemd_postun_with_restart squid.service

%triggerin -- samba-common
if ! getent group wbpriv >/dev/null 2>&1 ; then
  /usr/sbin/groupadd -g 88 wbpriv >/dev/null 2>&1 || :
fi
/usr/sbin/usermod -a -G wbpriv squid >/dev/null 2>&1 || \
    chgrp squid /var/cache/samba/winbindd_privileged >/dev/null 2>&1 || :
