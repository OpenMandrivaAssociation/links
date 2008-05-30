%define version 2.1
%define rel 0.%pre.2
%define pre pre36

Summary:	Lynx-like text WWW browser
Name:		links
Version:	%{version}
Release:	%mkrel %rel
License:	GPLv2+
Group:		Networking/WWW

Source0:	http://atrey.karlin.mff.cuni.cz/~clock/twibright/links/download/%name-%version%pre.tar.bz2
Source4:	links.cfg
Patch1:		links-2.1pre18-no-flashy-white.patch
Patch3:		links-0.96-no-weird-unhx-ing-of-command-line-args.patch
Patch6:		cookies-save-0.96.patch
Patch7:		links-0.96-no-domain-security.patch
Patch8:		links-current-color-by-default--and-vt100-frames.patch
Patch10:	links-2.0pre1-be-graphic-when-called-_links-graphic_.patch
Patch11:	links-2.0pre1-convert-old-bookmarks-in-new-format.patch
Patch12:	links-2.1pre31-gz.patch
Patch14:	links-2.1pre17-automake.patch
Patch21:	links-2.1pre17-fix-segfault-on-loading-cookies.patch
Patch22:	links-2.1pre2-64bit-fixes.patch
Patch23:	links-2.1pre31-dont-have-two-assocations-with-same-label--otherwise-one-cant-override-shared-config.patch
Patch24:	links-2.1pre18-CVE-2006-5925--disable-SMB.patch

URL:		http://links.twibright.com/
BuildRequires:	X11-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	ncurses-devel => 5.0
BuildRequires:	openssl-devel
BuildRequires:	directfb-devel >= 0.9.17
BuildRequires:	automake1.9
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
%setup  -q -n %name-%version%pre
%patch1 -p1
%patch3 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1 -b .gzip
%patch14 -p1 -b .automake18
%patch21 -p1
%patch22 -p1 -b .64bit-fixes
%patch23 -p1
%patch24 -p1

#rm -f missing
#ln -s /usr/share/automake-1.4/missing missing

autoreconf --force --install

%build
%configure2_5x --enable-javascript
(cd Unicode ; LC_ALL=C ./gen )
%make

cp -f links links-text

# Needed to fix linkage problem
#rm -f bfu.o dip.o lru.o x.o framebuffer.o terminal.o kbd.o links_icon.o
make clean
%configure2_5x --enable-graphics --enable-javascript
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
%{update_menus}

update-alternatives --install /usr/bin/links links /usr/bin/links-graphic 20

%postun graphic
%{clean_menus}

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
%doc AUTHORS BUGS ChangeLog README SITES TODO 
%config(noreplace) /etc/links.cfg
%{_mandir}/*/*


