import hashlib
from django.utils.crypto import (
    constant_time_compare, get_random_string, pbkdf2,
)
import base64


def make_password(password):
    hasher = PBKDF2PasswordHasher()
    return hasher.encode(password, PBKDF2PasswordHasher.salt())


def verify(password, encoded):
    return PBKDF2PasswordHasher().verify(password, encoded)


class PBKDF2PasswordHasher:
    """
    Secure password hashing using the PBKDF2 algorithm (recommended)

    Configured to use PBKDF2 + HMAC + SHA256.
    The result is a 64 byte binary string.  Iterations may be changed
    safely but you must rename the algorithm if you change SHA256.
    """
    algorithm = "pbkdf2_sha256"
    iterations = 120000
    digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return constant_time_compare(encoded, encoded_2)

    @staticmethod
    def salt():
        """Generate a cryptographically secure nonce salt in ASCII."""
        return get_random_string()

