import os
import struct
import sys
import unittest
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
for p in (TOOLS, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

from cubelib.srf import (SRF, SRFError, KIND_SKIN, KIND_XML, KIND_PNG,  # noqa: E402
                         KIND_DIB, KIND_SVG, KIND_BMP)

HEADER = b'Steinberg Resource File\r\n'
NAME = b'/Thumbs.db\r\n'


def member(payload, stored=None):
    """A member preceded by the leftover name line, zlib-compressed."""
    return NAME + zlib.compress(payload)


def png(w, h):
    ihdr = struct.pack('>II', w, h) + bytes(13)
    return (b'\x89PNG\r\n\x1a\n' + struct.pack('>I', 13) + b'IHDR' + ihdr +
            b'\x00\x00\x00\x00IEND\xaeB`\x82')


def stored_png(w, h):
    body = png(w, h)
    return NAME + body


def dib(w, h):
    return member(struct.pack('<Iii', 40, w, h) + bytes(32))


SKIN = b'<skin><template name="AudioConnections" title="Audio Connections"/>' \
       b'<template name="AddTrack" title="Add Track"/></skin>'
XML = b'<?xml version="1.0"?><thing/>'
SVG = b'<svg id="Raster_Icons"></svg>'


def build():
    out = bytearray(HEADER)
    out += member(SKIN)
    out += member(XML)
    out += member(png(22, 22))
    out += stored_png(44, 44)
    out += dib(86, 60)
    out += member(SVG)
    out += bytes([0x5A, 0x5A, 0x5A, 0x5A, 0x5A])       # trailing junk
    return bytes(out)


class TestSRF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blob = build()
        cls.srf = SRF(cls.blob, path='fixture.srf')

    def test_rejects_foreign_file(self):
        with self.assertRaises(SRFError):
            SRF(b'this is not a resource file' * 10)._parse()

    def test_member_count_and_kinds(self):
        kinds = [m.kind for m in self.srf]
        self.assertEqual(kinds, [KIND_SKIN, KIND_XML, KIND_PNG, KIND_PNG,
                                 KIND_DIB, KIND_SVG])

    def test_payloads_round_trip(self):
        m = list(self.srf)
        self.assertEqual(m[0].payload, SKIN)
        self.assertEqual(m[1].payload, XML)
        self.assertEqual(m[5].payload, SVG)

    def test_offsets_account_for_the_name_line(self):
        # every member is preceded by the leftover /Thumbs.db name line, so
        # bodies are 12 bytes apart, not back to back
        expect = len(HEADER) + len(NAME)
        for mem in self.srf:
            self.assertEqual(mem.offset, expect)
            expect += mem.stored_size + len(NAME)
        self.assertEqual(expect - len(NAME), self.srf.trailing_offset)

    def test_len_and_iter(self):
        self.assertEqual(len(self.srf), 6)
        self.assertEqual(len(list(self.srf)), 6)

    def test_skin_xml_concatenates(self):
        self.assertEqual(self.srf.skin_xml(), SKIN + XML)

    def test_image_dimensions(self):
        dims = self.srf.image_dimensions()
        self.assertEqual(dims.get((22, 22)), 1)
        self.assertEqual(dims.get((44, 44)), 1)
        self.assertEqual(dims.get((86, 60)), 1)

    def test_images_helper(self):
        # 2 PNG + 1 DIB; the SVG is vector art and counted separately
        self.assertEqual(len(self.srf.images()), 3)
        self.assertEqual(len(self.srf.by_kind(KIND_SVG)), 1)

    def test_by_kind(self):
        self.assertEqual(len(self.srf.by_kind(KIND_PNG)), 2)

    def test_summary_reports_coverage(self):
        s = self.srf.summary()
        self.assertIn('6 members', s)
        self.assertIn('5 trailing bytes', s)
        self.assertIn('accounted for', s)

    def test_names_from_trailing_table(self):
        self.assertIn('ZZZZ', ' '.join(self.srf.names()))


class TestSRFEmpty(unittest.TestCase):
    def test_header_only(self):
        srf = SRF(HEADER)
        self.assertEqual(len(srf), 0)
        # the CRLF that ends the header line is left over, not a member
        self.assertEqual(srf.trailing, b'\r\n')

    def test_stops_at_unrecognised_data(self):
        srf = SRF(HEADER + b'\x11\x22\x33\x44' * 8)
        self.assertEqual(len(srf), 0)


if __name__ == '__main__':
    unittest.main()
