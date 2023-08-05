from .auth import AuthTokenLink
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from pydantic import validator, ValidationError
from cryptography.hazmat.primitives.asymmetric import rsa
from typing import Any, Callable, Awaitable, Dict
import jwt
import datetime
from rath.operation import Operation


class SignLocalLink(AuthTokenLink):
    private_key: rsa.RSAPrivateKey

    @validator("private_key", pre=True, always=True)
    def must_be_valid_pem_key(cls, v: Any) -> str:
        try:
            if isinstance(v, str):
                with open(v, "rb") as f:
                    v = f.read()

            key = serialization.load_pem_private_key(
                v, password=None, backend=default_backend()
            )

            # Check if it is an RSA key
            if not isinstance(key, rsa.RSAPrivateKey):
                raise ValidationError("PEM key is not an RSA Private key.")

            return key
        except Exception as e:
            raise ValidationError(f"Not a valid PEM key. {str(e)}")

    async def aretrieve_payload(self, Operation):
        raise NotImplementedError("Please implement this method.")

    async def aload_token(self, operation: Operation):
        payload = await self.aretrieve_payload(operation)
        token = jwt.encode(payload, key=self.private_key, algorithm="RS256")
        return token

    async def arefresh_token(self):
        raise NotImplementedError


class ComposedSignTokenLink(SignLocalLink):
    payload_retriever: Callable[[Operation], Awaitable[Dict]]

    async def aretrieve_payload(self, operation: Operation):
        return await self.payload_retriever(operation)
