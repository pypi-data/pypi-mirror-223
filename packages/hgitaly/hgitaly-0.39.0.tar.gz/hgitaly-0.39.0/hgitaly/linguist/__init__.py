# Copyright 2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from hashlib import sha256
import json
import subprocess

from grpc import StatusCode
from importlib_resources import files


def read_linguist_languages(path):
    res = {}
    with path.open() as langf:
        for name, details in json.load(langf).items():
            color = details.get('color')
            if color is not None:
                res[name] = color
    return res


LANGUAGE_COLORS = read_linguist_languages(
    files(__name__).joinpath('languages.json'))


def language_color(lang_name):
    """Perform the same defaulting as in Gitaly.

    This is not thread-safe, because it actually updates
    :data:`LANGUAGE_COLORS` due to defaulting in case the detected language
    does not have a color there. That is not a problem: HGitaly is not
    multithreaded (or rather uses a unique service thread at a given time,
    out of the pool still created by grpcio).

    As of this writing, go-enry v2.8.3 (already used by Gitaly to return the
    color) defaults to `#cccccc`:

      // GetColor returns a HTML color code of a given language.
      func GetColor(language string) string {
        if color, ok := data.LanguagesColor[language]; ok {
            return color
        }

        if color, ok := data.LanguagesColor[GetLanguageGroup(language)]; ok {
            return color
        }

        return "#cccccc"
      }

    Gitaly then concludes with (from internal/gitaly/linguist/linguist.go) ::

      // Color returns the color Linguist has assigned to language.
      func Color(language string) string {
        if color := enry.GetColor(language); color != "#cccccc" {
            return color
        }

        colorSha := sha256.Sum256([]byte(language))
        return fmt.Sprintf("#%x", colorSha[0:3])
      }
    """
    color = LANGUAGE_COLORS.get(lang_name)
    if color is not None:
        return color

    color_sha = sha256(lang_name.encode('utf-8')).hexdigest()
    color = '#' + color_sha[:6]
    LANGUAGE_COLORS[lang_name] = color
    return color


def language_stats(bin_path, path, context):
    """Return the full language stats working directory at given path.

    :param str bin_path: path to the Tokei executable
    :param path: the directory to analyze as a :class:`pathlib.Path` instance.
    """
    try:
        tokei = subprocess.run(
            (bin_path, '--compact', '-o', 'json', path),
            encoding='utf-8',
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        # in Gitaly 15.5, the resulting error code is 'INTERNAL', with
        # details 'language stats: waiting for linguist: exit status %d'
        context.abort(
            StatusCode.INTERNAL,
            "CommitLanguages: tokei error status code=%d stderr=%r" % (
                exc.returncode, exc.stderr))
    except FileNotFoundError:
        # in Gitaly 15.5, if `gitaly-linguist` cannot be found, the resulting
        # error code is `INTERNAL`, with details 'language stats: waiting
        # for linguist: exit status 127' (same as rewrapping in a shell)
        context.abort(
            StatusCode.INTERNAL,
            "language stats: tokei executable '%s' not found" % bin_path)
    except PermissionError:
        # Gitaly 15.5 behaves similarly in this case as in the not found case,
        # only with exit status 126 in details (same as in a shell, again)
        context.abort(
            StatusCode.INTERNAL,
            "language stats: permission denied to run "
            "tokei executable '%s'" % bin_path)

    # overriding variable also to free buffer immediately, as it can be
    # fairly big, e.g. 10MB for heptapod-rails
    tokei = json.loads(tokei.stdout)

    stats = {}
    total = 0

    for lang_name, details in tokei.items():
        # We can't use the `Total` entry because the ratios we have
        # to produce are expressed in bytes, not lines.
        if lang_name == 'Total':
            continue

        per_file = details['reports']
        total_bytes = 0
        for report in per_file:
            total_bytes += (path / report['name']).stat().st_size
        stats[lang_name] = dict(files=len(per_file),
                                total_bytes=total_bytes,
                                )
        total += total_bytes
    return stats, total
