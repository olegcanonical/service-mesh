"""Compatibility shim for Kubernetes API CAs that fail Python 3.13+ strict X.509 checks.

Python 3.13 enabled VERIFY_X509_STRICT by default. Some clusters (e.g. MicroK8s) issue a
CA without the keyUsage extension, which makes every Kubernetes API call fail with
"CA cert does not include key usage extension". The chain is still fully verified; only
the strict-profile flag is cleared.
"""

import ssl

_original = ssl.create_default_context


def _create_default_context(*args, **kwargs) -> ssl.SSLContext:
    context = _original(*args, **kwargs)
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return context


ssl.create_default_context = _create_default_context
