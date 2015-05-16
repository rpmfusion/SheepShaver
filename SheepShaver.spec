%define date 20150516
%define mon_version 3.2

Summary:        Power Macintosh emulator
Name:           SheepShaver
Version:        2.4
Release:        0.1.%{date}%{?dist}
License:        GPLv2+
URL:            http://sheepshaver.cebix.net/
# GRRR github, no url ...
Source0:        macemu-master.zip
Source1:        cxmon-3.2-cvs20130310.tar.gz
Source2:        SheepShaver.png
# Patch 10+ because this is for Source1 rather then Source0
Patch10:        cxmon-3.2-hide-symbols.patch
Patch11:        cxmon-3.2-strfmt.patch
BuildRequires:  libtool gcc-c++ gtk2-devel
BuildRequires:  desktop-file-utils readline-devel
BuildRequires:  libXt-devel libXxf86vm-devel SDL-devel
Requires:       hicolor-icon-theme
# Other archs need an instruction skipper on well-known invalid
# memory references (e.g. illegal writes to ROM).
ExclusiveArch:  i686 x86_64 ppc

%description
SheepShaver is a MacOS run-time environment that allows you to run classic
MacOS applications. This means that both Linux and MacOS applications can
run at the same time (usually in a window on the Linux desktop).

If you are using a PowerPC-based system, applications will run at native
speed (i.e. with no emulation involved). There is also a built-in PowerPC
G4 emulator, without MMU support, for non-PowerPC systems.


%prep
%setup -q -a 1 -n macemu-master
pushd cxmon-%{mon_version}
%patch10 -p1
%patch11 -p1
popd
chmod -x SheepShaver/src/kpx_cpu/src/mathlib/ieeefp.hpp


%build
pushd SheepShaver/src/Unix
NO_CONFIGURE=1 ./autogen.sh
export CXXFLAGS="$RPM_OPT_FLAGS -fpermissive"
%configure --datadir=%{_sysconfdir} --enable-ppc-emulator=yes \
    --with-mon=../../../cxmon-%{mon_version}/src \
    --disable-xf86-dga --enable-sdl-audio --with-bincue
DYNGEN_CFLAGS="$(echo $RPM_OPT_FLAGS | sed s/-fstack-protector-strong//)"
make %{?_smp_mflags} \
    DYNGEN_CFLAGS="$DYNGEN_CFLAGS" DYNGEN_CXXFLAGS="$DYNGEN_CFLAGS"
popd


%install
pushd SheepShaver/src/Unix
make install DESTDIR=$RPM_BUILD_ROOT
popd
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tunconfig

# Create the system menu entry
%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Sheep Shaver
Comment=Power Macintosh Emulator
Exec=SheepShaver
Icon=SheepShaver
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
%if 0%{?fedora} && 0%{?fedora} < 19
    --vendor rpmforge \
%endif
    %{name}.desktop

install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/SheepShaver.png


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc SheepShaver/COPYING SheepShaver/NEWS SheepShaver/doc/Linux/*
%dir %{_sysconfdir}/SheepShaver/
%config(noreplace) %{_sysconfdir}/SheepShaver/keycodes
%{_sysconfdir}/SheepShaver/tunconfig
%{_bindir}/SheepShaver
%{_datadir}/icons/hicolor/32x32/apps/SheepShaver.png
%{_datadir}/applications/*%{name}.desktop
%{_mandir}/man1/SheepShaver.1*


%changelog
* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 2.4-0.1.20150516
- SheepShaver 2.4 git snapshot du-jour
- Fix FTBFS (rf#3634)

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 2.3-0.13.20130310
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 10 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 2.3-0.12.20130310
- New upstream: http://sheepsaver.cebix.net/
- Uses github, no source tarbals :| Update to todays git master (bbc0af47)
- Modernize spec
- Fix FTBFS (since F-11 !)
- Switch from esound (deprecated / obsolete) to SDL for sound output

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

* Thu Apr 21 2005 Matthias Saou <http://freshrpms.net/> 2.2-0.20050315
- Spec file cleanup, based on the .src.rpm from the SheepShaver website.
- Make cxmon support optionnal with --without mon.
- Add menu entry.
- Disable binary stripping on make install to get a useful debuginfo package.

