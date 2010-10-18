%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}
%{!?gemdir: %global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)}
%global gemname ffi
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global libname %{gemname}_c.so 
%global githubhash b69a5e3
%global tarballname ffi-ffi-%{githubhash}

Name:           rubygem-%{gemname}
Version:        0.6.3
Release:        1%{?dist}
Summary:        FFI Extensions for Ruby
Group:          Development/Languages

License:        BSD
URL:            http://wiki.github.com/ffi/ffi
# The source file is hosted at github. You can access this tarball with
# the following link:
#          http://github.com/ffi/ffi/tarball/0.5.4
Source0:        %{tarballname}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  ruby ruby-devel rubygems rubygem(rake) rubygem(rake-compiler) libffi-devel rubygem(rspec)
BuildRequires:  pkgconfig
Requires:       rubygems
Requires:       ruby(abi) = 1.8
Provides:       rubygem(%{gemname}) = %{version}

%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here[http://wiki.github.com/ffi/ffi/why-use-ffi].

%prep
%setup -q -n %{tarballname}

%build
export CFLAGS="%{optflags}"
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
rake gem
gem install -V -d --local --no-ri -i ./geminst --force pkg/%{gemname}-%{version}.gem 

%install
rm -rf %{buildroot}
mkdir %{buildroot}
install -d -m0755 %{buildroot}%{gemdir}
install -d -m0755  %{buildroot}%{ruby_sitearch}
cp -R %{_builddir}/%{tarballname}/geminst/* %{buildroot}%{gemdir}
mv %{buildroot}%{geminstdir}/lib/%{libname} %{buildroot}%{ruby_sitearch}/%{libname} 
rm -rf %{buildroot}%{geminstdir}/lib/%{libname}
rm -rf %{buildroot}%{geminstdir}/ext

%check
rake test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{geminstdir}/README.rdoc 
%doc %{geminstdir}/History.txt
%doc %{geminstdir}/LICENSE 
%doc %{gemdir}/doc/%{gemname}-%{version}
%dir %{geminstdir}
%{geminstdir}/.require_paths
%{geminstdir}/Rakefile
%{geminstdir}/gen
%{geminstdir}/lib
%{geminstdir}/spec
%{geminstdir}/tasks
%{ruby_sitearch}/%{libname}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec 


%changelog
* Wed Mar 10 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Power PC fixes from upstream which were found testing 0.6.2

* Tue Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Pull in 0.6.2 from upstream

* Tue Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-3
- Final updates based on package review

* Tue Feb 16 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-2
- Updates Based on code review comments

* Mon Feb 15 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-1
- Initial specfile
