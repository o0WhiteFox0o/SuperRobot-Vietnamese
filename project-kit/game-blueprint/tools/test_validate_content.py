import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_content as vc  # noqa: E402

EXAMPLE = HERE.parent / "examples" / "content"


class ValidateContentTest(unittest.TestCase):
    def copy(self):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        out = d / "c"
        shutil.copytree(EXAMPLE, out)
        return out

    def test_example_is_clean(self):
        errors, _ = vc.validate(EXAMPLE)
        self.assertEqual(errors, [])

    def test_broken_weapon_reference(self):
        c = self.copy()
        p = c / "data" / "units.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d["records"][0]["weapons"].append("weapon.nope")
        p.write_text(json.dumps(d), encoding="utf-8")
        errors, _ = vc.validate(c)
        self.assertTrue(any("weapon.nope" in e for e in errors))

    def test_unknown_field_and_duplicate_id(self):
        c = self.copy()
        p = c / "data" / "weapons.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d["records"][1]["id"] = d["records"][0]["id"]
        d["records"][0]["extra"] = 1
        p.write_text(json.dumps(d), encoding="utf-8")
        errors, _ = vc.validate(c)
        self.assertTrue(any("unknown field" in e for e in errors))
        self.assertTrue(any("duplicate id" in e for e in errors))

    def test_bad_next_scene(self):
        c = self.copy()
        p = c / "scenes" / "scene-001.json"
        p.write_text(p.read_text(encoding="utf-8").replace("scene.002\"}", "scene.999\"}"), encoding="utf-8")
        errors, _ = vc.validate(c)
        self.assertTrue(any("scene.999" in e for e in errors))

    def test_upgrade_curve_length(self):
        c = self.copy()
        p = c / "data" / "rules" / "upgrade-rules.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d["curve"] = d["curve"][:10]
        p.write_text(json.dumps(d), encoding="utf-8")
        errors, _ = vc.validate(c)
        self.assertTrue(any("curve" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
