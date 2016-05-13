%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Fallback to rh-nodejs4 rh-nodejs4-scldevel is probably not available in
# the buildroot.
%{!?scl_nodejs:%global scl_nodejs rh-nodejs4}
%{!?scl_prefix_nodejs:%global scl_prefix_nodejs %{scl_nodejs}-}

# Generated from shoulda-matchers-2.6.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name shoulda-matchers

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.8.0
Release: 4%{?dist}
Summary: Making tests easy on the fingers and eyes
Group: Development/Languages
License: MIT
URL: https://github.com/thoughtbot/shoulda-matchers
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix}rubygem(activesupport) >= 3.0.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(bundler)
BuildRequires: %{?scl_prefix}rubygem(bcrypt)
BuildRequires: %{?scl_prefix}rubygem(rspec)
BuildRequires: %{?scl_prefix}rubygem(byebug)
BuildRequires: %{?scl_prefix}rubygem(coffee-rails)
BuildRequires: %{?scl_prefix}rubygem(jbuilder)
BuildRequires: %{?scl_prefix}rubygem(jquery-rails)
BuildRequires: %{?scl_prefix}rubygem(rails)
BuildRequires: %{?scl_prefix}rubygem(sass-rails)
BuildRequires: %{?scl_prefix}rubygem(sdoc)
BuildRequires: %{?scl_prefix}rubygem(shoulda-context)
BuildRequires: %{?scl_prefix}rubygem(spring)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix}rubygem(turbolinks)
BuildRequires: %{?scl_prefix}rubygem(uglifier)
BuildRequires: %{?scl_prefix}rubygem(web-console)
BuildRequires: %{?scl_prefix}rubygem(activeresource)
BuildRequires: %{?scl_prefix}rubygem(protected_attributes)
BuildRequires: %{?scl_prefix}rubygem(rspec-rails)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

BuildRequires: %{?scl_prefix_nodejs}nodejs

%description
shoulda-matchers provides Test::Unit- and RSpec-compatible one-liners that
test common Rails functionality. These tests would otherwise be much longer,
more complex, and error-prone.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix permissions.
# https://github.com/thoughtbot/shoulda-matchers/pull/744
chmod a-x %{buildroot}%{gem_instdir}/doc_config/yard/templates/default/fulldoc/html/css/bootstrap.css

%check
pushd .%{gem_instdir}

# It is easier to recreate the Gemfile to use local versions of gems.
rm Gemfile.lock
cat << GF > Gemfile
source 'https://rubygems.org'

gem 'activeresource'
gem 'bcrypt'
gem 'protected_attributes'
gem 'rspec-rails'
gem 'rails'
gem 'sqlite3'
# Required for /spec/acceptance/rails_integration_spec.rb:55
# but we don't have spring-commands-rspec in Fedora yet.
# gem 'spring'
GF

# Seems that AR changed the way how the ranges are checked. Disable the
# offending tests for now.
# https://github.com/thoughtbot/shoulda-matchers/issues/743
sed -i '/active_record_can_raise_range_error?/ a\      return false' spec/support/unit/helpers/active_record_versions.rb

# RSpec doesn't suppor #expects anymore.
# https://github.com/thoughtbot/shoulda-matchers/commit/093268eac41ec3fe86d37eb316c2ab15ae3b9a46
sed -i 's/double.expects/allow(double).to receive/' spec/unit/shoulda/matchers/doublespeak/stub_implementation_spec.rb

%{?scl:scl enable %{scl} - << \EOF}
bundle exec rspec spec/unit
%{?scl:EOF}

# minitest-reporters is not available in Fedora yet.
mv spec/acceptance/independent_matchers_spec.rb{,.disabled}

# JS runtime is needed.
%{?scl:scl enable %{scl} %{scl_nodejs} - << \EOF}
bundle exec rspec spec/acceptance
%{?scl:EOF}

popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
# This would just complicate licensing due to bundled JS/CSS without any
# real benefit.
%exclude %{gem_instdir}/doc_config
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Appraisals
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile*
%{gem_instdir}/NEWS.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/cucumber.yml
%{gem_instdir}/gemfiles
%doc %{gem_instdir}/docs.watchr
%{gem_instdir}/script
%{gem_instdir}/shoulda-matchers.gemspec
%{gem_instdir}/spec
%{gem_instdir}/tasks

%changelog
* Thu Apr 07 2016 Pavel Valena <pvalena@redhat.com> - 2.8.0-4
- Add missing dependencies to BuildRequires
- Enable tests

* Wed Mar 02 2016 Pavel Valena <pvalena@redhat.com> - 2.8.0-3
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 26 2015 Vít Ondruch <vondruch@redhat.com> - 2.8.0-1
- Update to should-matchers 2.8.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Vít Ondruch <vondruch@redhat.com> - 2.6.1-3
- Workaround RoR 4.1.2+ compatibility issue.
- Relax Rake dependency.

* Thu Jul 03 2014 Vít Ondruch <vondruch@redhat.com> - 2.6.1-2
- Add missing BR: rubygem(shoulda-context).
- Updated upstream URL.
- Relaxed BR: ruby dependency.

* Mon Jun 30 2014 Vít Ondruch <vondruch@redhat.com> - 2.6.1-1
- Initial package
