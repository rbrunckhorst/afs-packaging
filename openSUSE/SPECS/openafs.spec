#
# spec file for package openafs
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
# needssslcertforbuild


#Compat macro for new _fillupdir macro introduced in Nov 2017
%if ! %{defined _fillupdir}
%define _fillupdir /var/adm/fillup-templates
%endif
%define _lto_cflags %{nil} 

#
#	TUNABLES
#
#
# Determine presence of rpmbuild command line --define arguments and set
# defaults if not present.
#
%define build_userspace_on_cmdline %{?build_userspace:1}%{!?build_userspace:0}
%define build_kernel_modules_on_cmdline %{?build_kernel_modules:1}%{!?build_kernel_modules:0}
%define build_dkmspkg_on_cmdline %{?build_dkmspkg:1}%{!?build_dkmspkg:0}
%define kernelvers %{?kernvers}

# package-wide definitions here

# build authlibs
%define build_authlibs 1

# build userspace
%if !%{build_userspace_on_cmdline}
%define build_userspace 1
%endif

# build kernel modules
%if !%{build_kernel_modules_on_cmdline}
%define build_kernel_modules 1
%endif

# build dkmspkg_
%if !%{build_dkmspkg_on_cmdline}
%define build_dkmspkg 1
%endif

# flag for firewalld, only required for SLE-12
%if 0%{?sle_version} <= 120500 && !0%{?is_opensuse} 
%define have_firewalld 0
%else
%define have_firewalld 1
%endif

#
# package internal directories
#
%define filelayout        fhs
%define afslogsdir        /var/log/openafs
%define afsconfdir        /etc/openafs/server
%define viceetcdir        /etc/openafs
%define vicecachedir      /var/cache/openafs
%define afslocaldir       /var/lib/openafs

%ifarch ppc64le ppc64 %{arm}
%define build_kernel_modules 0
%endif

# used for %setup only
# leave upstream tar-balls untouched for integrity checks.

# update with the version in the tar files (e.g. 1.8.8.1-8-gl18924 )
%define upstream_version %{tarversion}
%define package_version %{?afsversion}%{!?afsversion:%{upstream_version}}
%define release_version %{?release}%{!?release:1}

Name:           openafs

Version:        %{package_version}
Release:        %{release_version}%{?dist}
Summary:        OpenAFS Distributed File System
License:        IPL-1.0
Group:          System/Filesystems
Packager:       Sine Nomine Associates <openafs@sinenomine.net>
Vendor:         Sine Nomine Associates
URL:            http://www.openafs.org/

Source0:        openafs-%{upstream_version}-src.tar.bz2
Source1:        openafs-%{upstream_version}-doc.tar.bz2
Source2:        openafs-%{upstream_version}-src.tar.bz2.md5
Source3:        openafs-%{upstream_version}-doc.tar.bz2.md5
Source4:        openafs-%{upstream_version}-src.tar.bz2.sha256
Source5:        openafs-%{upstream_version}-doc.tar.bz2.sha256

Source10:       README.SUSE.openafs
Source15:       logrotate.openafs-server
Source18:       RELNOTES
Source19:       ChangeLog
Source20:       kernel-source.build-modules.sh
Source23:       openafs-client.service
Source24:       openafs-client.service.allow_unsupported
Source25:       openafs-server.service
Source26:       openafs-fuse-client.service
Source27:       sysconfig.openafs-client
Source28:       sysconfig.openafs-server
Source29:       sysconfig.openafs-fuse-client
Source30:       preamble
Source40:       afs3-bos.xml
Source41:       afs3-callback.xml
Source42:       afs3-fileserver.xml
Source43:       afs3-prserver.xml
Source44:       afs3-rmtsys.xml
Source45:       afs3-update.xml
Source46:       afs3-vlserver.xml
Source47:       afs3-volser.xml
Source55:       openafs.SuidCells
Source56:       openafs.CellAlias
Source57:       openafs.ThisCell
Source58:       openafs.cacheinfo
Source99:       openafs.changes

#
#	GENERAL BuildRequires and Requires
#

BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  coreutils
BuildRequires:  fdupes
%if %{have_firewalld}
BuildRequires:  firewall-macros
%endif
BuildRequires:  flex
BuildRequires:  fuse-devel
BuildRequires:  git
BuildRequires:  krb5-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libtool
BuildRequires:  ncurses-devel
%if 0%{?suse_version} < 1120
BuildRequires:  perl-macros
%endif
BuildRequires:  pkg-config
BuildRequires:  swig

%if 0%{?suse_version} < 1210
Requires(post): %insserv_prereq
%endif
Requires(post): %fillup_prereq

%if %{build_kernel_modules} 
BuildRequires:  %{kernel_module_package_buildreqs}
%endif

%description  
AFS is a cross-platform distributed file system product pioneered at
Carnegie Mellon University and supported and developed as a product by
Transarc Corporation (now IBM Pittsburgh Labs). It offers a
client-server architecture for file sharing, providing location
independence, scalability, and transparent migration capabilities for
data.

In addition, among its features are authentication, encryption,
caching, disconnected operations, replication for higher availability
and load balancing, and ACLs.

%if %{build_userspace}
%package server
Summary:        OpenAFS File System Server
Group:          System/Filesystems
Requires:       %{name} = %{version}

%description server
AFS is a cross-platform distributed file system product pioneered at
Carnegie Mellon University and supported and developed as a product by
Transarc Corporation (now IBM Pittsburgh Labs). It offers a
client-server architecture for file sharing, providing location
independence, scalability, and transparent migration capabilities for
data.

In addition, among its features are authentication, encryption,
caching, disconnected operations, replication for higher availability
and load balancing, and ACLs. This package contains the static
libraries and header files needed to develop applications for OpenAFS.

%if %{build_authlibs}
%package authlibs
Summary:        OpenAFS authentication shared libraries
Group:          Development/Libraries/C and C++

%description authlibs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides a shared version of libafsrpc and libafsauthent.
None of the programs included with OpenAFS currently use these shared
libraries; however, third-party software that wishes to perform AFS
authentication may link against them.

%package authlibs-devel
Summary:        OpenAFS shared library development
Group:          Development/Libraries/C and C++
Requires:       %{name}-authlibs = %{version}
Requires:       %{name}-devel = %{version}

%description authlibs-devel
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package includes the static versions of libafsrpc and
libafsauthent, and symlinks required for building against the dynamic
libraries.

%endif

%package devel
Summary:        OpenAFS Static Libraries and Header Files
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}

%description devel
AFS is a cross-platform distributed file system product pioneered at
Carnegie Mellon University and supported and developed as a product by
Transarc Corporation (now IBM Pittsburgh Labs). It offers a
client-server architecture for file sharing, providing location
independence, scalability, and transparent migration capabilities for
data.

In addition, among its features are authentication, encryption,
caching, disconnected operations, replication for higher availability
and load balancing, and ACLs. This package contains the OpenAFS server.

%package kernel-source
Summary:        OpenAFS Kernel Module source tree
Group:          System/Filesystems
Requires:       bison
Requires:       flex
Requires:       gcc
Requires:       kernel-devel
Requires:       %{name}-devel = %{version}
Provides:       %{name}-kernel = %{version}
Provides:       %{name}-kmp = %{version}

%description kernel-source
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the source code to build your own AFS kernel
module.

%if %{build_dkmspkg}
%package -n dkms-%{name}
Summary:        DKMS-ready kernel source for AFS distributed filesystem
Group:          Development/Kernel
Provides:       %{name}-kernel = %{version}
Provides:       %{name}-kmp = %{version}
Requires(pre):  %{name}-devel = %{version}
Requires(pre):  %{name}-kernel-source = %{version}
Requires(pre):  kernel-devel
Requires(pre):  dkms
Requires(pre):  flex
Requires(pre):  make
Requires(post): dkms

%description -n dkms-%{name}
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the source code to allow DKMS to build an
AFS kernel module.
%endif


%package fuse_client
Summary:        OpenAFS FUSE File System Client
Group:          System/Filesystems
Conflicts:      %{name}-client
Requires:       %{name} = %{version}

%description fuse_client
AFS is a cross-platform distributed file system product pioneered at
Carnegie Mellon University and supported and developed as a product by
Transarc Corporation (now IBM Pittsburgh Labs). It offers a
client-server architecture for file sharing, providing location
independence, scalability, and transparent migration capabilities for
data.

This client is using the EXPERIMENTAL FUSE interface on LINUX.
It does not offer authentication etc. 

%package client
Summary:        OpenAFS File System Client
Group:          System/Filesystems
Requires:       %{name} = %{version}
Requires:       %{name}-kmp >= %{version}
Requires:       krb5-client

%description client
AFS is a cross-platform distributed file system product pioneered at
Carnegie Mellon University and supported and developed as a product by
Transarc Corporation (now IBM Pittsburgh Labs). It offers a
client-server architecture for file sharing, providing location
independence, scalability, and transparent migration capabilities for
data.

In addition, among its features are authentication, encryption,
caching, disconnected operations, replication for higher availability
and load balancing, and ACLs. This package contains the OpenAFS client.

%package client-compat
Summary:        OpenAFS client compatibility symlinks
Group:          System/Filesystems
Requires:       %{name} = %{version}, %{name}-client = %{version}

%description client-compat
AFS is a cross-platform distributed file system product pioneered at
Carnegie Mellon University and supported and developed as a product by
Transarc Corporation (now IBM Pittsburgh Labs). It offers a
client-server architecture for file sharing, providing location
independence, scalability, and transparent migration capabilities for
data.

This package provides compatibility symlinks for legacy layout.
It is completely optional, and is only necessary if legacy layout
is needed. It will create symlinks only for directories.
This package is for the legacy client part (/usr/vice/)

%package server-compat
Summary:        OpenAFS server compatibility symlinks
Group:          System/Filesystems
Requires:       %{name} = %{version}, %{name}-server = %{version}

%description server-compat
AFS is a cross-platform distributed file system product pioneered at
Carnegie Mellon University and supported and developed as a product by
Transarc Corporation (now IBM Pittsburgh Labs). It offers a
client-server architecture for file sharing, providing location
independence, scalability, and transparent migration capabilities for
data.

This package provides compatibility symlinks for legacy layout.
It is completely optional, and is only necessary if legacy layout
is needed. It will create symlinks only for directories.
This package is for the legacy server part (/usr/afs/)

%endif

%if %{build_kernel_modules}
%package KMP
Summary:        OpenAFS Distributed File System - kernel module
Group:          System/Kernel

%kernel_module_package -x lockdep um pae -p %{S:30}

krel=`make -si -C /usr/src/linux-obj/%_target_cpu/default/ ARCH=x86 kernelrelease 2>/dev/null`

%description KMP
This package contains the kernel module for OpenAFS. For details see
the openafs package.

%endif

%prep

: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
: @@@
: @@@ package-name:       %{name}
: @@@ package-version:    %{package_version}
: @@@ package-release:    %{release_version}
: @@@ file-layout:	  %{filelayout}
: @@@ lib dir:    	  %{_libdir}
: @@@ libexec dir:    	  %{_libexecdir}
: @@@ bin dir:    	  %{_bindir}
: @@@ sbin dir:    	  %{_sbindir}
: @@@ include dir:    	  %{includedir}
: @@@ sysconf dir:    	  %{_sysconfdir}
: @@@ man dir:    	  %{_mandir}
: @@@ build userspace:    %{build_userspace}
: @@@ build modules:      %{build_kernel_modules}
: @@@ build dkmspkg:      %{build_dkmspkg}
: @@@ architecture:       %{_arch}
: @@@ target cpu:         %{_target_cpu}
: @@@
: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

for src_file in %{S:0}  %{S:1}; do
    if [ "`md5sum $src_file | awk '{print $1}'`" != "`cat $src_file.md5 | awk '{print $1}'`" ]; then 
        echo "ERROR: MD5-Integrity check for $src_file failed."; 
        exit 1
    fi
    if [ "`sha256sum $src_file | awk '{print $1}'`" != "`cat $src_file.sha256 | awk '{print $1}'`" ]; then 
        echo "ERROR: SHA256-Integrity check for $src_file failed."; 
        exit 1
    fi
done

%setup -q -n openafs-%{upstream_version} -T -b 0 -b 1

./regen.sh

%build
# architecture specific settings
sysbase=%{_arch}

%ifarch ppc
perl -pi -e 's,^(XCFLAGS.*),\1 -fPIC,' src/config/Makefile.ppc_linux24.in
%endif
%ifarch ppc64 ppc64le
sysbase=ppc64
export LDFLAGS="$LDFLAGS -m64"
%endif
%ifarch %{arm}
sysbase=arm
%endif
%ifarch aarch64
sysbase=arm64
%define _arch arm64
%endif
%ifarch s390x
sysbase=s390
%endif
%ifarch x86_64
sysbase=amd64
perl -pi -e 's,^(XCFLAGS.*),\1 -fPIC,' src/config/Makefile.amd64_linux24.in
perl -pi -e 's,^(XLIBS.*),\1 -lresolv,' src/config/Makefile.amd64_linux24.in
%endif

afs_sysname=${sysbase}_linux26

RPM_OPT_FLAGS=`echo ${RPM_OPT_FLAGS} | sed s/-D_FORTIFY_SOURCE=2//`
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fPIC -fcommon" 

export KRB5LIBS='-lcom_err -lkrb5'
export PATH_KRB5_CONFIG=%{krb5_config}

#afslogsdir=/var/log/openafs ./configure \
afslogsdir=/var/log/openafs; export afslogsdir; %configure \
    --disable-transarc-paths \
    --disable-pam \
    --disable-strip-binaries \
    --includedir=%{_includedir}/openafs \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --with-afs-sysname=$afs_sysname \
    --disable-kernel-module \
    --with-swig

%if %{build_userspace}
make CCFLAGS="$CFLAGS" XCFLAGS="$CFLAGS" PAM_CFLAGS="$CFLAGS" KOPTS="$CFLAGS" all_nolibafs
%endif
make CCFLAGS="$CFLAGS" XCFLAGS="$CFLAGS" PAM_CFLAGS="$CFLAGS" KOPTS="$CFLAGS" only_libafs_tree

# the test suite need a configured KDC
#make -C src/tests all

# Kernel-module

%if %{build_kernel_modules}
mkdir obj

for flavor in %flavors_to_build; do
    if [ -n "%{kernelvers}" ]; then
    krel=$(make -si -C /usr/src/linux-obj/%_target_cpu/$flavor/ ARCH=x86 kernelrelease 2>/dev/null)
    kver=${krel%%-*}
    if [ "$kver" != %{kernelvers} ]; then 
        echo "ERROR: Kernel-version check $kver failed."; 
        exit 1
    fi
    fi
    rm -rf obj/$flavor
    cp -a libafs_tree obj/$flavor
    pushd obj/$flavor
    find . -name "*.c" -exec sed -i '/MODULE_LICENSE(/a MODULE_INFO(retpoline, "Y");' "{}" "+"
    ./configure  --with-linux-kernel-build=/usr/src/linux-obj/%{_target_cpu}/$flavor --with-linux-kernel-headers=/usr/src/linux \
    --disable-transarc-paths --without-swig
    export EXTRA_CFLAGS='-DVERSION=\"%version\"'
    export LINUX_MAKE_ARCH="ARCH=%{_arch}"
    make
    popd
done
%endif # build_kernel_modules

%install

#
# install build binaries using  make 
%if %{build_userspace}
make DESTDIR=%{buildroot} install_nolibafs

#
# man-pages 

OLD_PWD=`pwd`
cd doc/man-pages
%make_install
cd $OLD_PWD

#
# create directories
mkdir -p %{buildroot}/%_unitdir
mkdir -p %{buildroot}/%{afslogsdir}/old
mkdir -p %{buildroot}/%{_fillupdir}
mkdir -p %{buildroot}/%{vicecachedir}
mkdir -p %{buildroot}/%{viceetcdir}
mkdir -p %{buildroot}%{_datadir}/openafs/C
mkdir -p %{buildroot}/%{afsconfdir}
mkdir -p %{buildroot}/%{afslocaldir}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/usr/vice
mkdir -p %{buildroot}/usr/afs

#
# client
cp -a src/afsd/CellServDB %{buildroot}/%{viceetcdir}/CellServDB
cp -a %{S:55} %{buildroot}/%{viceetcdir}/SuidCells
cp -a %{S:56} %{buildroot}/%{viceetcdir}/CellAlias
cp -a %{S:57} %{buildroot}/%{viceetcdir}/ThisCell
cp -a %{S:58} %{buildroot}/%{viceetcdir}/cacheinfo
cp -a src/afs/afszcm.cat %{buildroot}%{_datadir}/openafs/C
install -m 644 %{S:27} %{buildroot}/%{_fillupdir}/sysconfig.openafs-client
%if 0%{?sle_version} > 150000 
install -m 644 %{S:24} %{buildroot}/%_unitdir/openafs-client.service
%else
install -m 644 %{S:23} %{buildroot}/%_unitdir
%endif
ln -s %{_sbindir}/service %{buildroot}/%{_sbindir}/rcopenafs-client

#
# fuse client package
install -m 644 %{S:29} %{buildroot}/%{_fillupdir}/sysconfig.openafs-fuse-client
install -m 644 %{S:26} %{buildroot}/%_unitdir
ln -s %{_sbindir}/service %{buildroot}/%{_sbindir}/rcopenafs-fuse-client

# 
# server
install -m 644 %{S:28} %{buildroot}/%{_fillupdir}/sysconfig.openafs-server
install -m 644 %{S:25} %{buildroot}/%_unitdir
ln -s %{_sbindir}/service %{buildroot}/%{_sbindir}/rcopenafs-server

#
# kernel-source 
mkdir -p %{buildroot}/usr/src/kernel-modules/openafs
chmod -R o-w src/libafs
chmod -R o-w libafs_tree
cp -a libafs_tree %{buildroot}/usr/src/kernel-modules/openafs
install -m 755 %{S:20} %{buildroot}/usr/src/kernel-modules/openafs/build-modules.sh
install -m 644 LICENSE %{buildroot}/usr/src/kernel-modules/openafs/LICENSE

#-----------------------------------------------------------------------------
# Install DKMS source.
#-----------------------------------------------------------------------------
install -d -m 755 %{buildroot}/usr/src
cp -a libafs_tree %{buildroot}/usr/src/%{name}-%{version}

cat > %{buildroot}/usr/src/%{name}-%{version}/dkms.conf <<"EOF"

PACKAGE_VERSION="%{version}"

# Items below here should not have to change with each driver version.
PACKAGE_NAME="%{name}"
MAKE[0]='./configure --with-linux-kernel-headers=/usr/src/linux/ --with-linux-kernel-build=$kernel_source_dir && make && case "${kernelver_array[0]}${kernelver[0]}" in 2.4.*) mv src/libafs/MODLOAD-*/libafs-* libafs.o ;; *) mv src/libafs/MODLOAD-*/libafs.ko . ;; esac'
CLEAN="if [ -e src/libafs/Makefile ]; then make -C src/libafs clean; else true; fi"

BUILT_MODULE_NAME[0]="libafs"
DEST_MODULE_LOCATION[0]="/updates/"
STRIP[0]=no
AUTOINSTALL=yes
NO_WEAK_MODULES="true"

EOF


#
# main package
cp -a %{S:10} README.SUSE
cp -a %{S:18} RELNOTES
cp -a %{S:19} ChangeLog
mkdir -p %{buildroot}/etc/ld.so.conf.d
echo %{_libdir}/openafs > %{buildroot}/etc/ld.so.conf.d/openafs.conf

# move some bin to sbin
mv %{buildroot}/%{_bindir}/asetkey %{buildroot}/%{_sbindir}/asetkey
mv %{buildroot}/%{_bindir}/bos %{buildroot}/%{_sbindir}/bos
mv %{buildroot}/%{_bindir}/akeyconvert %{buildroot}/%{_sbindir}/akeyconvert
mv %{buildroot}/%{_bindir}/udebug %{buildroot}/%{_sbindir}/udebug

# avoid conflicts with other packages by adding the prefix afs_ to filenames
mv %{buildroot}%{_bindir}/scout %{buildroot}%{_bindir}/afs_scout
cat %{buildroot}/%{_mandir}/man1/scout.1 | sed 's/\<scout\>/afs_scout/g' > %{buildroot}/%{_mandir}/man1/afs_scout.1
rm %{buildroot}/%{_mandir}/man1/scout.1 
mv %{buildroot}%{_sbindir}/backup %{buildroot}%{_sbindir}/afs_backup
OLD_PWD=`pwd`
cd %{buildroot}/%{_mandir}/man8/
for f in $(ls backup*); do 
    cat $f | sed 's/\<backup\>/afs_backup/g' > afs_"$f"
    rm $f
done
cd $OLD_PWD

# create manpage for afsd.fuse as a real file
rm %{buildroot}/%{_mandir}/man8/afsd.fuse.8
cp -p %{buildroot}/%{_mandir}/man8/afsd.8 %{buildroot}/%{_mandir}/man8/afsd.fuse.8

# move  %%{_libdir}/afs-stuff to %%{_libdir}/openafs
mv %{buildroot}/%{_libdir}/afs/* %{buildroot}/%{_libdir}/openafs
mv %{buildroot}/%{_libdir}/*.* %{buildroot}/%{_libdir}/openafs
rm -rf %{buildroot}/%{_libdir}/afs

# move perl module to perl vendor library path
mkdir -p %{buildroot}/%{perl_vendorlib}/AFS
mv %{buildroot}/%{_libdir}/perl/AFS/ukernel.pm %{buildroot}/%{perl_vendorlib}/AFS/ukernel.pm
mkdir -p %{buildroot}%{perl_vendorarch}
mv %{buildroot}/%{_libdir}/perl/ukernel.so %{buildroot}/%{perl_vendorarch}/ukernel.so

# firewalld

%if %{have_firewalld}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:40} %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:41} %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:42} %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:43} %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:44} %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:45} %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:46} %{buildroot}%{_prefix}/lib/firewalld/services/
install -D -m 644 %{S:47} %{buildroot}%{_prefix}/lib/firewalld/services/
%endif


#
# client-compat

mkdir -p %{buildroot}/usr/vice
ln -s %{viceetcdir} %{buildroot}/usr/vice/etc
ln -s %{vicecachedir} %{buildroot}/usr/vice/cache

#
# server-compat

mkdir -p %{buildroot}/usr/afs
ln -s %{_libexecdir}/openafs %{buildroot}/usr/afs/bin
ln -s %{afslogsdir} %{buildroot}/usr/afs/logs
ln -s %{afsconfdir} %{buildroot}/usr/afs/etc
ln -s %{viceetcdir} %{buildroot}/usr/afs/local
ln -s %{afslocaldir}/db %{buildroot}/usr/afs/db

#
# client|server-compat

%dnl ln -s %{_libdir}/openafs/libafshcrypto.so.2.0.0 %{buildroot}/%{_libdir}/libafshcrypto.so.2.0.0
%dnl ln -s %{_libdir}/openafs/libafshcrypto.so.2 %{buildroot}/%{_libdir}/libafshcrypto.so.2
%dnl ln -s %{_libdir}/openafs/librokenafs.so.2.0.0 %{buildroot}/%{_libdir}/librokenafs.so.2.0.0
%dnl ln -s %{_libdir}/openafs/librokenafs.so.2 %{buildroot}/%{_libdir}/librokenafs.so.2

#
# general cleanup
#

# we supposedly don't need this on linux
rm %{buildroot}/%{_sbindir}/rmtsysd

%if %{build_authlibs} == 0
rm %{buildroot}/%{_libdir}/libafsauthent.so.*
rm %{buildroot}/%{_libdir}/libafsrpc.so.*
rm %{buildroot}/%{_libdir}/libkopenafs.so.*
rm %{buildroot}/%{_libdir}/libafsauthent.so
rm %{buildroot}/%{_libdir}/libafsrpc.so
rm %{buildroot}/%{_libdir}/libkopenafs.so
%endif

# remove all static libraries
find %{buildroot} -type f -name "*.a" -delete

# remove unused man pages
for x in dlog symlink symlink_list symlink_make symlink_remove; do
    rm %{buildroot}/%{_mandir}/man1/${x}.1
done
for x in rmtsysd xfs_size_check aklog_dynamic_auth; do
    rm %{buildroot}/%{_mandir}/man8/${x}.8
done

# compress man pages
OLD_PWD=`pwd`
for d in %{buildroot}%{_mandir}/man*; do
    cd $d
    for f in *; do
        if [ -h $f ]; then
            mv $f $f.gz
        elif [ -f $f ];then
            gzip -9 $f
        else 
            echo "Unknown thing to compress : $f"
        fi
    done
done
cd $OLD_PWD

# replace duplicates by symlinks
%fdupes -s %{buildroot}/usr

%endif

# KMP
%if %{build_kernel_modules}
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=updates

for flavor in %flavors_to_build; do
    make -C /usr/src/linux-obj/%{_arch}/$flavor %{?linux_make_arch} modules_install \
        M=$PWD/`find obj/$flavor/ -name MODLOAD-\* -type d`
done
%endif

#
# main
%if %{build_userspace}
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post kernel-source
echo To install the kernel-module, do:
echo cd /usr/src/kernel-modules/openafs
echo sh ./build-modules.sh build
echo sh ./build-modules.sh install

#
# fuse client

%pre fuse_client
%service_add_pre openafs-fuse-client.service

%preun fuse_client
%service_del_preun openafs-fuse-client.service
%{stop_on_removal}

%post fuse_client
if [ ! -d /afs ]; then
    mkdir /afs
fi
%{fillup_only -n openafs-fuse-client}
%service_add_post openafs-fuse-client.service
/sbin/ldconfig

if [ "x$1" = "x" ]; then
    my_operation=0
else
    my_operation=$1
fi

if [ $my_operation -gt 1 ]; then
    echo Not stopping the possibly running client.
    echo You must restart the client to put the upgrade into effect.
else
    echo This is the experimental FUSE implementation of the openafs-client
    echo Please configure your cell like with the in-kernel openafs-client
    echo authentication etc. is not implemented yet in this version.
fi

%postun fuse_client
%service_del_postun openafs-fuse-client.service
if [ -d /afs ]; then
     echo make sure to remove directory /afs if unwanted.
fi
/sbin/ldconfig

#
# client

%pre client
%service_add_pre openafs-client.service

%post client
if [ ! -d /afs ]; then
    mkdir /afs
fi
/sbin/ldconfig
%{fillup_only -n openafs-client}
%service_add_post openafs-client.service
%if %{have_firewalld}
%firewalld_reload
%endif

if [ "x$1" = "x" ]; then
    my_operation=0
else
    my_operation=$1
fi
if [ $my_operation -gt 1 ]; then
    echo Not stopping the possibly running client.
    echo You must restart the client to put the upgrade into effect.
else 
    echo For configuring the client, please check /etc/sysconfig/openafs-client
    echo and/or follow the instructions found on http://www.openafs.org  how to install an openafs-client. 
fi

%preun client
%{stop_on_removal}
%service_del_preun openafs-client.service

%postun client
if [ -d /afs ]; then
     echo make sure to remove directory /afs if unwanted.
fi
/sbin/ldconfig
%service_del_postun openafs-client.service

#
# server

%pre server
%service_add_pre openafs-server.service

%post server
/sbin/ldconfig
%{fillup_only -n openafs-server}
%service_add_post openafs-server.service

if [ "$FIRST_ARG" -gt 1 ]; then
    # update no new install
    echo Not stopping the possibly running services.
    echo You must restart the service to put the upgrade into effect.
    if [ -d /var/openafs ]; then
         echo To upgrade, stop the server, copy the contents of /var/openafs to /var/lib/openafs,
         echo remove the empty directory /var/openafs and then start the server again. 
    fi
else 
    echo For configuring the server, please check /etc/sysconfig/openafs-server
    echo and/or follow the instructions found on http://www.openafs.org to install an openafs-client. 
fi

%if %{build_dkmspkg}
%post -n dkms-%{name}
dkms add -m %{name} -v %{version} --rpm_safe_upgrade
dkms build -m %{name} -v %{version} --rpm_safe_upgrade
dkms install -m %{name} -v %{version} --rpm_safe_upgrade

%preun -n dkms-%{name}
dkms remove -m %{name} -v %{version} --rpm_safe_upgrade --all ||:
%endif

%preun server
%service_del_preun openafs-server.service
%{stop_on_removal}

%postun server
/sbin/ldconfig
%service_del_postun openafs-server.service

#
# devel

%post devel

%postun devel

#
# authlibs

%if %{build_authlibs}
%post authlibs

%postun authlibs
%endif



%endif
#
#	FILES
#
%if %{build_userspace}
%files           
%defattr(-,root,root)
%config /etc/ld.so.conf.d/openafs.conf
%config(noreplace) %{viceetcdir}/CellAlias
%config(noreplace) %{viceetcdir}/CellServDB
%config(noreplace) %{viceetcdir}/ThisCell
%dir %{viceetcdir}
%doc %{_mandir}/man5/afsmonitor.5.gz
%doc %{_mandir}/man1/afs.1.gz
%doc %{_mandir}/man1/afs_compile_et.1.gz
%doc %{_mandir}/man1/afs_scout.1.gz
%doc %{_mandir}/man1/afsmonitor.1.gz 
%doc %{_mandir}/man1/cmdebug.1.gz
%doc %{_mandir}/man1/pts.1.gz
%doc %{_mandir}/man1/pts_*.gz
%doc %{_mandir}/man1/restorevol.1.gz
%doc %{_mandir}/man1/rxdebug.1.gz
%doc %{_mandir}/man1/sys.1.gz
%doc %{_mandir}/man1/translate_et.1.gz
%doc %{_mandir}/man1/udebug.1.gz
%doc %{_mandir}/man1/vos.1.gz
%doc %{_mandir}/man1/vos_*gz
%doc %{_mandir}/man1/xstat_cm_test.1.gz
%doc %{_mandir}/man1/xstat_fs_test.1.gz
%doc %{_mandir}/man5/CellAlias.5.gz
%doc %{_mandir}/man5/CellServDB.5.gz
%doc %{_mandir}/man5/NetInfo.5.gz
%doc %{_mandir}/man5/NetRestrict.5.gz
%doc %{_mandir}/man5/ThisCell.5.gz
%doc %{_mandir}/man5/afs.5.gz
%doc %{_mandir}/man5/butc.5.gz
%doc %{_mandir}/man5/butc_logs.5.gz
%doc %{_mandir}/man5/fms.log.5.gz
%doc %{_mandir}/man5/sysid.5.gz
%doc %{_mandir}/man5/uss.5.gz
%doc %{_mandir}/man5/uss_*.5.gz
%doc %{_mandir}/man8/afs_backup.8.gz
%doc %{_mandir}/man8/afs_backup_*.8.gz
%doc %{_mandir}/man8/bos.8.gz
%doc %{_mandir}/man8/bos_[a-t]*.8.gz
%doc %{_mandir}/man8/bos_uninstall.8.gz
%doc %{_mandir}/man8/butc.8.gz
%doc %{_mandir}/man8/fms.8.gz
%doc %{_mandir}/man8/read_tape.8.gz
%doc %{_mandir}/man8/uss.8.gz
%doc %{_mandir}/man8/uss_*.8.gz
%doc %{_mandir}/man8/vsys.8.gz
%doc NEWS README* RELNOTES ChangeLog
%{_bindir}/afs_compile_et
%{_bindir}/afs_scout
%{_bindir}/afsio
%{_bindir}/afsmonitor
%{_bindir}/cmdebug
%{_bindir}/pts
%{_bindir}/restorevol
%{_bindir}/sys
%{_bindir}/translate_et
%{_bindir}/xstat_cm_test
%{_bindir}/xstat_fs_test
%{_libdir}/openafs/libafshcrypto.so.*
%{_libdir}/openafs/librokenafs.so.*
%{_sbindir}/afs_backup
%{_sbindir}/bos
%{_sbindir}/butc
%{_sbindir}/fms
%{_sbindir}/read_tape
%{_sbindir}/rxdebug
%{_sbindir}/udebug
%{_sbindir}/uss
%{_sbindir}/vos
%{_sbindir}/vsys

%files fuse_client
%defattr(-,root,root)
%{_sbindir}/afsd.fuse
%{_sbindir}/rcopenafs-fuse-client
%config(noreplace) %{viceetcdir}/SuidCells
%config(noreplace) %{viceetcdir}/cacheinfo
%doc %{_mandir}/man8/afsd.fuse.8.gz
%_unitdir/openafs-fuse-client.service
%{_fillupdir}/sysconfig.openafs-fuse-client
%{vicecachedir}

%files client
%defattr(-,root,root)
 %{_bindir}/fs
 %{_bindir}/aklog
 %{_bindir}/klog.krb5
 %{_bindir}/pagsh
 %{_bindir}/pagsh.krb	
 %{_bindir}/tokens
 %{_bindir}/tokens.krb
 %{_bindir}/unlog
 %{_bindir}/up
 %{_sbindir}/afsd
 %{_sbindir}/fstrace
%doc %{_mandir}/man1/fs.1.gz
%doc %{_mandir}/man1/fs_*.1.gz
%doc %{_mandir}/man1/aklog.1.gz
%doc %{_mandir}/man1/klog.krb5.1.gz
%doc %{_mandir}/man1/pagsh.1.gz
%doc %{_mandir}/man1/pagsh.krb.1.gz
%doc %{_mandir}/man1/tokens.1.gz
%doc %{_mandir}/man1/tokens.krb.1.gz
%doc %{_mandir}/man1/unlog.1.gz
%doc %{_mandir}/man1/up.1.gz
%doc %{_mandir}/man8/afsd.8.gz
%doc %{_mandir}/man8/fstrace.8.gz
%doc %{_mandir}/man8/fstrace_*.8.gz
%_unitdir/openafs-client.service
%doc %{_mandir}/man1/copyauth.1.gz
%doc %{_mandir}/man5/cacheinfo.5.gz
%doc %{_mandir}/man5/afs_cache.5.gz
%dir %{_datadir}/openafs
%dir %{_datadir}/openafs/C
%{_datadir}/openafs/C/afszcm.cat
%doc %{_mandir}/man5/afszcm.cat.5.gz
%config(noreplace) %{viceetcdir}/SuidCells
%config(noreplace) %{viceetcdir}/cacheinfo
%{_sbindir}/rcopenafs-client
%{_fillupdir}/sysconfig.openafs-client
%{vicecachedir}
%if %{have_firewalld}
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/services
%{_prefix}/lib/firewalld/services/afs3-callback.xml
%{_prefix}/lib/firewalld/services/afs3-rmtsys.xml
%endif

%files server 
%defattr(-,root,root)
%attr(770,root,root) %dir %{afslocaldir}
%attr(775,root,root) %dir %{afslogsdir}
%config %{viceetcdir}/server
%doc %{_mandir}/man5/AuthLog.5.gz
%doc %{_mandir}/man5/AuthLog.dir.5.gz
%doc %{_mandir}/man5/BackupLog.5.gz
%doc %{_mandir}/man5/BosConfig.5.gz
%doc %{_mandir}/man5/BosLog.5.gz
%doc %{_mandir}/man5/FORCESALVAGE.5.gz
%doc %{_mandir}/man5/FileLog.5.gz
%doc %{_mandir}/man5/KeyFile.5.gz
%doc %{_mandir}/man5/KeyFileExt.5.gz
%doc %{_mandir}/man5/NoAuth.5.gz
%doc %{_mandir}/man5/PtLog.5.gz
%doc %{_mandir}/man5/SALVAGE.fs.5.gz
%doc %{_mandir}/man5/SalvageLog.5.gz
%doc %{_mandir}/man5/UserList.5.gz
%doc %{_mandir}/man5/VLLog.5.gz
%doc %{_mandir}/man5/VolserLog.5.gz
%doc %{_mandir}/man5/afs_volume_header.5.gz
%doc %{_mandir}/man5/bdb.DB0.5.gz
%doc %{_mandir}/man5/krb.conf.5.gz
%doc %{_mandir}/man5/krb.excl.5.gz
%doc %{_mandir}/man5/prdb.DB0.5.gz
%doc %{_mandir}/man5/salvage.lock.5.gz
%doc %{_mandir}/man5/tapeconfig.5.gz
%doc %{_mandir}/man5/vldb.DB0.5.gz
%doc %{_mandir}/man8/akeyconvert.8.gz
%doc %{_mandir}/man8/asetkey.8.gz
%doc %{_mandir}/man8/bos_util.8.gz
%doc %{_mandir}/man8/bosserver.8.gz
%doc %{_mandir}/man8/buserver.8.gz
%doc %{_mandir}/man8/dafileserver.8.gz
%doc %{_mandir}/man8/dafssync-debug.8.gz
%doc %{_mandir}/man8/dafssync-debug_*.8.gz
%doc %{_mandir}/man8/dasalvager.8.gz
%doc %{_mandir}/man8/davolserver.8.gz
%doc %{_mandir}/man8/fileserver.8.gz
%doc %{_mandir}/man8/fssync-debug.8.gz
%doc %{_mandir}/man8/fssync-debug_*.8.gz
%doc %{_mandir}/man8/prdb_check.8.gz
%doc %{_mandir}/man8/pt_util.8.gz
%doc %{_mandir}/man8/ptserver.8.gz
%doc %{_mandir}/man8/salvager.8.gz
%doc %{_mandir}/man8/salvageserver.8.gz
%doc %{_mandir}/man8/state_analyzer.8.gz
%doc %{_mandir}/man8/upclient.8.gz
%doc %{_mandir}/man8/upserver.8.gz
%doc %{_mandir}/man8/vldb_check.8.gz
%doc %{_mandir}/man8/vldb_convert.8.gz
%doc %{_mandir}/man8/vlserver.8.gz
%doc %{_mandir}/man8/voldump.8.gz
%doc %{_mandir}/man8/volinfo.8.gz
%doc %{_mandir}/man8/volscan.8.gz
%doc %{_mandir}/man8/volserver.8.gz
%dir %{_libexecdir}/openafs
%{_libexecdir}/openafs/buserver
%{_libexecdir}/openafs/dafileserver
%{_libexecdir}/openafs/dasalvager
%{_libexecdir}/openafs/davolserver
%{_libexecdir}/openafs/fileserver
%{_libexecdir}/openafs/ptserver
%{_libexecdir}/openafs/salvager
%{_libexecdir}/openafs/salvageserver
%{_libexecdir}/openafs/upclient
%{_libexecdir}/openafs/upserver
%{_libexecdir}/openafs/vlserver
%{_libexecdir}/openafs/volserver
%{_sbindir}/asetkey
%{_sbindir}/akeyconvert
%{_sbindir}/bos_util
%{_sbindir}/bosserver
%{_sbindir}/dafssync-debug
%{_sbindir}/fssync-debug 
%{_sbindir}/prdb_check
%{_sbindir}/pt_util
%{_sbindir}/salvsync-debug 
%{_sbindir}/state_analyzer 
%{_sbindir}/vldb_check
%{_sbindir}/vldb_convert
%{_sbindir}/voldump
%{_sbindir}/volinfo
%{_sbindir}/volscan
%_unitdir/openafs-server.service
%{_sbindir}/rcopenafs-server
/%{_fillupdir}/sysconfig.openafs-server
%if %{have_firewalld}
%dir %{_prefix}/lib/firewalld
%dir %{_prefix}/lib/firewalld/services
%{_prefix}/lib/firewalld/services/afs3-bos.xml  
%{_prefix}/lib/firewalld/services/afs3-fileserver.xml
%{_prefix}/lib/firewalld/services/afs3-prserver.xml
%{_prefix}/lib/firewalld/services/afs3-update.xml
%{_prefix}/lib/firewalld/services/afs3-vlserver.xml
%{_prefix}/lib/firewalld/services/afs3-volser.xml
%endif

%files devel  
%defattr(-,root,root)
%dir %{_libdir}/openafs
%doc %{_mandir}/man1/livesys.1.gz
%doc %{_mandir}/man1/rxgen.1.gz
%doc %{_mandir}/man3/AFS::ukernel.3.gz
%{_bindir}/livesys
%{_bindir}/rxgen
%{_includedir}/openafs/
%{_libdir}/openafs/libafshcrypto.so
%{_libdir}/openafs/librokenafs.so
%{perl_vendorarch}/ukernel.so
%dir %{perl_vendorlib}/AFS
%{perl_vendorlib}/AFS/ukernel.pm

%if %{build_dkmspkg}
%files -n dkms-%{name}
%defattr(-,root,root)
/usr/src/%{name}-%{version}
%endif

%files  kernel-source 
%defattr(-,root,root)
%dir /usr/src/kernel-modules
%dir /usr/src/kernel-modules/openafs
/usr/src/kernel-modules/openafs/*

%if %{build_authlibs}
%files authlibs
%defattr(-,root,root)
%{_libdir}/openafs/libafsauthent.so.*
%{_libdir}/openafs/libafsrpc.so.*
%{_libdir}/openafs/libkopenafs.so.*

%files authlibs-devel
%defattr(-,root,root)
%{_libdir}/openafs/libafsauthent.so
%{_libdir}/openafs/libafsrpc.so
%{_libdir}/openafs/libkopenafs.so
%endif

%files client-compat
%defattr(-,root,root)
%{_prefix}/vice/etc
%{_prefix}/vice/cache
%dnl %{_libdir}/librokenafs.so.*
%dnl %{_libdir}/libafshcrypto.so.*

%files server-compat
%defattr(-,root,root)
%{_prefix}/afs/bin
%{_prefix}/afs/etc
%{_prefix}/afs/logs
%{_prefix}/afs/local
%{_prefix}/afs/db
%dnl %{_libdir}/librokenafs.so.*
%dnl %{_libdir}/libafshcrypto.so.*

%endif
#
#	CHANGELOG
#

%changelog
* Mon Nov 29 2021 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- re-add linux-kmp.patch. Required for 5.15
* Fri Oct  1 2021 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Fix %%ifarch for 32-bit arm
* Tue Aug  3 2021 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to openafs version 1.8.8
- remove linux-kmp.patch. Not required at the minute.
* Thu Apr 29 2021 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- add patches for kernel 5.12 to linux-kmp.patch
* Thu Mar  4 2021 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- add patches for kernel 5.11 to linux-kmp.patch
* Mon Feb 22 2021 Michael Meffie <mmeffie@sinenomine.net>
- fix building of perl module AFS::ukernel
* Mon Feb 22 2021 Matthias Gerstner <matthias.gerstner@suse.com>
- kernel-source.build-modules.sh: choose safe CWD while executing the build to
  prevent files being created in unsafe locations. Use new SUSE naming
  convention and rely on /etc/os-release, since /etc/SuSE-release no longer
  exists.
* Fri Feb  5 2021 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- use stock 1.8.7 from openafs.org
  * git-version might contain experimental code
  * add linux-kmp.patch for newer kernels
* Sat Jan 16 2021 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to HEAD of git branch openafs-stable-1_8_x
  * fix critical bug described in
    https://lists.openafs.org/pipermail/openafs-info/2021-January/043026.html
  * remove remove-get_ds-usage.patch
  * remove add_arch_to_linux_kernel_make.patch
* Mon Jan 11 2021 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- cleanup spec-file
  * do not include firewalld-stuff for SLE_12
  * use %%ifarch instead of %%if %%{_arch}
  * enable retpol line for TW x86_64 again
* Mon Nov  2 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to HEAD of git branch openafs-stable-1_8_x
* Mon Oct 12 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- add firewalld-configuration files
- enable loading of unsupported kernel-module on SLES15
* Mon Aug 17 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to HEAD of git branch openafs-stable-1_8_x
  * kernel 5.8 not supported by 1.8.6
    and no official package-upates out yet.
* Mon Aug 10 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- add patch remove-get_ds-usage.patch to fix building KMP on aarch64
* Wed Jul  1 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to official 1.8.6
  * remove patch 4c4bdde.diff
  * remove patch d3c7f75.diff
  * use source URLs again
* Tue Jun 16 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- remove fix_timeval_i586.patch
* Tue Jun 16 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- disable retpol line for TW x86_64. It does not compile.
* Mon Jun 15 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to HEAD of git branch openafs-stable-1_8_x.
  * 1.8.6pre3 is not out yet.
  * disable source URLs, none are present
- Fix build with GCC-10
  * add patch 4c4bdde.diff
  * add patch d3c7f75.diff
- create ld.so.conf-file dynamically
* Sat Apr 18 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to 1.8.6pre2
- disable fix_timeval_i586.patch
* Fri Apr 10 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to HEAD of git branch openafs-stable-1_8_x.
  * 1.8.6pre2 is not out yet.
  * disable source URLs, none are present
  * remove patch forward-to-1.8.6.pre1.patch
- fix build of i586 with fix_timeval_i586.patch
* Thu Apr  2 2020 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to pre-release 1.8.6pre1: forward-to-1.8.6.pre1.patch
* Wed Oct 23 2019 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to security-release 1.8.5, adresses:
  * OPENAFS-SA-2019-001: Skip server OUT args on error
  * OPENAFS-SA-2019-002: Zero all server RPC args
  * OPENAFS-SA-2019-003: ubik: Avoid unlocked ubik_currentTrans deref
* Thu Oct 10 2019 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to official version 1.8.4
- support Linux-kernel 5.3
- Avoid non-dir ENOENT errors in afs_lookup
- fix parsing of fileservers with -vlruthresh, etc.
- other bugfixes
* Thu Sep 26 2019 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to pre-release 1.8.4pre2
  * fix builds for Linux-kernels 5.3
* Sun Jul 28 2019 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- disable compilation with LTO, does not work yet.
* Tue Apr 30 2019 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to 1.8.3
- Require krb5-client for package openafs-client
- fix broken directory layout
- fix broken post-install script
- allow crypt to be set/unset on startup of client
- clean up source-filenames
* Mon Mar 25 2019 Jan Engelhardt <jengelh@inai.de>
- Use source URLs.
* Thu Mar 14 2019 Christof Hanke <christof.hanke@mpcdf.mpg.de>
- update to pre-release 1.8.3pre1
  * fix builds for Linux-kernels 4.20 and 5.0
  * other fixes, see RELNOTES-1.8.3pre1
  * remove obsolete Linux-4.20.patch
* Wed Jan 16 2019 christof.hanke@mpcdf.mpg.de
- Fix build for Lunux-4.20: Linux-4.20.patch
- use proper log-directory: dir_layout.patch
* Fri Sep 28 2018 Guillaume GARDET <guillaume.gardet@opensuse.org>
- Fix build for aarch64
* Wed Sep 12 2018 Jan Engelhardt <jengelh@inai.de>
- Quote "*.c", and avoid unnecessary pass through xargs.
* Wed Sep 12 2018 christof.hanke@mpcdf.mpg.de
- update to security-release 1.8.2
  * fix CVE-2018-16947 (OPENAFS-SA-2018-001)
  * fix CVE-2018-16948 (OPENAFS-SA-2018-002)
  * fix CVE-2018-16949 (OPENAFS-SA-2018-003)
* Wed Sep 12 2018 christof.hanke@mpcdf.mpg.de
- add retpoline support
* Sun Sep  9 2018 christof.hanke@mpcdf.mpg.de
- update to version 1.8.1.1
- Remove use_timespec64_for_kernel_4.18.patch. It is now integrated.
* Thu Aug 16 2018 christof.hanke@mpcdf.mpg.de
- Fix 32Bit build by adding
  commit 554176bd236d772d670df9bdd2496facd5a4209a as
  use_timespec64_for_kernel_4.18.patch
* Thu Aug 16 2018 christof.hanke@mpcdf.mpg.de
- Update to 1.8.1
- Remove backporting patches for AArch64 build:
  * add_support_fo_arm64_linux26.patch
  * dont_require_AFS_SYSCALL.patch
  * add_AFS_STRINGIZE_macro.patch
  * avoid_double_param_in_arm64_kernel.patch
* Wed Jun 27 2018 christof.hanke@mpcdf.mpg.de
- adjust building of KMP to new kernels (see boo 1098050)
  add patch add_arch_to_linux_kernel_make.patch for this
- add libtirpc-devel to BuildRequires:
- minor cleanups
* Fri May  4 2018 guillaume.gardet@opensuse.org
- Update to 1.8.0
- Fix AArch64 build by updating spec and backporting patches:
  * add_support_fo_arm64_linux26.patch
  * dont_require_AFS_SYSCALL.patch
  * add_AFS_STRINGIZE_macro.patch
  * avoid_double_param_in_arm64_kernel.patch
* Thu Apr 19 2018 christof.hanke@mpcdf.mpg.de
- remove package krb5-mit. It contained binaries for server and client.
  Besides, client and server already had an implicit dependency on krb5.
  Put the binaries to client and server-package respectively.
- Remove openafs-1.8.x.heimdal.patch and everything heimdal-related.
  SUSE does not provide a proper heimdal and it's untested for a long
  time.
* Mon Apr 16 2018 christof.hanke@mpcdf.mpg.de
- fdupes: use symlinks instead of hardlinks. Do not fdupe
  /etc and /var
* Fri Apr  6 2018 christof.hanke@mpcdf.mpg.de
- fix dependencies between packages, so that fuse-client
  can be installed.
- cleanup old sys-v sysconfig files and other minor fixes
- fix unit file for fuse-client
* Mon Apr  2 2018 christof.hanke@mpcdf.mpg.de
- build fuse-client unconditionally.
- do not build KMP on unsupported architectures so that overall
  build succeeds.
* Wed Mar 28 2018 christof.hanke@mpcdf.mpg.de
- rename binary backup to afs_backup.
  - rename man pages and prefix "backup" in content
- prefix "scout" by "afs_" in man-page
- remove unnecessary macro indirection %%ARCH
- replace hard-coded paths by macros
- make whitespace more consistent
- minor syntax and typo fixes
* Sun Mar 18 2018 jengelh@inai.de
- Replace old $RPM_* vars (most of them) by macros.
- Replace unnecessary macro indirections like %%bindir by %%_bindir.
* Thu Mar 15 2018 christof.hanke@mpcdf.mpg.de
- cleanup last cleanup: also remove rc.* files
* Tue Mar  6 2018 christof.hanke@mpcdf.mpg.de
- cleanup package for Factory:
  - rename package to openafs.
  - remove sys-v init stuff.
  - apply recommendations given in Request 581009
* Wed Feb 28 2018 christof.hanke@mpcdf.mpg.de
- add compat macro for new _fillupdir macro introduced in Nov 2017
* Wed Feb 28 2018 christof.hanke@mpcdf.mpg.de
- update to 1.8.0pre5
* Sun Jan  7 2018 christof.hanke@mpcdf.mpg.de
- update to 1.8.0pre4
- add patch for ncurses detection
* Thu Dec  7 2017 christof.hanke@mpcdf.mpg.de
- update to 1.8.0pre3
- add integrity check of tar-balls
* Fri Sep  1 2017 christof.hanke@mpcdf.mpg.de
- do not strip binaries on install
- fix %%postun server
* Fri Sep  1 2017 christof.hanke@mpcdf.mpg.de
- update to 1.8.0pre2
- use a preamble-file for KMP
- sort/cleanup/beautify spec-file
* Fri Sep  1 2017 christof.hanke@mpcdf.mpg.de
- spec-file:
  + use hardlinks for fdupes to provide correct header files in
    kernel-source
  + minor bugfixes, reorganization
- rename changes file to openafs18.changes
* Thu Feb  9 2017 christof.hanke@mpcdf.mpg.de
- rename package to openafs18-* so they don't override
  stable openafs-1.6 ones
- move ld.so to main package -- was in server-packages
* Tue Feb  7 2017 christof.hanke@mpcdf.mpg.de
- enable building of KMP
- make openafs-krb5-mit package dependend on openafs-client package
- add ld.so - config to main package
* Fri Jan 27 2017 christof.hanke@rzg.mpg.de
- remove pam, is not build on x86_64 and i596
* Mon Dec 26 2016 christof.hanke@rzg.mpg.de
- first version of 1.8
- remove docs package, put man pages in induvidual packets
- remove layout-patch, deal with this in spec file directly
* Sat Dec  3 2016 christof.hanke@rzg.mpg.de
- add new ChangeLog
* Thu Dec  1 2016 christof.hanke@rzg.mpg.de
- update to version 1.6.20
* Wed Nov 16 2016 christof.hanke@rzg.mpg.de
- add missing RemainAfterExit=true to client-systemd unit.
* Tue Nov 15 2016 christof.hanke@rzg.mpg.de
- update to version 1.6.19
* Tue Oct  4 2016 aj@suse.com
- Update README: Change SuSE to SUSE.
* Thu Jul 21 2016 christof.hanke@rzg.mpg.de
- update to version 1.6.18.2
* Fri Jun 24 2016 christof.hanke@rzg.mpg.de
- update to version 1.6.18.1
* Tue May 10 2016 christof.hanke@rzg.mpg.de
- update to version 1.6.18
* Thu Mar 17 2016 christof.hanke@rzg.mpg.de
- update to version 1.6.17
- cleanup
* Fri Dec 18 2015 christof.hanke@rzg.mpg.de
- update to version 1.6.16
- remove fix for configure for new ncurses, now dealt with in
  shipped package
* Sat Nov 21 2015 christof.hanke@rzg.mpg.de
- start using change.log again
- fix configure test for new ncurses
* Thu Jun 17 2010 cseader@novell.com
- update to version 1.4.12.1
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 23 2006 nadvornik@suse.cz
- fixed kernel module to compile
* Wed Jan 11 2006 mge@suse.de
- add openafs.SuidCells and openafs.CellServDB
- cleanup SPEC-file(s)
- finally adopt
  sysconfig.transarcmode.openafs-client
  rc.transarcmode.afs-server
  rc.transarcmode.afs-client
  to transarc mode; and fix a small typo in
  rc.defaultmode.afs-client
* Fri Jan  6 2006 mge@suse.de
- set "%%defattr(-,root,root)" for transarcmode-file-lists
- fix lib64 build problem in transarcmode
* Thu Jan  5 2006 mge@suse.de
- introduce transarc-mode and default-mode
- introduce "options"
* Thu Dec 29 2005 mge@suse.de
- build for SLES 9
- with heimdal krb5 support
- enable-largefile-fileserver
* Wed Dec 21 2005 nadvornik@suse.cz
- updated to 1.4.0
- fixed dangerous compiler warnings
* Mon Oct 31 2005 dmueller@suse.de
- don't build as root
* Fri Aug 26 2005 nadvornik@suse.cz
- fixed kernel module to build
- fixed sysconfig file name
* Thu Jul 14 2005 nadvornik@suse.cz
- updated to 1.3.85
- used LSB conforming init script names
* Tue Jul  5 2005 hare@suse.de
- Update for linux 2.6.13.
* Thu May 12 2005 nadvornik@suse.cz
- gcc4 fixes in kernel module
* Tue Apr 12 2005 nadvornik@suse.cz
- fixed to compile with gcc4
* Wed Feb 23 2005 nadvornik@suse.cz
- fixed memory leaks and 64bit fixes backported from 1.3.79
- updated README.SUSE
* Thu Feb  3 2005 nadvornik@suse.cz
- updated to 1.3.78
* Mon Jan 31 2005 nadvornik@suse.cz
- fixed afs.h to be usable from userspace [#50283]
* Tue Jan 25 2005 nadvornik@suse.cz
- updated to latest snapshot
* Wed Sep 15 2004 nadvornik@suse.cz
- added requres: kernel-nongpl [#45167]
- fixed kernel module oops [#44618]
* Wed Aug 11 2004 nadvornik@suse.cz
- use kernel module from openafs 1.3.70 to support kernel 2.6
* Mon Mar  8 2004 nadvornik@suse.cz
- updated to 1.2.11
- added note that client for kernel 2.6 is not available
* Tue Jan 20 2004 ro@suse.de
- added pam-devel to neededforbuild
* Fri Dec 12 2003 meissner@suse.de
- Added hack if no MTU came from userspace.
- Removed superflous ppc64 patch part.
* Thu Dec 11 2003 meissner@suse.de
- ppc64 port added (status: no longer crashes, talks to the network,
  but not successfully).
- Change headerfiles to make it possible to do a ppc -> ppc64 crosscompile.
* Mon Oct  6 2003 olh@suse.de
- build with -fPIC on ppc32
* Tue Sep 16 2003 nadvornik@suse.cz
- patch from cvs to use AllocLargeSpace for struct osi_file to prevent
  oopses with some kernel configurations
* Thu Sep 11 2003 nadvornik@suse.cz
- added option DYNROOT to sysconfig and enabled it by default [#27205]
* Wed Sep 10 2003 nadvornik@suse.cz
- added cleanup before module build [#29649]
* Tue Sep  9 2003 nadvornik@suse.cz
- fixed possible segfault
* Thu Sep  4 2003 nadvornik@suse.cz
- set permissions of /var/lib/openafs to 700
- README.SuSE fixes
* Thu Aug 28 2003 nadvornik@suse.cz
- use ghost for /afs, the directory is created by init-script
- fixed README.SuSE
* Thu Aug 21 2003 nadvornik@suse.cz
- moved all static libraries to /usr/lib/afs, fixes conflict with libdes
- used default value for THIS_CELL_SERVER_NAME
- removed old patches
* Tue Aug 12 2003 nadvornik@suse.cz
- fixed a bug in init script
* Mon Aug 11 2003 nadvornik@suse.cz
- updated to final 1.2.10
* Wed Jul 30 2003 nadvornik@suse.cz
- updated to 1.2.10-rc4
- do not destroy CellServDB even if REGENERATE_CELL_INFO=yes
- fixed to compile on x86_64
* Wed Jul 30 2003 sf@suse.de
-  use %%_lib where it was missing
* Wed Jul  9 2003 nadvornik@suse.cz
- fixed conflicts in filelist
* Fri Jun 20 2003 nadvornik@suse.cz
- improved init scripts
* Thu Jun 19 2003 nadvornik@suse.cz
- added README.SuSE
- fixed init scripts [#27426]
- installed man pages
* Thu Jun 12 2003 poeml@suse.de
- add /usr/src/kernel-modules to the file list
* Wed Jun  4 2003 schwab@suse.de
- Fix SMP configuration detection.
* Wed May 14 2003 poeml@suse.de
- rework filelists:
  - package/remove unpackaged files
  - move some files into the server & client subpackages
  - use %%defattr
- fix deprecated tail -1 syntax (fixes building the kernel module)
* Mon May 12 2003 nadvornik@suse.cz
- updated to 1.2.9
- added DATA_ENCRYPTION option to sysconfig
* Mon Mar 10 2003 poeml@suse.de
- x86_64: add -lresolv, -fPIC
- fix lib path on all 64 bit platforms
* Thu Mar  6 2003 nadvornik@suse.cz
- added sysconfig metadata
* Mon Feb 24 2003 nadvornik@suse.cz
- added dirs /afs, /etc/openafs, /var/lib/openafs to filelist
* Sun Feb 16 2003 olh@suse.de
- workaround broken -lresolv detection, lib64 fixes
* Wed Feb 12 2003 nadvornik@suse.cz
- fixed multiline strings in kernel module
* Fri Jan 24 2003 nadvornik@suse.cz
- updated to 1.2.8
- improved init script
* Fri Nov 29 2002 nadvornik@suse.cz
- included errno.h
- fixed multiline strings
* Fri Nov 22 2002 nadvornik@suse.cz
- first version of init scripts
* Wed Nov 20 2002 poeml@suse.de
- initial draft of a package. Lots of stuff missing, like init
  scripts, or the kerberos 5 migration toolkit.
