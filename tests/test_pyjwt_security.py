"""Run: python -m unittest discover -s tests -v (with project requirements)."""

import base64
import datetime
import hashlib
import hmac
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import jwt
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509.oid import NameOID


def forge_hs256(public_material):
    def b64(value):
        return base64.urlsafe_b64encode(value).rstrip(b"=")

    header = b64(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = b64(json.dumps({"sub": "forged-user"}).encode())
    message = header + b"." + payload
    signature = hmac.new(public_material, message, hashlib.sha256).digest()
    return (message + b"." + b64(signature)).decode()


class JWTKeySafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.ec_key = ec.generate_private_key(ec.SECP256R1())

    def test_der_public_keys_and_certificate_reject_hmac_forgery(self):
        """GHSA-p4g4-x82p-q773: public DER bytes are never HMAC secrets."""
        public = self.rsa_key.public_key()
        name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "test.invalid")])
        now = datetime.datetime.utcnow()
        certificate = (
            x509.CertificateBuilder().subject_name(name).issuer_name(name)
            .public_key(public).serial_number(1)
            .not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=1))
            .sign(self.rsa_key, hashes.SHA256())
        )
        materials = {
            "spki": public.public_bytes(serialization.Encoding.DER,
                                        serialization.PublicFormat.SubjectPublicKeyInfo),
            "pkcs1": public.public_bytes(serialization.Encoding.DER,
                                         serialization.PublicFormat.PKCS1),
            "certificate": certificate.public_bytes(serialization.Encoding.DER),
        }
        for label, material in materials.items():
            with self.subTest(encoding=label):
                with self.assertRaises(jwt.InvalidKeyError):
                    jwt.decode(forge_hs256(material), material,
                               algorithms=["RS256", "HS256"])

    def test_mutated_pem_public_keys_reject_hmac_forgery(self):
        """GHSA-ffc3-869f-jxw9: mutated PEM never becomes an HMAC secret."""
        for algorithm, key in [("RS256", self.rsa_key), ("ES256", self.ec_key)]:
            pem = key.public_key().public_bytes(
                serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
            variants = {
                "canonical": pem,
                "tab-before-end": pem.replace(b"-----END", b"\t-----END"),
                "cr-only": pem.replace(b"\n", b"\r"),
                "single-line": b" ".join(pem.splitlines()),
            }
            for label, material in variants.items():
                with self.subTest(algorithm=algorithm, encoding=label):
                    with self.assertRaises(jwt.InvalidKeyError):
                        jwt.decode(forge_hs256(material), material,
                                   algorithms=[algorithm, "HS256"])

    def test_normal_signing_and_verification_remain_compatible(self):
        payload = {"sub": "test-user", "aud": "test-client"}
        secret = b"test-only-hmac-secret-at-least-32-bytes-long"
        for algorithm, signing_key, verification_key in [
            ("HS256", secret, secret),
            ("HS256", bytes(range(64)), bytes(range(64))),
            ("RS256", self.rsa_key, self.rsa_key.public_key()),
            ("ES256", self.ec_key, self.ec_key.public_key()),
        ]:
            with self.subTest(algorithm=algorithm):
                token = jwt.encode(payload, signing_key, algorithm=algorithm)
                self.assertEqual(jwt.decode(token, verification_key,
                                            algorithms=[algorithm], audience="test-client"),
                                 payload)

    def test_wrong_algorithm_and_signature_remain_rejected(self):
        secret = b"test-only-hmac-secret-at-least-32-bytes-long"
        token = jwt.encode({"sub": "test-user"}, secret, algorithm="HS256")
        with self.assertRaises(jwt.InvalidAlgorithmError):
            jwt.decode(token, self.rsa_key.public_key(), algorithms=["RS256"])
        with self.assertRaises(jwt.InvalidSignatureError):
            jwt.decode(token, b"different-test-secret-at-least-32-bytes", algorithms=["HS256"])


class JWKSRedirectTests(unittest.TestCase):
    def test_redirect_rejected_without_contacting_destination(self):
        """GHSA-9v7f-9g4p-ffgj: do not forward headers or trust redirect keys."""
        requests = []

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append((self.path, self.headers.get("X-Test-Header")))
                if self.path == "/redirect":
                    self.send_response(302)
                    self.send_header("Location", "/destination")
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b'{"keys": []}')

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            base = "http://127.0.0.1:%d" % server.server_port
            client = jwt.PyJWKClient(base + "/redirect", timeout=2,
                                     headers={"X-Test-Header": "test-only"})
            with self.assertRaises(jwt.PyJWKClientConnectionError):
                client.fetch_data()
            self.assertEqual(requests, [("/redirect", "test-only")])
            self.assertEqual(jwt.PyJWKClient(base + "/normal", timeout=2).fetch_data(),
                             {"keys": []})
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
