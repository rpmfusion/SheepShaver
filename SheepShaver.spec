# $Id: SheepShaver.spec,v 1.1 2008/10/18 14:04:25 thl Exp $
# Authority: matthias

%{?dist: %{expand: %%define %dist 1}}
%{?fedora: %{expand: %%define fc%{fedora} 1}}

%{!?dist:%define _with_modxorg 1}
%{?el5:  %define _with_modxorg 1}
%{?fc7:  %define _with_modxorg 1}
%{?fc6:  %define _with_modxorg 1}
%{?fc5:  %define _with_modxorg 1}

%define date 20060514
%define mon_version 3.1
%define desktop_vendor rpmforge

Summary: Power Macintosh emulator
Name: SheepShaver
Version: 2.3
Release: 0.4.%{date}.fc7
License: GPL
Group: Applications/Emulators
URL: http://www.gibix.net/projects/sheepshaver/
Source0: http://www.gibix.net/projects/sheepshaver/files/SheepShaver-%{version}-0.%{date}.1.tar.bz2
Source1: http://wwwthep.physik.uni-mainz.de/~cbauer/cxmon-%{mon_version}.tar.gz
Source2: SheepShaver.png
Patch0: SheepShaver-2.2-nostrip.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++, gtk2-devel, esound-devel >= 0.2.8
BuildRequires: desktop-file-utils, readline-devel
%{?_with_sdl:BuildRequires: SDL-devel}
%{?_with_modxorg:BuildRequires: libXt-devel}
#BuildRequires: SDL-devel
# Other archs need an instruction skipper on well-known invalid
# memory references (e.g. illegal writes to ROM).
ExclusiveArch: %{ix86} ppc x86_64

%description
SheepShaver is a MacOS run-time environment that allows you to run classic
MacOS applications. This means that both Linux and MacOS applications can
run at the same time (usually in a window on the Linux desktop).

If you are using a PowerPC-based system, applications will run at native
speed (i.e. with no emulation involved). There is also a built-in PowerPC
G4 emulator, without MMU support, for non-PowerPC systems.

Available rebuild options :
--without : mon
--with    : sdl


%prep
%setup -a 1
%patch0 -p1 -b .nostrip


%build
pushd src/Unix
%configure \
    --datadir=%{_sysconfdir} \
    %{!?_without_mon: --with-mon=../../cxmon-%{mon_version}/src} \
    %{?_with_sdl: --enable-sdl-video --enable-sdl-audio}
    %{__make} %{?_smp_mflags}
popd


%install
%{__rm} -rf %{buildroot}
%makeinstall -C src/Unix \
    datadir="%{buildroot}%{_sysconfdir}"

# Create the system menu entry
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Sheep Shaver
Comment=Power Macintosh Emulator
Exec=SheepShaver
Icon=SheepShaver.png
Terminal=false
Type=Application
Categories=Application;Utility;
Encoding=UTF-8
EOF

%{__mkdir_p} %{buildroot}%{_datadir}/applications
desktop-file-install --vendor %{desktop_vendor} \
    --dir %{buildroot}%{_datadir}/applications \
    %{name}.desktop

%{__install} -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/pixmaps/SheepShaver.png


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc COPYING NEWS doc/Linux/*
%dir %{_sysconfdir}/SheepShaver/
%config %{_sysconfdir}/SheepShaver/keycodes
%config %{_sysconfdir}/SheepShaver/tunconfig
%{_bindir}/SheepShaver
%{_datadir}/pixmaps/SheepShaver.png
%{_datadir}/applications/%{desktop_vendor}-%{name}.desktop
%{_mandir}/man1/SheepShaver.1*


%changelog
* Sat Oct 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.3-0.4.20060514.fc7
- rebuild for RPM Fusion

* Sun Jun 25 2006 Matthias Saou <http://freshrpms.net/> 2.3-0.3.20060514
- Update to 2.3-0.20060514.1.
- Remove no longer needed stats patch.

* Fri Jan 13 2006 Matthias Saou <http://freshrpms.net/> 2.3-0.2.20051130
- Add modular xorg build conditional.

* Thu Dec  1 2005 Matthias Saou <http://freshrpms.net/> 2.3-0.1.20051130
- Update to 2.3 20051130 snapshot.
- Update URLs to gibix.net.
- Drop no longer relevant misc patch (NET_IF_SHEEPNET change).
- Add --with sdl rebuild option.
- Switch from gtk1 to new gtk2 GUI.

* Sat Apr 21 2005 Matthias Saou <http://freshrpms.net/> 2.2-0.20050315
- Spec file cleanup, based on the .src.rpm from the SheepShaver website.
- Make cxmon support optionnal with --without mon.
- Add menu entry.
- Disable binary stripping on make install to get a useful debuginfo package.

