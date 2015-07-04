import csscompressor

from pipeline.compressors import CompressorBase


class CSSCompressor(CompressorBase):
    """
    A CSS compressor using the Python ``csscompressor`` module.
    """
    def compress_css(self, css):
        return csscompressor.compress(css)
