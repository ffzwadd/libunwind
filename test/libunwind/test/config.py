#===----------------------------------------------------------------------===##
#
#                     The LLVM Compiler Infrastructure
#
# This file is dual licensed under the MIT and the University of Illinois Open
# Source Licenses. See LICENSE.TXT for details.
#
#===----------------------------------------------------------------------===##
import os
import sys

from libcxx.test.config import Configuration as LibcxxConfiguration


class Configuration(LibcxxConfiguration):
    # pylint: disable=redefined-outer-name
    def __init__(self, lit_config, config):
        super(Configuration, self).__init__(lit_config, config)
        self.libunwind_src_root = None
        self.libunwind_obj_root = None
        self.abi_library_path = None
        self.libcxx_src_root = None

    def configure_src_root(self):
        self.libunwind_src_root = self.get_lit_conf(
            'libunwind_src_root',
            os.path.dirname(self.config.test_source_root))
        self.libcxx_src_root = self.get_lit_conf(
            'libcxx_src_root',
            os.path.join(self.libunwind_src_root, '/../libcxx'))

    def configure_obj_root(self):
        self.libunwind_obj_root = self.get_lit_conf('libunwind_obj_root')
        super(Configuration, self).configure_obj_root()

    def has_cpp_feature(self, feature, required_value):
        return int(self.cxx.dumpMacros().get('__cpp_' + feature, 0)) >= required_value

    def configure_features(self):
        super(Configuration, self).configure_features()
        if not self.get_lit_bool('enable_exceptions', True):
            self.config.available_features.add('libcxxabi-no-exceptions')

    def configure_compile_flags(self):
        self.cxx.compile_flags += ['-DLIBUNWIND_NO_TIMER']
        if self.get_lit_bool('enable_exceptions', True):
            self.cxx.compile_flags += ['-funwind-tables']
        else:
            self.cxx.compile_flags += ['-fno-exceptions', '-DLIBUNWIND_HAS_NO_EXCEPTIONS']
        if not self.get_lit_bool('enable_threads', True):
            self.cxx.compile_flags += ['-D_LIBUNWIND_HAS_NO_THREADS']
            self.config.available_features.add('libunwind-no-threads')
        super(Configuration, self).configure_compile_flags()

    def configure_compile_flags_header_includes(self):
        self.configure_config_site_header()

        libunwind_headers = self.get_lit_conf(
            'libunwind_headers',
            os.path.join(self.libunwind_src_root, 'include'))
        if not os.path.isdir(libunwind_headers):
            self.lit_config.fatal("libunwind_headers='%s' is not a directory."
                                  % libunwind_headers)
        self.cxx.compile_flags += ['-I' + libunwind_headers]

    def configure_compile_flags_exceptions(self):
        pass

    def configure_compile_flags_rtti(self):
        pass
