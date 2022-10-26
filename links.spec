Summary:	Lynx-like text WWW browser
Name:		links
Version:	2.28
Release:	1
License:	GPLv2+
Group:		Networking/WWW
Url:		http://links.twibright.com/
Source0:	http://links.twibright.com/download/links-%{version}.tar.bz2
Source4:	links.cfg
Patch3:		links-0.96-no-weird-unhx-ing-of-command-line-args.patch
Patch14:	links-2.8-automake.patch
BuildRequires:	bzip2-devel
BuildRequires:	gpm-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(directfb)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
Provides:	webclient
Requires:	links-common = %{EVRD}

%description
Links is a text based WWW browser, at first look similar to Lynx, but
somehow different:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- partially handle Javascript

%files
%{_bindir}/links-text

%post
update-alternatives --install /usr/bin/links links /usr/bin/links-text 10

%postun
if [ "$1" = "0" ]; then
  update-alternatives --remove links /usr/bin/links-text
fi

%triggerpostun -- links
if [ ! -e /usr/bin/links ]; then
  update-alternatives --auto links
fi

#----------------------------------------------------------------------------

%package graphic
Summary:	Lynx-like text/X11 WWW browser
Group:		Networking/WWW
Requires:	links-common = %{EVRD}
Provides:	webclient
Requires:	indexhtml

%description graphic
Links is a text/X11 based WWW browser, at first look similar to Lynx, but
somehow different:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- partially handle Javascript

%files graphic
%{_bindir}/links-graphic
%{_datadir}/applications/*

%post graphic
update-alternatives --install /usr/bin/links links /usr/bin/links-graphic 20

%postun graphic
if [ "$1" = "0" ]; then
  update-alternatives --remove links /usr/bin/links-graphic
fi

%triggerpostun graphic -- links
if [ ! -e /usr/bin/links ]; then
  update-alternatives --auto links
fi

#----------------------------------------------------------------------------

%package common
Summary:	Lynx-like text/X11 WWW browser
Group:		Networking/WWW
Requires:	links-common = %{EVRD}

%description common
Common files for links and links-graphic.

%files common
%doc AUTHORS ChangeLog README SITES
%config(noreplace) /etc/links.cfg
%{_mandir}/*/*

#----------------------------------------------------------------------------

%prep
%autosetup -p1
autoreconf -fi
%configure

%build
%make_build

cp -f links links-text

make clean
%configure --enable-graphics
%make_build

cp -f links links-graphic

%install
%make_install

rm -f %{buildroot}%{_bindir}/links
install links-graphic links-text %{buildroot}%{_bindir}

install -D -m 644 %{SOURCE4} %{buildroot}/etc/links.cfg

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Links
Comment=Lynx-like text/graphic Web browser
Exec=/usr/bin/links-graphic /usr/share/mdk/indexhtml/index.html
Icon=web_browser_section
Terminal=false
Type=Application
Categories=Network;WebBrowser;
EOF
