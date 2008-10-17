# TODO:
# - prepare nice patch or sf
# - fill summary and desc
Summary:	tuxguitar
#Summary(pl.UTF-8):
Name:		tuxguitar
Version:	1.0
Release:	0.7
License:	LGPL v2.1+
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/tuxguitar/%{name}-src-%{version}.tar.gz
# Source0-md5:	a9873adad0df58202d889648eb484879
URL:		http://www.tuxguitar.com.ar/
BuildRequires:	ant
# need eclipse-swt with cairo
BuildRequires:	eclipse-swt
BuildRequires:	fluidsynth-devel
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tuxguitar.

#% description -l pl.UTF-8 #.

%prep
%setup -q -n %{name}-src-%{version}

#based on Fedora spec
#Prevent static library paths to be built in TuxGuitar.jar (META-INF/MANIFEST.MF)
sed -i 's/<attribute name="Class-Path" value="${lib.swt.jar} ${dist.share.path}"\/>//' TuxGuitar/build.xml
# Declare the library path and classpath during runtime instead
sed -i 's|env_$|env_\nexport CLASSPATH=%{_javadir}/swt.jar\n|' misc/tuxguitar.sh
sed -i 's|PACKAGE_LIB:=%{_libdir}/jni|PACKAGE_LIB:=%{_libdir}/%{name}|' misc/tuxguitar.sh
sed -i 's|-Djava.library.path=${PACKAGE_LIB}|-Djava.library.path=${PACKAGE_LIB}:%{_libdir}/swt|' misc/tuxguitar.sh
# Add exec to replace the called shell
sed -i 's|${JAVA} ${JAVA_FLAGS}|exec ${JAVA} ${JAVA_FLAGS}|' misc/tuxguitar.sh

# Disable the pdf plugin that depends on "iText" which is currently not available on Fedora
sed -i 's/TuxGuitar-pdf \\/\\/g' Makefile
sed -i 's/.\/TuxGuitar-pdf\/tuxguitar-pdf.jar \\/\\/g' Makefile
# Change /lib to %%{_lib}, just in case
sed -i 's/\/lib\//\/%{_lib}\//g' Makefile
sed -i 's/\/lib\//\/%{_lib}\//g' misc/tuxguitar.sh
sed -i 's/\/lib\//\/%{_lib}\//g' TuxGuitar/xml/build-linux.xml
# Don't strip the binaries during %%install
sed -i 's/install -s/install -m 755/g' Makefile
# Remove pre-shipped binaries
find -name .DS_Store -exec rm {} \;

%build
export JAVA_HOME=%{java_home}
export CLASSPATH=$(build-classpath swt)

%{__make} SWT_JAR=$(build-classpath swt) CFLAGS="${RPM_OPT_FLAGS} -I%{JAVA_HOME}/include -I%{JAVA_HOME}/include/linux -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir}}

%{__make} DESTDIR=$RPM_BUILD_ROOT INSTALL_LIB_DIR=$RPM_BUILD_ROOT/%{_libdir}/%{name} install
%{__make} DESTDIR=$RPM_BUILD_ROOT INSTALL_LIB_DIR=$RPM_BUILD_ROOT/%{_libdir}/%{name} install-linux

cp -f TuxGuitar-*/*.jar TuxGuitar/share/plugins/
%{__make} -C TuxGuitar install DESTDIR=$RPM_BUILD_ROOT

install TuxGuitar/%{name}.jar $RPM_BUILD_ROOT%{_datadir}/%{name}

install misc/%{name}.tg $RPM_BUILD_ROOT%{_datadir}/%{name}
install misc/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1
install misc/%{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
install misc/%{name}.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README ChangeLog
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libtuxguitar-*.so
%{_datadir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_pixmapsdir}/%{name}.xpm
%{_desktopdir}/%{name}.desktop
