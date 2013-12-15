#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	mtl
Summary:	A Haskell binding to the mtl graphics library
Summary(pl.UTF-8):	Wiązanie Haskella do biblioteki graficznej mtl
Name:		ghc-%{pkgname}
Version:	2.1.2
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/mtl
Source0:	http://hackage.haskell.org/package/mtl-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	943c110524d96126bfa0e61f7df1ebcd
URL:		http://hackage.haskell.org/package/mtl
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base < 6
BuildRequires:	ghc-transformers >= 0.3
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof < 6
BuildRequires:	ghc-transformers-prof >= 0.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base < 6
Requires:	ghc-transformers >= 0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Monad classes using functional dependencies, with instances for
various monad transformers, inspired by the paper "Functional
Programming with Overloading and Higher-Order Polymorphism", by Mark P
Jones, in "Advanced School of Functional Programming", 1995
(<http://web.cecs.pdx.edu/~mpj/pubs/springschool.html>).

%description -l pl.UTF-8
Klasy monad wykorzystujące zależności funkcyjne z instancjami dla
różnych przekształceń monad, zainspirowane dokumentem "Functional
Programming with Overloading and Higher-Order Polymorphism" autorstwa
Marka P. Jonesa, opublikowanym w "Advanced School of Functional
Programming", 1995
(<http://web.cecs.pdx.edu/~mpj/pubs/springschool.html>).

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof < 6
Requires:	ghc-transformers-prof >= 0.3

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSmtl-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSmtl-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Cont
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Cont/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Error
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Error/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/RWS
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/RWS/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Reader
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Reader/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/State
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/State/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Writer
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Writer/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSmtl-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Cont/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Error/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/RWS/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Reader/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/State/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Monad/Writer/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
