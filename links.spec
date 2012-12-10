%define version 2.6
%define rel 1

Summary:	Lynx-like text WWW browser
Name:		links
Version:	%{version}
Release:	%mkrel %rel
License:	GPLv2+
Group:		Networking/WWW

Source0:	http://atrey.karlin.mff.cuni.cz/~clock/twibright/links/download/%name-%version.tar.bz2
Source4:	links.cfg
Patch3:		links-0.96-no-weird-unhx-ing-of-command-line-args.patch
Patch6:		cookies-save-0.96.patch
Patch21:	links-2.1pre17-fix-segfault-on-loading-cookies.patch
Patch22:	links-2.1pre2-64bit-fixes.patch
Patch23:	links-2.1pre31-dont-have-two-assocations-with-same-label--otherwise-one-cant-override-shared-config.patch

URL:		http://links.twibright.com/
BuildRequires:	libx11-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	openssl-devel
BuildRequires:	jpeg-devel
BuildRequires:	bzip2-devel
BuildRequires:	gpm-devel
BuildRequires:	zlib-devel
BuildRequires:	svgalib-devel
BuildRequires:	directfb-devel >= 0.9.17
Provides:	webclient
Requires:	links-common = %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Links is a text based WWW browser, at first look similar to Lynx, but
somehow different:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- partially handle Javascript

%package graphic
Summary:	Lynx-like text/X11 WWW browser
Group:		Networking/WWW
Requires:	links-common = %{version}
Provides:	webclient, links = %{version}-%{release}
Requires:	indexhtml

%description graphic
Links is a text/X11 based WWW browser, at first look similar to Lynx, but
somehow different:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- partially handle Javascript

%package common
Summary:	Lynx-like text/X11 WWW browser
Group:		Networking/WWW
Requires:	links-common = %{version}
Conflicts:	links < 2.1-0.pre18.5mdk, links-graphic < 2.1-0.pre18.5mdk

%description common
Common files for links and links-graphic

%prep
%setup  -q -n %name-%version
%patch3 -p1
%patch6 -p1
%patch21 -p1
%patch22 -p1 -b .64bit-fixes
%patch23 -p1

%build
# error: conditional "am__fastdepCXX" was never defined (for eautoreconf)
# Upstream configure produced by broken autoconf-2.13. This also fixes
# toolchain detection.
sed -i -e '/AC_PROG_CXX/s:#::' configure.in || die
autoreconf -fi
%configure2_5x
(cd Unicode ; LC_ALL=C ./gen )
%make

cp -f links links-text

# Needed to fix linkage problem
#rm -f bfu.o dip.o lru.o x.o framebuffer.o terminal.o kbd.o links_icon.o
make clean
%configure2_5x --enable-graphics
%make

cp -f links links-graphic

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

rm -f %buildroot%{_bindir}/links
install links-graphic links-text %buildroot%{_bindir}

install -D -m 644 %SOURCE4 %buildroot/etc/links.cfg

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Links
Comment=Lynx-like text/graphic Web browser
Exec=/usr/bin/links-graphic /usr/share/doc/HTML/index.html
Icon=web_browser_section
Terminal=false
Type=Application
Categories=Network;WebBrowser;
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- links
if [ ! -e /usr/bin/links ]; then
  update-alternatives --auto links
fi

%triggerpostun graphic -- links
if [ ! -e /usr/bin/links ]; then
  update-alternatives --auto links
fi

%post
update-alternatives --install /usr/bin/links links /usr/bin/links-text 10

%postun
if [ "$1" = "0" ]; then
  update-alternatives --remove links /usr/bin/links-text
fi

%post graphic
%if %mdkversion < 200900
%{update_menus}
%endif

update-alternatives --install /usr/bin/links links /usr/bin/links-graphic 20

%postun graphic
%if %mdkversion < 200900
%{clean_menus}
%endif

if [ "$1" = "0" ]; then
  update-alternatives --remove links /usr/bin/links-graphic
fi

%files 
%defattr(-,root,root)
%{_bindir}/links-text

%files graphic
%defattr(-,root,root)
%{_bindir}/links-graphic
%{_datadir}/applications/*

%files common
%defattr(-,root,root)
%doc AUTHORS ChangeLog README SITES
%config(noreplace) /etc/links.cfg
%{_mandir}/*/*




%changelog
* Tue Apr 17 2012 Alexander Khrukin <akhrukin@mandriva.org> 2.6-1
+ Revision: 791411
- version update 2.6

* Fri Dec 17 2010 Funda Wang <fwang@mandriva.org> 2.2-8mdv2011.0
+ Revision: 622592
- update BRs

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.1 packages

* Thu Apr 08 2010 Rémy Clouard <shikamaru@mandriva.org> 2.2-7mdv2010.1
+ Revision: 533227
- Rebuild for new openssl

* Wed Jan 13 2010 Götz Waschk <waschk@mandriva.org> 2.2-6mdv2010.1
+ Revision: 490513
- rebuild for new libjpeg

* Sun Nov 08 2009 Funda Wang <fwang@mandriva.org> 2.2-5mdv2010.1
+ Revision: 462916
- rebuild for new dfb

* Mon Aug 17 2009 Götz Waschk <waschk@mandriva.org> 2.2-4mdv2010.0
+ Revision: 417289
- rediff patches 10,11

* Sun Aug 17 2008 Funda Wang <fwang@mandriva.org> 2.2-3mdv2009.0
+ Revision: 272981
- rebuild for new dfb

* Sun Aug 03 2008 Funda Wang <fwang@mandriva.org> 2.2-2mdv2009.0
+ Revision: 261917
- New version 2.2

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri May 30 2008 Funda Wang <fwang@mandriva.org> 2.1-0.pre36.2mdv2009.0
+ Revision: 213230
- rebuild for new directfb

* Thu May 15 2008 Funda Wang <fwang@mandriva.org> 2.1-0.pre36.1mdv2009.0
+ Revision: 207634
- New version 2.1pre36

* Tue May 06 2008 Funda Wang <fwang@mandriva.org> 2.1-0.pre35.1mdv2009.0
+ Revision: 201766
- New version 2.1pre35

* Mon May 05 2008 Funda Wang <fwang@mandriva.org> 2.1-0.pre34.1mdv2009.0
+ Revision: 201377
- New version 2.1pre34

  + Thierry Vignaud <tv@mandriva.org>
    - fix URL
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Dec 09 2007 Funda Wang <fwang@mandriva.org> 2.1-0.pre31.1mdv2008.1
+ Revision: 116673
- New version 2.1pre31
- Rediff patch12,23

* Sun Dec 09 2007 Funda Wang <fwang@mandriva.org> 2.1-0.pre18.15mdv2008.1
+ Revision: 116669
- fix menu entry

  + Thierry Vignaud <tv@mandriva.org>
    - buildrequires X11-devel instead of XFree86-devel
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Pixel <pixel@mandriva.com>
    - really apply security fix for CVE-2006-5925
    - fix build
    - fix icon (#25644)


* Tue Nov 21 2006 Pixel <pixel@mandriva.com> 2.1-0.pre18.14mdv2007.0
+ Revision: 85722
- security fix for CVE-2006-5925 (patch24, disable SMB)
- Import links

* Sat Jul 08 2006 Pixel <pixel@mandriva.com> 2.1-0.pre18.13mdv2007.0
- switch to XDG menu

* Fri May 12 2006 Götz Waschk <waschk@mandriva.org> 2.1-0.pre18.12mdk
- rebuild for new directfb

* Sat Apr 01 2006 Pixel <pixel@mandriva.com> 2.1-0.pre18.11mdk
- links-graphic do not obsolete links anymore
  (no good reason for it and breaks distro scripts)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.1-0.pre18.10mdk
- rebuilt against openssl-0.9.8a

* Thu Nov 03 2005 Götz Waschk <waschk@mandriva.org> 2.1-0.pre18.9mdk
- rebuild for new directfb

* Tue Oct 11 2005 Pixel <pixel@mandriva.com> 2.1-0.pre18.8mdk
- really better fix for previous patch (ie fix memory leaks)

* Sat Oct 08 2005 Pixel <pixel@mandriva.com> 2.1-0.pre18.7mdk
- better fix for previous patch

* Sat Oct 08 2005 Pixel <pixel@mandriva.com> 2.1-0.pre18.6mdk
- don't have two assocations with same label, otherwise one can't override shared config

* Sat Aug 27 2005 Pixel <pixel@mandriva.com> 2.1-0.pre18.5mdk
- reverting previous changes, introduce links-common instead
- move the conflicts on links to links-common

* Tue Aug 23 2005 Pixel <pixel@mandriva.com> 2.1-0.pre18.4mdk
- links-graphic now depends on links 
  => no way to have links-graphic without links-text
  => this fixes upgrade conflicts and is cleaner
  (the other solution would be to create a links-common for links.cfg and the manpage)

* Fri Aug 19 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.1-0.pre18.3mdk
- add BuildRequires: automake1.9

* Wed Aug 10 2005 Abel Cheung <deaddog@mandriva.org> 2.1-0.pre18.2mdk
- Reenable Patch1 (changes link color from bright white to other color),
  which I accidentally disabled

* Tue Aug 09 2005 Abel Cheung <deaddog@mandriva.org> 2.1-0.pre18.1mdk
- 2.1pre18
- Build with directfb support
- Rediff patch12, 21
- Patch14: Newer automake can't accept conditional macros definition

* Mon Mar 07 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.1-0.pre15.2mdk
- add BuildRequires: automake1.4

* Tue Dec 14 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.1-0.pre15.1mdk
- new release
- fix URL
- Adapt patch #8 to new code

* Sat Aug 14 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 2.1-0.pre13.3mdk
- Fix menu

* Wed Feb 18 2004 David Baudens <baudens@mandrakesoft.com> 2.1-0.pre13.2mdk
- Fix menu

