import csscompressor
import rjsmin

from pipeline.compressors import CompressorBase


class CSSCompressor(CompressorBase):
    """
    A CSS compressor using the Python ``csscompressor`` module.
    """
    def compress_css(self, css):
        return csscompressor.compress(css)


class RJSMinCompressor(CompressorBase):
    """
    A JS compressor using the Python ``rjsmin`` module.

    Comments beginning /*! will be preserved.
    """
    def compress_js(self, js):
        return rjsmin.jsmin(js, keep_bang_comments=True)
