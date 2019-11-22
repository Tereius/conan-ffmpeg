#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import glob
import shutil


class FFMpegConan(ConanFile):
    name = "ffmpeg"
    version = "4.2"
    url = "https://github.com/Tereius/conan-ffmpeg"
    description = "A complete, cross-platform solution to record, convert and stream audio and video"
    license = "https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md"
    exports = "gas-preprocessor.pl"
    exports_sources = ["LICENSE", "dylibToFramework.sh"]
    settings = "os", "arch", "compiler", "build_type", "os_build", "arch_build"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "postproc": [True, False],
               "zlib": [True, False],
               "bzlib": [True, False],
               "lzma": [True, False],
               "iconv": [True, False],
               "freetype": [True, False],
               "openjpeg": [True, False],
               "openh264": [True, False],
               "opus": [True, False],
               "vorbis": [True, False],
               "zmq": [True, False],
               "sdl2": [True, False],
               "x264": [True, False],
               "x265": [True, False],
               "vpx": [True, False],
               "mp3lame": [True, False],
               "fdk_aac": [True, False],
               "alsa": [True, False],
               "pulse": [True, False],
               "vaapi": [True, False],
               "vdpau": [True, False],
               "xcb": [True, False],
               "appkit": [True, False],
               "avfoundation": [True, False],
               "coreimage": [True, False],
               "audiotoolbox": [True, False],
               "videotoolbox": [True, False],
               "securetransport": [True, False],
               "qsv": [True, False],
               "mediacodec": [True, False]}
    default_options = ("shared=True",
                       "fPIC=True",
                       "postproc=True",
                       "zlib=False",
                       "bzlib=False",
                       "lzma=False",
                       "iconv=False",
                       "freetype=False",
                       "openjpeg=False",
                       "openh264=False",
                       "opus=False",
                       "vorbis=False",
                       "zmq=False",
                       "sdl2=False",
                       "x264=False",
                       "x265=False",
                       "vpx=False",
                       "mp3lame=False",
                       "fdk_aac=False",
                       "alsa=True",
                       "pulse=True",
                       "vaapi=True",
                       "vdpau=True",
                       "xcb=False",
                       "appkit=True",
                       "avfoundation=True",
                       "coreimage=True",
                       "audiotoolbox=True",
                       "videotoolbox=True",
                       "securetransport=True",
                       "qsv=True",
                       "mediacodec=True")

    @property
    def is_mingw_windows(self):
        return self.settings.os == 'Windows' and self.settings.compiler == 'gcc' and os.name == 'nt'

    @property
    def is_android_windows(self):
        return self.settings.os_build == 'Windows' and self.settings.os == 'Android' and os.name == 'nt'

    @property
    def is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    def source(self):
        source_url = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % self.version
        tools.get(source_url)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os != "Linux":
            self.options.remove("vaapi")
            self.options.remove("vdpau")
            self.options.remove("xcb")
            self.options.remove("alsa")
            self.options.remove("pulse")
        if self.settings.os != "Macos" and self.settings.os != "iOS":
            self.options.remove("appkit")
            self.options.remove("avfoundation")
            self.options.remove("coreimage")
            self.options.remove("audiotoolbox")
            self.options.remove("videotoolbox")
            self.options.remove("securetransport")
        if self.settings.os != "Windows":
            self.options.remove("qsv")
        if self.settings.os != "Android":
            self.options.remove("mediacodec")
        if self.settings.os == "iOS":
            self.options.appkit = False

    def build_requirements(self):
        if self.settings.os == 'Android':
            self.options["android-ndk"].makeStandalone = True
            if self.settings.os_build == 'Windows':
                self.build_requires("strawberryperl/5.26.0@conan/stable")
                self.build_requires("msys2_installer/latest@bincrafters/stable")
            self.build_requires("android-ndk/r17b@tereius/stable")
        if self.settings.arch == "x86" or self.settings.arch == "x86_64":
            self.build_requires("yasm_installer/1.3.0@bincrafters/stable")
        if self.settings.os == 'Windows':
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def requirements(self):
        if self.options.zlib:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.bzlib:
            self.requires.add("bzip2/1.0.6@conan/stable")
        if self.options.lzma:
            self.requires.add("lzma/5.2.3@bincrafters/stable")
        if self.options.iconv:
            self.requires.add("libiconv/1.15@bincrafters/stable")
        if self.options.freetype:
            self.requires.add("freetype/2.8.1@bincrafters/stable")
        if self.options.openjpeg:
            self.requires.add("openjpeg/2.3.0@bincrafters/stable")
        if self.options.openh264:
            self.requires.add("openh264/1.7.0@bincrafters/stable")
        if self.options.vorbis:
            self.requires.add("vorbis/1.3.6@bincrafters/stable")
        if self.options.opus:
            self.requires.add("opus/1.2.1@bincrafters/stable")
        if self.options.zmq:
            self.requires.add("zmq/4.2.2@bincrafters/stable")
        if self.options.sdl2:
            self.requires.add("sdl2/2.0.7@bincrafters/stable")
        if self.options.x264:
            self.requires.add("libx264/20171211@bincrafters/stable")
        if self.options.x265:
            self.requires.add("libx265/2.7@bincrafters/stable")
        if self.options.vpx:
            self.requires.add("libvpx/1.7.0@bincrafters/stable")
        if self.options.mp3lame:
            self.requires.add("libmp3lame/3.100@bincrafters/stable")
        if self.options.fdk_aac:
            self.requires.add("libfdk_aac/0.1.5@bincrafters/stable")
        if self.settings.os == "Windows":
            if self.options.qsv:
                self.requires.add("intel_media_sdk/2017R1@bincrafters/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                arch_suffix = ''
                if self.settings.arch == "x86":
                    arch_suffix = ':i386'
                elif self.settings.arch == "x86_64":
                    arch_suffix = ':amd64'

                packages = ['pkg-config']
                if self.options.alsa:
                    packages.append('libasound2-dev%s' % arch_suffix)
                if self.options.pulse:
                    packages.append('libpulse-dev%s' % arch_suffix)
                if self.options.vaapi:
                    packages.append('libva-dev%s' % arch_suffix)
                if self.options.vdpau:
                    packages.append('libvdpau-dev%s' % arch_suffix)
                if self.options.xcb:
                    packages.extend(['libxcb1-dev%s' % arch_suffix,
                                     'libxcb-shm0-dev%s' % arch_suffix,
                                     'libxcb-shape0-dev%s' % arch_suffix,
                                     'libxcb-xfixes0-dev%s' % arch_suffix])
                for package in packages:
                    installer.install(package)
            elif tools.os_info.with_yum:
                installer = tools.SystemPackageTool()
                arch_suffix = ''
                if self.settings.arch == "x86":
                    arch_suffix = '.i686'
                elif self.settings.arch == "x86_64":
                    arch_suffix = '.x86_64'
                packages = ['pkgconfig']
                if self.options.alsa:
                    packages.append('alsa-lib-devel%s' % arch_suffix)
                if self.options.pulse:
                    packages.append('pulseaudio-libs-devel%s' % arch_suffix)
                if self.options.vaapi:
                    packages.append('libva-devel%s' % arch_suffix)
                if self.options.vdpau:
                    packages.append('libvdpau-devel%s' % arch_suffix)
                if self.options.xcb:
                    packages.append('libxcb-devel%s' % arch_suffix)
                for package in packages:
                    installer.install(package)

    def copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dir = os.path.join(root, 'lib', 'pkgconfig')
        pc_files = glob.glob('%s/*.pc' % pc_dir)
        for pc_name in pc_files:
            new_pc = os.path.join('pkgconfig', os.path.basename(pc_name))
            self.output.warn('copy .pc file %s' % os.path.basename(pc_name))
            shutil.copy(pc_name, new_pc)
            prefix = tools.unix_path(root) if self.settings.os == 'Windows' or self.settings.os_build == 'Windows'  else root
            tools.replace_prefix_in_pc_file(new_pc, prefix)

    def build(self):

        if self.is_msvc or self.is_mingw_windows or self.is_android_windows:
            msys_bin = self.deps_env_info['msys2_installer'].MSYS_BIN
            with tools.environment_append({'PATH': [msys_bin],
                                           'CONAN_BASH_PATH': os.path.join(msys_bin, 'bash.exe')}):
                if self.is_msvc:
                    with tools.vcvars(self.settings):
                        self.build_configure()
                else:
                    self.build_configure()
        else:
            self.build_configure()

    def check_pkg_config(self, option, package_name):
        if option:
            pkg_config = tools.PkgConfig(package_name)
            if not pkg_config.provides:
                raise Exception('package %s is not available' % package_name)

    def check_dependencies(self):
        if self.settings.os == 'Linux':
            self.check_pkg_config(self.options.alsa, 'alsa')
            self.check_pkg_config(self.options.pulse, 'libpulse')
            self.check_pkg_config(self.options.vaapi, 'libva')
            self.check_pkg_config(self.options.vdpau, 'vdpau')
            self.check_pkg_config(self.options.xcb, 'xcb')
            self.check_pkg_config(self.options.xcb, 'xcb-shm')
            self.check_pkg_config(self.options.xcb, 'xcb-shape')
            self.check_pkg_config(self.options.xcb, 'xcb-xfixes')

    def build_configure(self):
        self.check_dependencies()

        #with tools.chdir(self.build_folder + "/sources"):
        prefix = tools.unix_path(self.package_folder) if self.settings.os == 'Windows' or self.settings.os_build == 'Windows' else self.package_folder
        args = ['--prefix=%s' % prefix,
                '--disable-doc',
                '--disable-programs']
        if self.options.shared:
            args.extend(['--disable-static', '--enable-shared'])
        else:
            args.extend(['--disable-shared', '--enable-static'])
        args.append('--pkg-config-flags=--static')
        if self.settings.build_type == 'Debug':
            args.extend(['--disable-optimizations', '--disable-mmx', '--disable-stripping', '--enable-debug'])
        if self.is_msvc:
            args.append('--toolchain=msvc')
            args.append('--extra-cflags=-%s' % self.settings.compiler.runtime)
            if int(str(self.settings.compiler.version)) <= 12:
                # Visual Studio 2013 (and earlier) doesn't support "inline" keyword for C (only for C++)
                args.append('--extra-cflags=-Dinline=__inline' % self.settings.compiler.runtime)

        if self.settings.arch == 'x86':
            args.append('--arch=x86')
        elif str(self.settings.arch).startswith('armv6'):
            args.append('--arch=armv6-m')
        elif str(self.settings.arch).startswith('armv7'):
            args.append('--arch=armv7-a')
        elif str(self.settings.arch).startswith('armv8'):
            args.append('--arch=arm64')

        args.append('--enable-postproc' if self.options.postproc else '--disable-postproc')
        args.append('--enable-pic' if self.options.fPIC else '--disable-pic')
        args.append('--enable-zlib' if self.options.zlib else '--disable-zlib')
        args.append('--enable-bzlib' if self.options.bzlib else '--disable-bzlib')
        args.append('--enable-lzma' if self.options.lzma else '--disable-lzma')
        args.append('--enable-iconv' if self.options.iconv else '--disable-iconv')
        args.append('--enable-libfreetype' if self.options.freetype else '--disable-libfreetype')
        args.append('--enable-libopenjpeg' if self.options.openjpeg else '--disable-libopenjpeg')
        args.append('--enable-libopenh264' if self.options.openh264 else '--disable-libopenh264')
        args.append('--enable-libvorbis' if self.options.vorbis else '--disable-libvorbis')
        args.append('--enable-libopus' if self.options.opus else '--disable-libopus')
        args.append('--enable-libzmq' if self.options.zmq else '--disable-libzmq')
        args.append('--enable-sdl2' if self.options.sdl2 else '--disable-sdl2')
        args.append('--enable-libx264' if self.options.x264 else '--disable-libx264')
        args.append('--enable-libx265' if self.options.x265 else '--disable-libx265')
        args.append('--enable-libvpx' if self.options.vpx else '--disable-libvpx')
        args.append('--enable-libmp3lame' if self.options.mp3lame else '--disable-libmp3lame')
        args.append('--enable-libfdk-aac' if self.options.fdk_aac else '--disable-libfdk-aac')

        if self.options.x264 or self.options.x265 or self.options.postproc:
            args.append('--enable-gpl')

        if self.options.fdk_aac:
            args.append('--enable-nonfree')

        if self.settings.os == "Linux":
            args.append('--enable-alsa' if self.options.alsa else '--disable-alsa')
            args.append('--enable-libpulse' if self.options.pulse else '--disable-libpulse')
            args.append('--enable-vaapi' if self.options.vaapi else '--disable-vaapi')
            args.append('--enable-vdpau' if self.options.vdpau else '--disable-vdpau')
            if self.options.xcb:
                args.extend(['--enable-libxcb', '--enable-libxcb-shm',
                                '--enable-libxcb-shape', '--enable-libxcb-xfixes'])
            else:
                args.extend(['--disable-libxcb', '--disable-libxcb-shm',
                                '--disable-libxcb-shape', '--disable-libxcb-xfixes'])

        if self.settings.os == "Macos" or self.settings.os == "iOS":
            args.append('--enable-appkit' if self.options.appkit else '--disable-appkit')
            args.append('--enable-avfoundation' if self.options.avfoundation else '--disable-avfoundation')
            args.append('--enable-coreimage' if self.options.avfoundation else '--disable-coreimage')
            args.append('--enable-audiotoolbox' if self.options.audiotoolbox else '--disable-audiotoolbox')
            args.append('--enable-videotoolbox' if self.options.videotoolbox else '--disable-videotoolbox')
            args.append('--enable-securetransport' if self.options.securetransport else '--disable-securetransport')
            args.append('--install-name-dir=@rpath')

        if self.settings.os == "iOS":
            args.append('--enable-cross-compile')
            args.append('--target-os=darwin')
            #args.append('--sysroot=/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS%s.sdk' % self.settings.os.version)
            args.append('--cc=xcrun -sdk iphoneos clang')
            args.append('--as=gas-preprocessor.pl -arch aarch64 -- xcrun -sdk iphoneos clang')
            args.append('--extra-cflags=-arch arm64 -mios-version-min=8.0 -fembed-bitcode')
            args.append('--extra-ldflags=-arch arm64 -mios-version-min=8.0 -fembed-bitcode')
            args.append('--install-name-dir=@rpath')

        if self.settings.os == "Windows":
            args.append('--enable-libmfx' if self.options.qsv else '--disable-libmfx')

        if self.settings.os == "Android":
            args.append('--enable-cross-compile')
            args.append('--target-os=android')

            args.append('--nm=' + tools.unix_path(self.deps_env_info['android-ndk'].NM))
            args.append('--ar=' + tools.unix_path(self.deps_env_info['android-ndk'].AR))
            args.append('--ranlib=' + tools.unix_path(self.deps_env_info['android-ndk'].RANLIB))
            args.append('--strip=' + tools.unix_path(self.deps_env_info['android-ndk'].STRIP))
            if self.settings.compiler == 'clang':
                # if we use arm-linux-androideabi-clang.cmd we will run into the windows cmd.exe max command line length limit during linking. We should use the sh scripts
                args.append('--as=' + tools.unix_path(self.deps_env_info['android-ndk'].CC)[:-4])
                args.append('--ld=' + tools.unix_path(self.deps_env_info['android-ndk'].CC)[:-4])
                args.append('--cc=' + tools.unix_path(self.deps_env_info['android-ndk'].CC)[:-4])
                args.append('--cxx=' + tools.unix_path(self.deps_env_info['android-ndk'].CXX)[:-4])
            else:
                args.append('--as=' + tools.unix_path(self.deps_env_info['android-ndk'].CC))
                args.append('--ld=' + tools.unix_path(self.deps_env_info['android-ndk'].CC))
                args.append('--cc=' + tools.unix_path(self.deps_env_info['android-ndk'].CC))
                args.append('--cxx=' + tools.unix_path(self.deps_env_info['android-ndk'].CXX))
            #args.append('--objcc=' + tools.unix_path(self.deps_env_info['android-ndk'].OBJCOPY))

            args.append('--sysroot=' + tools.unix_path(self.deps_env_info['android-ndk'].SYSROOT))

            args.append('--cross-prefix=' + self.deps_env_info['android-ndk'].CHOST + '-')
            args.append('--enable-mediacodec' if self.options.mediacodec else '--disable-mediacodec')
            args.append('--enable-jni' if self.options.mediacodec else '--disable-jni')

            if self.settings.compiler == 'clang':
                tools.replace_in_file("./sources/libavdevice/v4l2.c", "int (*ioctl_f)(int fd, unsigned long int request, ...);", "int (*ioctl_f)(int fd, unsigned int request, ...);")

        # FIXME disable CUDA and CUVID by default, revisit later
        args.extend(['--disable-cuda', '--disable-cuvid'])

        tools.mkdir('pkgconfig')
        if self.options.freetype:
            self.copy_pkg_config('freetype')
            self.copy_pkg_config('libpng')
        if self.options.opus:
            self.copy_pkg_config('opus')
        if self.options.vorbis:
            self.copy_pkg_config('ogg')
            self.copy_pkg_config('vorbis')
        if self.options.zmq:
            self.copy_pkg_config('zmq')
        if self.options.sdl2:
            self.copy_pkg_config('sdl2')
        if self.options.x264:
            self.copy_pkg_config('libx264')
        if self.options.x265:
            self.copy_pkg_config('libx265')
        if self.options.vpx:
            self.copy_pkg_config('libvpx')
        if self.options.fdk_aac:
            self.copy_pkg_config('libfdk_aac')
        if self.options.openh264:
            self.copy_pkg_config('openh264')
        if self.options.openjpeg:
            self.copy_pkg_config('openjpeg')

        pkg_config_path = os.path.abspath('pkgconfig')
        pkg_config_path = tools.unix_path(pkg_config_path) if self.settings.os == 'Windows' or self.settings.os_build == 'Windows' else pkg_config_path

        try:
            if self.is_msvc or self.is_mingw_windows or self.is_android_windows:
                # hack for MSYS2 which doesn't inherit PKG_CONFIG_PATH
                for filename in ['.bashrc', '.bash_profile', '.profile']:
                    tools.run_in_windows_bash(self, 'cp ~/%s ~/%s.bak' % (filename, filename))
                    command = 'echo "export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%s" >> ~/%s'\
                                % (pkg_config_path, filename)
                    tools.run_in_windows_bash(self, command)

            env_build = AutoToolsBuildEnvironment(self, win_bash=self.is_mingw_windows or self.is_msvc or self.is_android_windows)

            # ffmpeg's configure is not actually from autotools, so it doesn't understand standard options like
            # --host, --build, --target
            with tools.environment_append({"PATH": [self.build_folder]}): # Add the build folder to the path so that gas-preprocessor.pl can be found

                env_build.configure(args=args, build=False, host=False, target=False,
                                    pkg_config_paths=[pkg_config_path], configure_dir=self.build_folder + "/sources")

                with tools.environment_append(env_build.vars):
                    #self.run("whereis make", win_bash=self.is_mingw_windows or self.is_msvc or self.is_android_windows)
                    self.run("make -j8", win_bash=self.is_mingw_windows or self.is_msvc or self.is_android_windows)
                    self.run("make install", win_bash=self.is_mingw_windows or self.is_msvc or self.is_android_windows)

                #env_build.make()
                #env_build.make(args=['install'])
                #tools.run_in_windows_bash(self, 'make' % (filename, filename))

        finally:
            if self.is_msvc or self.is_mingw_windows or self.is_android_windows:
                for filename in ['.bashrc', '.bash_profile', '.profile']:
                    tools.run_in_windows_bash(self, 'cp ~/%s.bak ~/%s' % (filename, filename))
                    tools.run_in_windows_bash(self, 'rm -f ~/%s.bak' % filename)

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
        if self.is_msvc and not self.options.shared:
            # ffmpeg produces .a files which are actually .lib files
            with tools.chdir(os.path.join(self.package_folder, 'lib')):
                libs = glob.glob('*.a')
                for lib in libs:
                    shutil.move(lib, lib[:-2] + '.lib')
        if self.settings.os == "iOS" and self.settings.build_type == "Release":
            self.run("%s/dylibToFramework.sh %s" % (self.source_folder, self.package_folder))

    def package_info(self):
        libs = ['avdevice', 'avfilter', 'avformat', 'avcodec', 'swresample', 'swscale', 'avutil']
        if self.options.postproc:
            libs.append('postproc')
        if self.is_msvc:
            if self.options.shared:
                self.cpp_info.libs = libs
                self.cpp_info.libdirs.append('bin')
            else:
                self.cpp_info.libs = ['lib' + lib for lib in libs]
        else:
            self.cpp_info.libs = libs
        if self.settings.os == "Macos" or self.settings.os == "iOS":
            frameworks = ['CoreVideo', 'CoreMedia', 'CoreGraphics', 'CoreFoundation', 'Foundation']
            if self.options.appkit:
                frameworks.append('AppKit')
            if self.options.avfoundation:
                frameworks.append('AVFoundation')
            if self.options.coreimage:
                frameworks.append('CoreImage')
            if self.options.audiotoolbox:
                frameworks.append('AudioToolbox')
            if self.options.videotoolbox:
                frameworks.append('VideoToolbox')
            if self.options.securetransport:
                frameworks.append('Security')
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            if self.settings.os == "Macos":
                self.cpp_info.exelinkflags.append("-framework OpenGL")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread'])
            if self.options.alsa:
                self.cpp_info.libs.append('asound')
            if self.options.pulse:
                self.cpp_info.libs.append('pulse')
            if self.options.vaapi:
                self.cpp_info.libs.extend(['va', 'va-drm', 'va-x11'])
            if self.options.vdpau:
                self.cpp_info.libs.extend(['vdpau', 'X11'])
            if self.options.xcb:
                self.cpp_info.libs.extend(['xcb', 'xcb-shm', 'xcb-shape', 'xcb-xfixes'])
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['ws2_32', 'secur32', 'shlwapi', 'strmiids', 'vfw32', 'bcrypt'])
