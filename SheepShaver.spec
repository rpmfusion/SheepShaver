%global commit e273bb1a0b4f6e35bcdbf6cf918aa0ca3e6d99da
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%define date 20171001

# Hardening breaks the jit
%undefine _hardened_build

Summary:        Power Macintosh emulator
Name:           SheepShaver
Version:        2.4
Release:        0.17.%{date}%{?dist}
License:        GPLv2+
URL:            http://sheepshaver.cebix.net/
Source0:        https://github.com/cebix/macemu/archive/%{commit}/BasiliskII-1.0-%{shortcommit}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}.png
Source3:        %{name}.appdata.xml
Patch1:         macemu-gcc10.patch
# Patch 10+ because these are for cxmon
Patch10:        cxmon-3.2-hide-symbols.patch
Patch11:        cxmon-3.2-strfmt.patch
Patch12:        cxmon-3.2-fpermissive.patch
BuildRequires:  libtool gcc-c++ gtk2-devel
BuildRequires:  desktop-file-utils libappstream-glib readline-devel
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
%autosetup -p1 -n macemu-%{commit}
sed -i 's/\r//' %{name}/src/Unix/tinyxml2.cpp
chmod -x %{name}/src/Unix/tinyxml2.cpp %{name}/src/Unix/tinyxml2.h
chmod -x %{name}/src/kpx_cpu/src/mathlib/ieeefp.hpp
# autogen
pushd %{name}/src/Unix
NO_CONFIGURE=1 ./autogen.sh
popd


%build
pushd %{name}/src/Unix
mkdir obj
%configure --datadir=%{_sysconfdir} --enable-ppc-emulator=yes \
    --disable-xf86-dga --enable-sdl-audio --with-bincue
# autoconf 2.71 says The preprocessor macro `STDC_HEADERS' is obsolete
# in AC_HEADER_STDC
# For now, explicitly add STDC_HEADERS to config.h
sed -i config.h -e '\@undef.*STDC_HEADERS@s|^.*$|#define STDC_HEADERS 1|'

DYNGEN_CFLAGS="$(echo $RPM_OPT_FLAGS | sed s/-fstack-protector-strong//)"
make %{?_smp_mflags} \
    DYNGEN_CFLAGS="$DYNGEN_CFLAGS" DYNGEN_CXXFLAGS="$DYNGEN_CFLAGS"
popd


%install
pushd %{name}/src/Unix
%make_install
popd
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tunconfig

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}

install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

install -D -p -m 0644 %{SOURCE3} \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml


%files
%doc %{name}/NEWS %{name}/doc/Linux/*
%license %{name}/COPYING
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/keycodes
%{_sysconfdir}/%{name}/tunconfig
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_mandir}/man1/%{name}.1*


%changelog
* Sat Aug 06 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4-0.17.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Apr 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.4-0.16.20171001
- Fix build with autoconf 2.71

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4-0.15.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-0.14.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Feb 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-0.13.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-0.12.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 10 2020 Hans de Goede <j.w.r.degoede@gmail.com> - 2.4-0.11.20171001
- Fix FTBFS

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-0.10.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-0.9.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-0.8.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-0.7.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.4-0.6.20171001
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct  1 2017 Hans de Goede <j.w.r.degoede@gmail.com> - 2.4-0.5.20171001
- Sync version with BasiliskII package / latest upstream

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.4-0.4.20160322
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.4-0.3.20160322
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul  7 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 2.4-0.2.20160322
- Sync version with BasiliskII package / latest upstream
- New version comes with bundled cxmon
- Fix FTBFS
- Use proper github download URL
- Add appdata

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

