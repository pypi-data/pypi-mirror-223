#!/usr/bin/env python3

# Copyright 2015, 2017, 2019-2023 National Research Foundation (SARAO)
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import configparser
import glob
import os
import os.path
import subprocess

from pybind11.setup_helpers import ParallelCompile, Pybind11Extension, build_ext
from setuptools import setup


class BuildExt(build_ext):
    user_options = build_ext.user_options + [
        ("coverage", None, "build with GCC --coverage option"),
        ("split-debug=", None, "write debug symbols to a separate directory"),
    ]
    boolean_options = build_ext.boolean_options + ["coverage"]

    def initialize_options(self):
        build_ext.initialize_options(self)
        # setuptools bug causes these to be lost during reinitialization by
        # ./setup.py develop
        if not hasattr(self, "coverage"):
            self.coverage = None
        if not hasattr(self, "split_debug"):
            self.split_debug = None

    def run(self):
        self.mkpath(self.build_temp)
        subprocess.check_call(os.path.abspath("configure"), cwd=self.build_temp)
        config = configparser.ConfigParser()
        config.read(os.path.join(self.build_temp, "python-build.cfg"))
        for extension in self.extensions:
            extension.extra_compile_args.extend(config["compiler"]["CFLAGS"].split())
            extension.extra_link_args.extend(config["compiler"]["LIBS"].split())
            if self.coverage:
                extension.extra_compile_args.extend(["-g", "-O0", "--coverage"])
                extension.libraries.extend(["gcov"])
            if self.split_debug:
                extension.extra_compile_args.extend(["-g"])
            extension.include_dirs.insert(0, os.path.join(self.build_temp, "include"))
        super().run()

    def build_extensions(self):
        # Stop GCC complaining about -Wstrict-prototypes in C++ code
        try:
            self.compiler.compiler_so.remove("-Wstrict-prototypes")
        except ValueError:
            pass
        super().build_extensions()

    def build_extension(self, ext):
        ext_path = self.get_ext_fullpath(ext.name)
        if self.split_debug:
            # If the base class decides to skip the link, we'll end up
            # constructing the .debug file from the already-stripped version of
            # the library, and it won't have any symbols. So force the link by
            # removing the output.
            try:
                os.remove(ext_path)
            except OSError:
                pass
        super().build_extension(ext)
        if self.split_debug:
            os.makedirs(self.split_debug, exist_ok=True)
            basename = os.path.basename(ext_path)
            debug_path = os.path.join(self.split_debug, basename + ".debug")
            self.spawn(["objcopy", "--only-keep-debug", "--", ext_path, debug_path])
            self.spawn(["strip", "--strip-debug", "--strip-unneeded", "--", ext_path])
            old_cwd = os.getcwd()
            # See the documentation for --add-gnu-debuglink for why it needs to be
            # run from the directory containing the file.
            ext_path_abs = os.path.abspath(ext_path)
            try:
                os.chdir(self.split_debug)
                self.spawn(
                    [
                        "objcopy",
                        "--add-gnu-debuglink=" + os.path.basename(debug_path),
                        "--",
                        ext_path_abs,
                    ]
                )
            finally:
                os.chdir(old_cwd)
            self.spawn(["chmod", "-x", "--", debug_path])


# Can't actually install on readthedocs.org because we can't compile,
# but we need setup.py to still be successful to make the doc build work.
rtd = os.environ.get("READTHEDOCS") == "True"

if not rtd:
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "configure")):
        raise SystemExit(
            "configure not found. Either download a release "
            + "from https://pypi.org/project/spead2 or run "
            + "./bootstrap.sh if not using a release."
        )

    extensions = [
        Pybind11Extension(
            "_spead2",
            sources=(
                glob.glob("src/py_*.cpp")
                + glob.glob("src/common_*.cpp")
                + glob.glob("src/recv_*.cpp")
                + glob.glob("src/send_*.cpp")
            ),
            depends=glob.glob("include/spead2/*.h"),
            language="c++",
            include_dirs=["include"],
            # We don't need to pass boost objects across shared library
            # boundaries. These macros makes -fvisibility=hidden do its job.
            # The first is asio-specific, while the latter is only used in
            # Boost 1.81+.
            define_macros=[
                ("BOOST_ASIO_DISABLE_VISIBILITY", None),
                ("BOOST_DISABLE_EXPLICIT_SYMBOL_VISIBILITY", None),
            ],
        )
    ]
else:
    extensions = []

ParallelCompile("SPEAD2_NUM_BUILD_JOBS").install()
setup(ext_package="spead2", ext_modules=extensions, cmdclass={"build_ext": BuildExt})
