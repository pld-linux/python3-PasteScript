#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	A pluggable command-line tool
Summary(pl.UTF-8):	Narzędzie linii poleceń z obsługą wtyczek
Name:		python3-PasteScript
Version:	3.3.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pastescript/
Source0:	https://files.pythonhosted.org/packages/source/P/PasteScript/PasteScript-%{version}.tar.gz
# Source0-md5:	f8a20ba18f7bb64d5c17ace06151181a
Patch0:		%{name}-template_dir_assemble.patch
URL:		https://pypi.org/project/pastescript/
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-setuptools >= 0.6-0.a9.1
%if %{with tests}
BuildRequires:	python3-Paste >= 3.0
BuildRequires:	python3-PasteDeploy >= 1.3.3
BuildRequires:	python3-nose >= 0.11
BuildRequires:	python3-six
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a pluggable command-line tool. It includes some built-in
features:
- Create file layouts for packages. For instance:
   $ paste create  --template=basic_package MyPackage
  will create a setuptools-ready file layout.
- Serving up web applications, with configuration based on
  paste.deploy.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzie linii poleceń z obsługą wtyczek. Niektóre
możliwości ma wbudowane:
- tworzenie plików dla pakietów, na przykład:
   $ paste create  --template=basic_package MyPackage
  utworzy plik dla setuptools.
- możliwość użycia w aplikacjach WWW z konfiguracją opartą na
  paste.deploy.

%package apidocs
Summary:	API documentation for Python PasteScript module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona PasteScript
Group:		Documentation

%description apidocs
API documentation for Python PasteScript module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona PasteScript.

%prep
%setup -q -n PasteScript-%{version}
%patch0 -p1

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
nosetests-%{py3_ver} tests -e test_list
# test_list requires clean venv(?)
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/paster
%{py3_sitescriptdir}/paste/script
%{py3_sitescriptdir}/PasteScript-%{version}-py*.egg-info
%{py3_sitescriptdir}/PasteScript-%{version}-py*-nspkg.pth

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,modules,*.html,*.js}
%endif
