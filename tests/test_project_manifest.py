"""Owned synthetic repositories exercise the real bound release consumer."""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tarfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
CONSUMER = ROOT / "scripts/check-project-manifest.py"
GIT = shutil.which("git")


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="shelltutor-manifest-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("GIT_", "SHELLTUTOR_"))}
        self.env.update(HOME=str(self.root), XDG_CONFIG_HOME=str(self.root / "config"),
                        LC_ALL="C", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.assertIsNotNone(GIT, "prepared Git 2.56+ is a contributor prerequisite")
        self.git("init", "--quiet")
        (self.root / "scripts").mkdir()
        shutil.copyfile(CONSUMER, self.root / "scripts/check-project-manifest.py")
        shutil.copytree(ROOT / "vendor", self.root / "vendor")
        shutil.copyfile(ROOT / "project.yaml", self.root / "project.yaml")
        shutil.copyfile(ROOT / ".gitattributes", self.root / ".gitattributes")
        (self.root / "STATUS.md").write_text("# Synthetic project status\n")
        wrapper = self.root / "scripts/verify-project.sh"
        wrapper.write_text("#!/usr/bin/env bash\nexit 0\n")
        wrapper.chmod(0o755)
        self.git("add", "--", ".")
        self.git("commit", "--quiet", "-m", "Synthetic fixture")
        self.rev = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        result = subprocess.run([GIT, "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
                                 "-c", "commit.gpgsign=false", "-c", "user.name=Fixture",
                                 "-c", "user.email=fixture@example.invalid", *args],
                                cwd=self.root, env=self.env, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def invoke(self, *args, expected=0, environment=None):
        env = {key: value for key, value in self.env.items() if not key.startswith("GIT_")}
        env.update(environment or {})
        result = subprocess.run([sys.executable, "-I", "-S", "-B",
                                 str(self.root / "scripts/check-project-manifest.py"), *args],
                                cwd=self.root, env=env, capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        record = json.loads(result.stdout)
        self.assertEqual(record["exit_code"], expected)
        return record

    def test_real_release_worktree_staged_and_revision(self):
        for args, mode in [((), "worktree"), (("--staged",), "staged"), (("--rev", self.rev), "rev")]:
            with self.subTest(mode=mode):
                result = self.invoke(*args)
                self.assertEqual(result["mode"], mode)
                self.assertEqual(result["declaration_checks"], "passed")
                self.assertEqual(result["native_contract"], "matched")
                self.assertEqual(result["complete_v1_validity"], "not_checked")
                self.assertEqual(result["runtime_acceptance"], "not_checked")

    def test_unknown_key_is_invalid_not_unavailable(self):
        with (self.root / "project.yaml").open("a") as stream:
            stream.write('surplus: "not permitted"\n')
        result = self.invoke(expected=1)
        self.assertEqual(result["declaration_checks"], "failed")
        self.assertEqual(result["findings"][0]["code"], "KEY_UNKNOWN")

    def test_staged_invalid_does_not_change_revision_verdict(self):
        manifest = self.root / "project.yaml"
        manifest.write_text(manifest.read_text().replace('operational_state: unverified',
                                                        'operational_state: impossible'))
        self.git("add", "project.yaml")
        self.invoke("--staged", expected=1)
        self.invoke("--rev", self.rev)

    def test_reference_must_exist_in_selected_tree(self):
        self.git("rm", "STATUS.md")
        self.git("commit", "--quiet", "-m", "Remove synthetic reference")
        revision = self.git("rev-parse", "HEAD").strip()
        result = self.invoke("--rev", revision, expected=1)
        self.assertEqual(result["findings"][0]["code"], "REFERENCE_MISSING")
        self.invoke("--rev", self.rev)

    def test_script_executable_mode_required(self):
        self.git("update-index", "--chmod=-x", "scripts/verify-project.sh")
        result = self.invoke("--staged", expected=1)
        self.assertEqual(result["findings"][0]["code"], "REFERENCE_MODE")

    def test_wrong_native_target_fails_conformance(self):
        other = self.root / "scripts/other.sh"
        other.write_text("#!/bin/sh\nexit 0\n")
        other.chmod(0o755)
        self.git("add", "scripts/other.sh")
        manifest = self.root / "project.yaml"
        manifest.write_text(manifest.read_text().replace('scripts/verify-project.sh', 'scripts/other.sh'))
        result = self.invoke(expected=1)
        self.assertEqual(result["declaration_checks"], "passed")
        self.assertEqual(result["native_contract"], "mismatch")

    def test_bootstrap_tamper_is_refused_before_execution(self):
        bootstrap = self.root / "vendor/project-manifest/release_verifier.py"
        marker = self.root / "executed"
        bootstrap.write_text("from pathlib import Path\nPath(" + repr(str(marker)) + ").touch()\n")
        result = self.invoke(expected=1)
        self.assertEqual(result["consumer_findings"], ["BOOTSTRAP_DIGEST"])
        self.assertFalse(marker.exists())

    def test_payload_tamper_is_refused_before_execution(self):
        payload = self.root / "vendor/project-manifest/release-1/src/project_manifest/acquire.py"
        payload.write_text("raise AssertionError('must not execute')\n")
        result = self.invoke(expected=1)
        self.assertEqual(result["consumer_findings"], ["RELEASE_BINDING"])

    def test_extra_vendor_file_is_refused(self):
        (self.root / "vendor/project-manifest/release-1/extra").write_text("extra\n")
        self.invoke(expected=1)

    def test_symlinked_bootstrap_is_unavailable(self):
        bootstrap = self.root / "vendor/project-manifest/release_verifier.py"
        saved = self.root / "bootstrap.py"
        bootstrap.rename(saved)
        bootstrap.symlink_to(saved)
        self.invoke(expected=2)

    def test_inherited_git_override_does_not_redirect_observation(self):
        before = hashlib.sha256((self.root / ".git/config").read_bytes()).hexdigest()
        result = self.invoke(expected=2, environment={"GIT_DIR": str(self.root / ".git")})
        self.assertEqual(result["declaration_checks"], "not_checked")
        self.assertEqual(before, hashlib.sha256((self.root / ".git/config").read_bytes()).hexdigest())

    def test_missing_git_is_unavailable(self):
        self.invoke(expected=2, environment={"PATH": str(self.root / "absent")})

    def test_revision_selector_requires_full_oid(self):
        result = self.invoke("--rev", "HEAD", expected=2)
        self.assertEqual(result["consumer_findings"], ["SOURCE_SELECTION"])

    def test_ci_revision_environment_and_conflict(self):
        result = self.invoke(environment={"SHELLTUTOR_MANIFEST_REV": self.rev})
        self.assertEqual(result["commit_oid"], self.rev)
        self.invoke("--staged", expected=2, environment={"SHELLTUTOR_MANIFEST_REV": self.rev})

    def test_linked_worktree_needs_explicit_common_directory(self):
        linked = self.root / "linked"
        self.git("worktree", "add", "--quiet", "--detach", str(linked), self.rev)
        env = {key: value for key, value in self.env.items() if not key.startswith("GIT_")}
        command = [sys.executable, "-I", "-S", "-B", str(linked / "scripts/check-project-manifest.py")]
        refused = subprocess.run(command, cwd=linked, env=env, capture_output=True, text=True, timeout=45)
        self.assertEqual(refused.returncode, 2, refused.stdout + refused.stderr)
        accepted = subprocess.run(command + ["--git-common-dir", str(self.root / ".git")],
                                  cwd=linked, env=env, capture_output=True, text=True, timeout=45)
        self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_attributes_preserve_exact_release_and_manifest_bytes(self):
        paths = [self.root / "project.yaml"] + sorted(p for p in (self.root / "vendor").rglob("*") if p.is_file())
        before = {str(path.relative_to(self.root)): path.read_bytes() for path in paths}
        attributes = self.root / "outside.attributes"
        attributes.write_text("* text eol=crlf filter=adoption ident working-tree-encoding=UTF-16\n")
        for path in paths:
            path.unlink()
        self.git("-c", "core.attributesFile=" + str(attributes), "-c", "filter.adoption.smudge=exit 97",
                 "-c", "filter.adoption.required=true", "checkout-index", "--force", "--", *before)
        for name, data in before.items():
            self.assertEqual((self.root / name).read_bytes(), data, name)

    def test_wrapper_refuses_arguments_before_make(self):
        result = subprocess.run(["/bin/bash", str(ROOT / "scripts/verify-project.sh"), "unexpected"],
                                cwd=self.root, env=self.env, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="shelltutor-preparation-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        spec = importlib.util.spec_from_file_location("shelltutor_preparation_fixture", ROOT / "scripts/prepare-ci-git.py")
        self.preparation = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.preparation)

    def archive(self, name, *, link=False):
        archive = self.root / "fixture.tar"
        with tarfile.open(archive, "w") as stream:
            info = tarfile.TarInfo(name)
            if link:
                info.type = tarfile.LNKTYPE
                info.linkname = "outside"
                stream.addfile(info)
            else:
                data = b"synthetic source\n"
                info.size = len(data)
                stream.addfile(info, io.BytesIO(data))
        return archive

    def test_archive_traversal_refused_before_extraction(self):
        destination = self.root / "destination"
        with self.assertRaisesRegex(self.preparation.PreparationError, "ARCHIVE_PATH"):
            self.preparation.extract(self.archive("../outside"), destination)
        self.assertFalse(destination.exists())

    def test_archive_hardlink_refused(self):
        destination = self.root / "destination"
        with self.assertRaisesRegex(self.preparation.PreparationError, "ARCHIVE_ENTRY"):
            self.preparation.extract(self.archive("alias", link=True), destination)
        self.assertFalse(destination.exists())

    def test_existing_destination_is_not_overwritten(self):
        destination = self.root / "destination"
        destination.mkdir()
        (destination / "owned").write_text("preserve\n")
        with self.assertRaisesRegex(self.preparation.PreparationError, "EXTRACTION_TARGET_EXISTS"):
            self.preparation.extract(self.archive("source"), destination)
        self.assertEqual((destination / "owned").read_text(), "preserve\n")

    def test_download_checksum_mismatch_refused(self):
        with mock.patch.object(self.preparation, "urlopen", return_value=io.BytesIO(b"wrong bytes")):
            with self.assertRaisesRegex(self.preparation.PreparationError, "ARCHIVE_CHECKSUM"):
                self.preparation.download(self.preparation.GIT, self.root / "archive")

    def test_native_host_cannot_start_setup(self):
        with mock.patch.object(self.preparation, "sys", SimpleNamespace(argv=["prepare-ci-git.py"])), \
                mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}), \
                mock.patch.object(self.preparation, "download") as download:
            with self.assertRaisesRegex(self.preparation.PreparationError, "HOSTED_LINUX_ONLY"):
                self.preparation.prepare()
            download.assert_not_called()

    def test_wrong_prepared_python_refused_before_setup(self):
        runtime = SimpleNamespace(argv=["prepare-ci-git.py"], version_info=(3, 13, 15),
                                  flags=SimpleNamespace(isolated=1, no_site=1), dont_write_bytecode=True)
        with mock.patch.object(self.preparation, "sys", runtime), \
                mock.patch.object(self.preparation.platform, "system", return_value="Linux"), \
                mock.patch.object(self.preparation.platform, "machine", return_value="x86_64"), \
                mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "RUNNER_OS": "Linux", "RUNNER_ARCH": "X64"}), \
                mock.patch.object(self.preparation, "download") as download:
            with self.assertRaisesRegex(self.preparation.PreparationError, "PREPARED_PYTHON_REQUIRED"):
                self.preparation.prepare()
            download.assert_not_called()


if __name__ == "__main__":
    unittest.main()
