%define date 20060514
%define mon_version 3.2
%define desktop_vendor rpmforge

Summary: Power Macintosh emulator
Name: SheepShaver
Version: 2.3
Release: 0.11.%{date}%{?dist}
License: GPLv2+
Group: Applications/Emulators
URL: http://www.gibix.net/projects/sheepshaver/
Source0: http://www.gibix.net/projects/sheepshaver/files/SheepShaver-%{version}-0.%{date}.1.tar.bz2
Source1: http://cxmon.cebix.net/downloads/cxmon-%{mon_version}.tar.gz
Source2: SheepShaver.png
Patch0: SheepShaver-2.2-nostrip.patch
Patch1: SheepShaver-2.3-gcc43.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++, gtk2-devel, esound-devel >= 0.2.8
BuildRequires: desktop-file-utils, readline-devel
%{?_with_sdl:BuildRequires: SDL-devel}
BuildRequires: libXt-devel, libXxf86dga-devel, libXxf86vm-devel
# Other archs need an instruction skipper on well-known invalid
# memory references (e.g. illegal writes to ROM).
ExclusiveArch: i586 ppc x86_64

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
%setup -q -a 1
%patch0 -p1 -b .nostrip
%patch1 -p1 -b .gcc43


%build
pushd src/Unix
%configure \
    --datadir=%{_sysconfdir} --enable-ppc-emulator=yes \
    %{!?_without_mon: --with-mon=../../cxmon-%{mon_version}/src} \
    %{?_with_sdl: --enable-sdl-video --enable-sdl-audio}
%{__mkdir} obj
%{__make} %{?_smp_mflags}
popd


%install
%{__rm} -rf %{buildroot}
%makeinstall -C src/Unix \
    datadir="%{buildroot}%{_sysconfdir}"
chmod +x %{buildroot}%{_sysconfdir}/%{name}/tunconfig

# Create the system menu entry
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Sheep Shaver
Comment=Power Macintosh Emulator
Exec=SheepShaver
Icon=SheepShaver.png
Terminal=false
Type=Application
Categories=Game;Emulator;
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
%config(noreplace) %{_sysconfdir}/SheepShaver/keycodes
%{_sysconfdir}/SheepShaver/tunconfig
%{_bindir}/SheepShaver
%{_datadir}/pixmaps/SheepShaver.png
%{_datadir}/applications/%{desktop_vendor}-%{name}.desktop
%{_mandir}/man1/SheepShaver.1*


%changelog
* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3-0.11.20060514
- Mass rebuilt for Fedora 19 Features

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3-0.10.20060514
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3-0.9.20060514
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Apr 12 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.3-0.8.20060514
- s/i386/i586/ in ExclusiveArch for F11

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.3-0.7.20060514
- rebuild for new F11 features

* Sun Oct 19 2008 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.3-0.6.20060514
- Use ppc cpu emulator even when running on ppc, as using the native cpu
  requires a private implementation of pthreads from:
  src/Unix/Linux/sheepthreads.c
  which depends on glibc pthread internals which are no longer exposed by
  glibc and quite possibly changed

* Sat Oct 18 2008 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.3-0.5.20060514
- Updated release of cxmon to 3.2
- Fix compilation with gcc-4.3 (tricky, esp. on x86_64)
- Regenerate Patch0, nuke _default_patch_fuzz 2
- Fixup desktop file Categories, so that we show up under the Emulators menu
- Make rpmlint like this package
- Add missing libXxf86dga-devel, libXxf86vm-devel BuildRequires

* Sat Oct 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.3-0.4.20060514
- rebuild for RPM Fusion
- define _default_patch_fuzz 2
- ExclusiveArch: i386 instead of ix86 to prevent plague building this for 
  athlon and other ix86 archs
- always build for x.org

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

