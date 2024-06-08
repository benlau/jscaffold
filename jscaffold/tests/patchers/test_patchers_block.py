from jscaffold.patchers.block import PatchBlock
import textwrap


def test_block_patch_read():
    source = textwrap.dedent(
        """\
        BEGIN
        value
        END
        """
    )

    patcher = PatchBlock("BEGIN", "END")

    assert patcher.read(source) == "value"


def test_block_patch_read_same_divider():
    source = textwrap.dedent(
        """\
        SEPARATOR
        value
        SEPARATOR
        """
    )

    patcher = PatchBlock("SEPARATOR", "SEPARATOR")

    assert patcher.read(source) == "value"


def test_block_patch_read_not_existed():
    source = textwrap.dedent(
        """\
        BEGIN
        value
        END
        """
    )

    patcher = PatchBlock("BEGIN", "BEGIN")

    assert patcher.read(source) is None


def test_block_patch_write():
    source = textwrap.dedent(
        """\
        BEGIN
        value
        END
        """
    )

    expected = textwrap.dedent(
        """\
        BEGIN
        value2
        END
        """
    )

    patcher = PatchBlock("BEGIN", "END")

    assert patcher.write(source, "value2") == expected


def test_block_write_non_existed():
    source = textwrap.dedent(
        """\
        """
    )

    expected = textwrap.dedent(
        """\

        BEGIN
        value2
        END"""
    )

    patcher = PatchBlock("BEGIN", "END")

    assert patcher.write(source, "value2") == expected
