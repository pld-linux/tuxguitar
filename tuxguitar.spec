# TODO:
# prepare working sh file :
# java -Djava.library.path=/usr/lib/swt -Dtuxguitar.share.path=/usr/share/tuxguitar \
# -cp /usr/share/java/swt.jar:.:/usr/share/tuxguitar/tuxguitar.jar: org.herac.tuxguitar.gui.TGMain
Summary:	tuxguitar
#Summary(pl.UTF-8):
Name:		tuxguitar
Version:	1.0
Release:	0.2
License:	LGPL v2.1+
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/tuxguitar/%{name}-src-%{version}.tar.gz
# Source0-md5:	a9873adad0df58202d889648eb484879
URL:		http://www.tuxguitar.com.ar/
BuildRequires:	ant
# need eclipse-swt with cairo
BuildRequires:	eclipse-swt
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tuxguitar.

#% description -l pl.UTF-8 #.

%prep
%setup -q -n %{name}-src-%{version}

%build
export JAVA_HOME=%{java_home}
export CLASSPATH=$(build-classpath swt)

%ant -f TuxGuitar/build.xml build
#%ant -f TuxGuitar-CoreAudio/build.xml build
%ant -f TuxGuitar-alsa/build.xml build
%ant -f TuxGuitar-ascii/build.xml build
%ant -f TuxGuitar-browser-ftp/build.xml build
%ant -f TuxGuitar-compat/build.xml build
%ant -f TuxGuitar-converter/build.xml build
%ant -f TuxGuitar-fluidsynth/build.xml build
%ant -f TuxGuitar-gtp/build.xml build
%ant -f TuxGuitar-jsa/build.xml build
%ant -f TuxGuitar-lilypond/build.xml build
%ant -f TuxGuitar-midi/build.xml build
%ant -f TuxGuitar-musicxml/build.xml build
%ant -f TuxGuitar-oss/build.xml build
#%ant -f TuxGuitar-pdf/build.xml build
%ant -f TuxGuitar-ptb/build.xml build
%ant -f TuxGuitar-tef/build.xml build
%ant -f TuxGuitar-tray/build.xml build
%ant -f TuxGuitar-winmm/build.xml build

cp -f TuxGuitar-*/*.jar TuxGuitar/share/plugins/

%ant -f TuxGuitar/build.xml package

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_javadir},%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir}}

%{__make} -C TuxGuitar install DESTDIR=$RPM_BUILD_ROOT

install TuxGuitar/%{name}.jar $RPM_BUILD_ROOT%{_datadir}/%{name}
install TuxGuitar/%{name} $RPM_BUILD_ROOT%{_bindir}

install misc/%{name}.tg $RPM_BUILD_ROOT%{_datadir}/%{name}
install misc/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1
install misc/%{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
install misc/%{name}.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README ChangeLog
%{_javadir}/%{name}.jar
%{_datadir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_pixmapsdir}/%{name}.xpm
%{_desktopdir}/%{name}.desktop
