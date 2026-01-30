#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		lokalize
Summary:	Lokalize - computer-aided translation system
Summary(pl.UTF-8):	Lokalize - system komputerowo wspomaganego tłumaczenia
Name:		ka6-%{kaname}
Version:	25.12.1
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	50bbafe64d3f3860b0623403882e0729
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Sql-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	hunspell-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kf6-sonnet-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lokalize is a computer-aided translation system that focuses on
productivity and quality assurance. It is targeted for software
translation and also integrates external conversion tools for
freelance office document translation.

Features:
- Project management overview
- Translation merging (synchronization)
- Translation memory
- Glossary
- Spell-checking

%description -l pl.UTF-8
Lokalize to system komputerowo wspomaganego tłumaczenia, skupiający
się na produktywności i zapewnieniu jakości. Głównym zastosowaniem
jest tłumaczenie oprogramowania; zawiera także narzędzia do
zewnętrznej konwersji do tłumaczenia dokumentów biurowych.

Możliwości:
- widok ogólny zarządzania projektem
- łączenie tłumaczeń (synchronizacja)
- pamięć tłumaczeń
- słownik pojęć
- sprawdzanie pisowni

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lokalize
%{_desktopdir}/org.kde.lokalize.desktop
%{_datadir}/config.kcfg/lokalize.kcfg
%{_iconsdir}/hicolor/*x*/apps/lokalize.png
%{_iconsdir}/hicolor/scalable/apps/lokalize.svgz
%{_datadir}/knotifications6/lokalize.notifyrc
%{_datadir}/lokalize
%{_datadir}/metainfo/org.kde.lokalize.appdata.xml
%{_datadir}/qlogging-categories6/lokalize.categories
