from colabrun.colabrun import main


def test_colabrun_forms(capsys):
    args = ["./examples/forms.py", "--text", "San Juan!"]
    main("test", args)
    captured = capsys.readouterr()
    result = captured.out
    assert "San Juan!" in result
