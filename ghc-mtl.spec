%define		pkgname	mtl
Summary:	A Haskell binding to the mtl graphics library
Summary(pl.UTF-8):	Wiązanie Haskella do biblioteki graficznej mtl
Name:		ghc-%{pkgname}
Version:	2.1.2
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/mtl/
Source0:	http://hackage.haskell.org/package/mtl-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	943c110524d96126bfa0e61f7df1ebcd
URL:		http://hackage.haskell.org/package/mtl/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-transformers >= 0.3
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-transformers >= 0.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

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

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
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
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
